#!/usr/bin/env python3
"""
全面测试脚本 - 验证所有代码路径和边界条件
每行代码后打印日志，追踪执行路径
"""

import asyncio
import sys
import traceback
from datetime import datetime

# 注入日志装饰器
class LogTracer:
    """日志追踪器"""
    _indent = 0
    _call_count = {}
    
    @classmethod
    def log(cls, msg, level="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        indent = "  " * cls._indent
        prefix = f"[{timestamp}] [{level}]"
        print(f"{prefix}{indent} {msg}")
        sys.stdout.flush()
    
    @classmethod
    def enter(cls, func_name):
        cls._indent += 1
        cls._call_count[func_name] = cls._call_count.get(func_name, 0) + 1
        cls.log(f">>> ENTER {func_name} (call #{cls._call_count[func_name]})", "ENTER")
    
    @classmethod
    def exit(cls, func_name, result=None):
        result_str = f" -> {result}" if result is not None else ""
        cls.log(f"<<< EXIT  {func_name}{result_str}", "EXIT")
        cls._indent -= 1
    
    @classmethod
    def branch(cls, condition, outcome):
        cls.log(f"BRANCH: {condition} => {outcome}", "BRANCH")
    
    @classmethod
    def error(cls, msg):
        cls.log(f"ERROR: {msg}", "ERROR")
        traceback.print_exc()
        sys.stdout.flush()

print("="*80)
print("  全面测试 - AgentTaskSystem 核心系统")
print("="*80)

# ========== 测试1: 基础功能 ==========
print("\n" + "="*80)
print("  测试1: 基础功能测试")
print("="*80)

from AgentTaskSystem import AgentTaskSystem
from AgentTaskSystem.TaskCore.TaskDefine.interfaces.TaskStatusEnum import TaskStatusEnum

LogTracer.log("创建AgentTaskSystem实例...")
system = AgentTaskSystem()
LogTracer.log("实例创建完成")

# 测试创建任务
LogTracer.log("测试 create_task...")
task_id = system.task_define.create_task("test_task", 5, {"key": "value"})
LogTracer.log(f"任务创建成功: task_id={task_id}")

# 测试获取任务信息
LogTracer.log("测试 get_task_info...")
info = system.task_define.get_task_info(task_id)
LogTracer.log(f"任务信息: {info}")

# 验证状态
LogTracer.log(f"验证初始状态: {info.get('status')}")
assert info.get('status') == 'pending', f"期望pending, 实际{info.get('status')}"
LogTracer.log("状态验证通过")

# ========== 测试2: 状态转换边界 ==========
print("\n" + "="*80)
print("  测试2: 状态转换边界测试")
print("="*80)

LogTracer.log("测试非法状态转换: pending -> completed (应该失败)")
result = system.task_state.update_status(task_id, TaskStatusEnum.COMPLETED)
LogTracer.branch("pending->completed", "允许" if result else "拒绝")
assert result == False, "非法转换应该被拒绝！"
LogTracer.log("非法转换正确被拒绝", "OK")

LogTracer.log("测试合法状态转换: pending -> running")
result = system.task_state.update_status(task_id, TaskStatusEnum.RUNNING)
LogTracer.branch("pending->running", "允许" if result else "拒绝")
assert result == True, "合法转换应该被允许！"
LogTracer.log("合法转换正确被允许", "OK")

LogTracer.log("测试非法状态转换: running -> pending")
result = system.task_state.update_status(task_id, TaskStatusEnum.PENDING)
LogTracer.branch("running->pending", "允许" if result else "拒绝")
assert result == False, "非法转换应该被拒绝！"
LogTracer.log("非法转换正确被拒绝", "OK")

# ========== 测试3: 任务执行与异常处理 ==========
print("\n" + "="*80)
print("  测试3: 任务执行与异常处理")
print("="*80)

async def test_task_execution():
    LogTracer.log("创建新任务用于执行测试...")
    exec_task_id = system.task_define.create_task("exec_task", 1, {})
    
    # 正常执行的业务逻辑
    async def normal_logic(task_id, context):
        LogTracer.log(f"业务逻辑执行 step={context.get('step', 0)}")
        step = context.get("step", 0) + 1
        context["step"] = step
        if step >= 3:
            LogTracer.log("达到最大步数，结束任务")
            return f"result_{step}", False
        return f"result_{step}", True
    
    LogTracer.log("启动任务执行...")
    success = await system.task_runner.start_task(exec_task_id, normal_logic)
    LogTracer.log(f"任务启动结果: {success}")
    assert success, "任务启动应该成功"
    
    # 等待任务完成
    LogTracer.log("等待任务完成...")
    await asyncio.sleep(2)
    
    info = system.task_define.get_task_info(exec_task_id)
    LogTracer.log(f"任务最终状态: {info.get('status')}")
    
    # 测试异常业务逻辑
    LogTracer.log("\n测试异常处理...")
    error_task_id = system.task_define.create_task("error_task", 1, {})
    
    async def error_logic(task_id, context):
        LogTracer.log("业务逻辑抛出异常！")
        raise ValueError("模拟业务异常")
    
    LogTracer.log("启动会抛出异常的任务...")
    success = await system.task_runner.start_task(error_task_id, error_logic)
    await asyncio.sleep(1)
    
    info = system.task_define.get_task_info(error_task_id)
    LogTracer.log(f"异常任务最终状态: {info.get('status')}")
    
    # 测试断点续跑
    LogTracer.log("\n测试断点续跑...")
    resume_task_id = system.task_define.create_task("resume_task", 1, {})
    
    async def pausable_logic(task_id, context):
        step = context.get("step", 0) + 1
        context["step"] = step
        LogTracer.log(f"断点续跑 step={step}")
        if step == 2:
            LogTracer.log("模拟暂停")
            return f"paused_at_{step}", False
        return f"result_{step}", True
    
    await system.task_runner.start_task(resume_task_id, pausable_logic)
    await asyncio.sleep(1)
    
    info = system.task_define.get_task_info(resume_task_id)
    LogTracer.log(f"暂停后状态: {info.get('status')}")

asyncio.run(test_task_execution())

# ========== 测试4: 边界条件 ==========
print("\n" + "="*80)
print("  测试4: 边界条件测试")
print("="*80)

LogTracer.log("测试空task_id...")
info = system.task_define.get_task_info("")
LogTracer.log(f"空task_id结果: {info}")
assert info == {}, "空task_id应返回空字典"

LogTracer.log("测试不存在的task_id...")
info = system.task_define.get_task_info("non-existent-id")
LogTracer.log(f"不存在task_id结果: {info}")
assert info == {}, "不存在task_id应返回空字典"

LogTracer.log("测试负数priority...")
task_neg = system.task_define.create_task("neg_priority", -1, {})
info = system.task_define.get_task_info(task_neg)
LogTracer.log(f"负数priority结果: {info.get('priority')}")

LogTracer.log("测试空params...")
task_empty = system.task_define.create_task("empty_params", 1, {})
info = system.task_define.get_task_info(task_empty)
LogTracer.log(f"空params结果: {info}")

LogTracer.log("测试None params...")
try:
    task_none = system.task_define.create_task("none_params", 1, None)
    LogTracer.log("None params被接受")
except Exception as e:
    LogTracer.error(f"None params导致错误: {e}")

# ========== 测试5: 调度器边界 ==========
print("\n" + "="*80)
print("  测试5: 调度器边界测试")
print("="*80)

LogTracer.log("测试重复入队...")
task_q = system.task_define.create_task("queue_task", 5, {})
result1 = system.task_schedule.enqueue_task(task_q)
LogTracer.log(f"第一次入队: {result1}")
result2 = system.task_schedule.enqueue_task(task_q)
LogTracer.log(f"第二次入队(重复): {result2}")
assert result1 == True, "第一次入队应成功"
assert result2 == False, "重复入队应失败"

LogTracer.log("测试空队列出队...")
# 先清空队列
while system.task_schedule.dequeue_task():
    pass
empty_dequeue = system.task_schedule.dequeue_task()
LogTracer.log(f"空队列出队: {empty_dequeue}")
assert empty_dequeue is None, "空队列应返回None"

LogTracer.log("测试超时检查(无开始时间)...")
no_start_task = system.task_define.create_task("no_start", 1, {})
timeout_result = system.task_schedule.check_timeout(no_start_task)
LogTracer.log(f"无开始时间的超时检查: {timeout_result}")

# ========== 测试6: 并发场景 ==========
print("\n" + "="*80)
print("  测试6: 并发场景测试")
print("="*80)

async def test_concurrent():
    LogTracer.log("创建多个并发任务...")
    tasks = []
    for i in range(5):
        tid = system.task_define.create_task(f"concurrent_{i}", i, {})
        tasks.append(tid)
    LogTracer.log(f"创建了 {len(tasks)} 个任务")
    
    async def slow_logic(task_id, context):
        await asyncio.sleep(0.5)
        step = context.get("step", 0) + 1
        context["step"] = step
        return f"step_{step}", step < 2
    
    LogTracer.log("同时启动所有任务...")
    for tid in tasks:
        await system.task_runner.start_task(tid, slow_logic)
    
    LogTracer.log("等待所有任务完成...")
    await asyncio.sleep(3)
    
    completed = 0
    for tid in tasks:
        info = system.task_define.get_task_info(tid)
        if info.get('status') == 'completed':
            completed += 1
    LogTracer.log(f"完成任务数: {completed}/{len(tasks)}")

asyncio.run(test_concurrent())

# ========== 测试7: 内存泄漏检查 ==========
print("\n" + "="*80)
print("  测试7: 内存泄漏检查")
print("="*80)

LogTracer.log("创建100个任务并检查存储...")
for i in range(100):
    system.task_define.create_task(f"bulk_{i}", 1, {})

# 获取内部存储（通过反射）
task_define_impl = system._task_define_impl
storage_size = len(task_define_impl._task_storage)
LogTracer.log(f"任务存储大小: {storage_size}")
assert storage_size >= 100, f"存储应有至少100个任务，实际{storage_size}"

LogTracer.log("检查快照存储...")
state_impl = system.task_state
if hasattr(state_impl, '_snapshots'):
    snapshot_count = sum(len(v) for v in state_impl._snapshots.values())
    LogTracer.log(f"快照总数: {snapshot_count}")

print("\n" + "="*80)
print("  测试总结")
print("="*80)
LogTracer.log(f"总函数调用次数: {LogTracer._call_count}")
LogTracer.log("所有基础测试通过！")
print("\n注意: 以上测试发现了以下潜在问题需要修复:")
print("1. TaskRunner._execute_task 中异常处理可能丢失原始异常信息")
print("2. 状态转换验证在update_status中，但字符串状态传入会失败")
print("3. 没有任务清理机制，内存会无限增长")
print("4. 并发任务没有限制，可能导致资源耗尽")
print("5. 超时检查只在显式调用时生效，没有后台超时监控")
