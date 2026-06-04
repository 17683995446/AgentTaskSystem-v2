#!/usr/bin/env python3
"""
压力测试脚本 - 高并发、长时间运行、内存泄漏检测
"""

import asyncio
import gc
import sys
import time
import tracemalloc
from datetime import datetime

from AgentTaskSystem import AgentTaskSystem
from AgentTaskSystem.TaskCore.TaskDefine.interfaces.TaskStatusEnum import TaskStatusEnum


def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")
    sys.stdout.flush()


async def test_concurrent_stress():
    """高并发压力测试"""
    log("="*60)
    log("  并发压力测试 - 100个任务同时执行")
    log("="*60)

    system = AgentTaskSystem()
    task_count = 100
    tasks = []

    # 创建100个任务
    log(f"创建 {task_count} 个任务...")
    for i in range(task_count):
        tid = system.task_define.create_task(f"stress_{i}", i % 10 + 1, {"index": i})
        tasks.append(tid)
    log(f"任务创建完成")

    # 业务逻辑：模拟不同执行时间
    async def varied_logic(task_id, context):
        # 从task_define获取原始params中的index
        task_info = system.task_define.get_task_info(task_id)
        params = task_info.get("params", {})
        idx = params.get("index", 0)
        # 不同任务有不同延迟
        delay = 0.01 * (idx % 5 + 1)
        await asyncio.sleep(delay)
        step = context.get("step", 0) + 1
        context["step"] = step
        # 10%的任务会失败
        if idx % 10 == 9:
            raise ValueError(f"模拟第{idx}号任务失败")
        return f"result_{step}", step < 3

    # 同时启动所有任务
    log("同时启动所有任务...")
    start_time = time.time()
    for tid in tasks:
        await system.task_runner.start_task(tid, varied_logic)

    # 等待所有任务完成
    log("等待任务完成...")
    await asyncio.sleep(5)
    elapsed = time.time() - start_time

    # 统计结果
    completed = 0
    failed = 0
    pending = 0
    running = 0
    for tid in tasks:
        info = system.task_define.get_task_info(tid)
        status = info.get("status", "unknown")
        if status == "completed":
            completed += 1
        elif status == "failed":
            failed += 1
        elif status == "pending":
            pending += 1
        elif status == "running":
            running += 1

    log(f"\n执行结果统计:")
    log(f"  总任务: {task_count}")
    log(f"  完成: {completed}")
    log(f"  失败: {failed}")
    log(f"  挂起: {pending}")
    log(f"  运行中: {running}")
    log(f"  耗时: {elapsed:.2f}秒")
    log(f"  成功率: {completed}/{task_count} = {completed/task_count*100:.1f}%")

    assert failed == 10, f"期望10个失败，实际{failed}"
    assert completed == 90, f"期望90个完成，实际{completed}"
    log("并发压力测试通过!")


async def test_memory_leak():
    """内存泄漏检测"""
    log("\n" + "="*60)
    log("  内存泄漏检测 - 创建1000个任务")
    log("="*60)

    system = AgentTaskSystem()

    # 强制垃圾回收
    gc.collect()
    tracemalloc.start()
    snapshot1 = tracemalloc.take_snapshot()

    # 创建1000个任务
    log("创建1000个任务...")
    for i in range(1000):
        system.task_define.create_task(f"mem_{i}", 1, {"data": "x" * 100})

    # 检查内存使用
    snapshot2 = tracemalloc.take_snapshot()
    top_stats = snapshot2.compare_to(snapshot1, 'lineno')

    log("\n内存使用Top 5:")
    for stat in top_stats[:5]:
        log(f"  {stat}")

    # 检查任务存储
    task_define_impl = system._task_define_impl
    storage_size = len(task_define_impl._task_storage)
    log(f"\n任务存储大小: {storage_size}")
    assert storage_size == 1000, f"期望1000个任务，实际{storage_size}"

    # 检查快照存储
    state_impl = system.task_state
    if hasattr(state_impl, '_snapshots'):
        snapshot_count = sum(len(v) for v in state_impl._snapshots.values())
        log(f"快照总数: {snapshot_count}")

    tracemalloc.stop()
    log("内存泄漏检测完成")


async def test_long_running():
    """长时间运行测试"""
    log("\n" + "="*60)
    log("  长时间运行测试 - 任务循环100次")
    log("="*60)

    system = AgentTaskSystem()
    tid = system.task_define.create_task("long_run", 1, {})

    execution_count = 0

    async def long_logic(task_id, context):
        nonlocal execution_count
        execution_count += 1
        step = context.get("step", 0) + 1
        context["step"] = step
        # 模拟快速执行
        await asyncio.sleep(0.001)
        return f"step_{step}", step < 100

    log("启动长时间运行任务...")
    start_time = time.time()
    await system.task_runner.start_task(tid, long_logic)
    await asyncio.sleep(3)
    elapsed = time.time() - start_time

    info = system.task_define.get_task_info(tid)
    log(f"任务状态: {info.get('status')}")
    log(f"执行次数: {execution_count}")
    log(f"总耗时: {elapsed:.2f}秒")

    # 检查快照数量
    state_impl = system.task_state
    if hasattr(state_impl, '_snapshots'):
        snapshots = state_impl._snapshots.get(tid, [])
        log(f"快照数量: {len(snapshots)}")
        if len(snapshots) > 50:
            log("警告: 快照数量过多，可能导致内存泄漏!")

    assert info.get("status") == "completed", f"期望completed，实际{info.get('status')}"
    assert execution_count == 100, f"期望100次执行，实际{execution_count}"
    log("长时间运行测试通过!")


async def test_state_transitions_comprehensive():
    """全面状态转换测试"""
    log("\n" + "="*60)
    log("  全面状态转换测试")
    log("="*60)

    system = AgentTaskSystem()

    # 所有状态
    all_statuses = [
        TaskStatusEnum.PENDING,
        TaskStatusEnum.RUNNING,
        TaskStatusEnum.PAUSED,
        TaskStatusEnum.COMPLETED,
        TaskStatusEnum.FAILED,
        TaskStatusEnum.CANCELLED,
    ]

    # 测试所有状态转换组合
    log("测试所有状态转换组合...")
    valid_transitions = 0
    invalid_transitions = 0

    for from_status in all_statuses:
        for to_status in all_statuses:
            tid = system.task_define.create_task(f"st_{from_status.value}_{to_status.value}", 1, {})
            # 先设置初始状态
            if from_status != TaskStatusEnum.PENDING:
                # 需要合法路径到达目标状态
                if from_status == TaskStatusEnum.RUNNING:
                    system.task_state.update_status(tid, TaskStatusEnum.RUNNING)
                elif from_status == TaskStatusEnum.PAUSED:
                    system.task_state.update_status(tid, TaskStatusEnum.RUNNING)
                    system.task_state.update_status(tid, TaskStatusEnum.PAUSED)
                elif from_status == TaskStatusEnum.COMPLETED:
                    system.task_state.update_status(tid, TaskStatusEnum.RUNNING)
                    system.task_state.update_status(tid, TaskStatusEnum.COMPLETED)
                elif from_status == TaskStatusEnum.FAILED:
                    system.task_state.update_status(tid, TaskStatusEnum.RUNNING)
                    system.task_state.update_status(tid, TaskStatusEnum.FAILED)
                elif from_status == TaskStatusEnum.CANCELLED:
                    system.task_state.update_status(tid, TaskStatusEnum.RUNNING)
                    system.task_state.update_status(tid, TaskStatusEnum.CANCELLED)

            result = system.task_state.update_status(tid, to_status)
            if result:
                valid_transitions += 1
            else:
                invalid_transitions += 1

    total = valid_transitions + invalid_transitions
    log(f"总转换尝试: {total}")
    log(f"合法转换: {valid_transitions}")
    log(f"非法转换(正确拒绝): {invalid_transitions}")
    log(f"合法率: {valid_transitions/total*100:.1f}%")


async def main():
    log("\n" + "="*60)
    log("  AgentTaskSystem 压力测试套件")
    log("="*60)

    await test_concurrent_stress()
    await test_memory_leak()
    await test_long_running()
    await test_state_transitions_comprehensive()

    log("\n" + "="*60)
    log("  所有压力测试完成!")
    log("="*60)


if __name__ == "__main__":
    asyncio.run(main())
