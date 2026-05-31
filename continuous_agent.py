"""
🤖 Agent 持续运行任务！
方案：用纯 Python 实现，不需要系统权限
"""

import time
import asyncio
from typing import Callable, Dict, Any, Optional
from datetime import datetime


class ContinuousAgent:
    """
    持续运行的 Agent！
    支持：
    - 定时任务（每隔N秒运行一次）
    - 循环任务（一直运行，失败自动重启）
    - 队列任务（任务一个接一个运行）
    """
    
    def __init__(self):
        self.tasks: Dict[str, Dict] = {}
        self._running = False
        self._task_counter = 0
        print("✅ ContinuousAgent 准备好了！")
    
    def add_scheduled_task(self, name: str, interval_seconds: int, task_func: Callable) -> str:
        """
        添加定时任务（每隔N秒运行一次）
        
        参数:
            name: 任务名称
            interval_seconds: 间隔秒数
            task_func: 你的任务函数
            
        示例:
            def my_job():
                print("干活啦！")
                
            agent.add_scheduled_task("我的定时任务", 5, my_job)
        """
        self._task_counter += 1
        task_id = f"scheduled_{self._task_counter}"
        
        self.tasks[task_id] = {
            "id": task_id,
            "name": name,
            "type": "scheduled",
            "interval": interval_seconds,
            "func": task_func,
            "enabled": True,
            "last_run": None,
            "run_count": 0
        }
        
        print(f"✅ 添加定时任务: {name} (间隔 {interval_seconds}s)")
        return task_id
    
    def add_loop_task(self, name: str, task_func: Callable, max_retries: int = 3) -> str:
        """
        添加循环任务（一直运行，失败自动重试）
        
        参数:
            name: 任务名称
            task_func: 你的任务函数
            max_retries: 最大重试次数
            
        示例:
            def my_job():
                print("一直运行的任务！")
                
            agent.add_loop_task("我的循环任务", my_job)
        """
        self._task_counter += 1
        task_id = f"loop_{self._task_counter}"
        
        self.tasks[task_id] = {
            "id": task_id,
            "name": name,
            "type": "loop",
            "func": task_func,
            "max_retries": max_retries,
            "enabled": True,
            "retry_count": 0,
            "run_count": 0
        }
        
        print(f"✅ 添加循环任务: {name}")
        return task_id
    
    def add_queue_task(self, name: str, task_func: Callable) -> str:
        """
        添加队列任务（按顺序一个接一个运行）
        
        参数:
            name: 任务名称
            task_func: 你的任务函数
            
        示例:
            def job1():
                print("任务1")
                
            agent.add_queue_task("队列任务1", job1)
        """
        self._task_counter += 1
        task_id = f"queue_{self._task_counter}"
        
        self.tasks[task_id] = {
            "id": task_id,
            "name": name,
            "type": "queue",
            "func": task_func,
            "enabled": True,
            "run_count": 0
        }
        
        print(f"✅ 添加队列任务: {name}")
        return task_id
    
    async def _run_scheduled_task(self, task_info: Dict):
        """运行定时任务"""
        task_id = task_info["id"]
        name = task_info["name"]
        interval = task_info["interval"]
        func = task_info["func"]
        
        print(f"\n⏰ 定时任务启动: {name} (间隔 {interval}s)")
        
        while task_info["enabled"] and self._running:
            try:
                print(f"\n🚀 运行定时任务: {name}")
                result = func()
                print(f"✅ {name} 完成: {result}")
                
                task_info["last_run"] = datetime.now()
                task_info["run_count"] += 1
                
                # 等待下一次
                await asyncio.sleep(interval)
                
            except Exception as e:
                print(f"❌ {name} 失败: {e}")
                await asyncio.sleep(interval)
    
    async def _run_loop_task(self, task_info: Dict):
        """运行循环任务"""
        task_id = task_info["id"]
        name = task_info["name"]
        func = task_info["func"]
        max_retries = task_info["max_retries"]
        
        print(f"\n🔄 循环任务启动: {name}")
        
        while task_info["enabled"] and self._running:
            try:
                print(f"\n🚀 运行循环任务: {name}")
                result = func()
                print(f"✅ {name} 完成: {result}")
                
                task_info["retry_count"] = 0
                task_info["run_count"] += 1
                
                # 小休息一下，避免CPU 100%
                await asyncio.sleep(1)
                
            except Exception as e:
                task_info["retry_count"] += 1
                print(f"❌ {name} 失败 ({task_info['retry_count']}/{max_retries}): {e}")
                
                if task_info["retry_count"] >= max_retries:
                    print(f"⚠️  {name} 达到最大重试次数，暂停")
                    task_info["enabled"] = False
                else:
                    await asyncio.sleep(2)
    
    async def _run_queue_tasks(self):
        """运行队列任务"""
        queue_tasks = [t for t in self.tasks.values() if t["type"] == "queue" and t["enabled"]]
        
        if not queue_tasks:
            return
        
        print(f"\n📋 队列任务开始，共 {len(queue_tasks)} 个任务")
        
        for task_info in queue_tasks:
            if not self._running:
                break
                
            name = task_info["name"]
            func = task_info["func"]
            
            try:
                print(f"\n🚀 运行队列任务: {name}")
                result = func()
                print(f"✅ {name} 完成: {result}")
                task_info["run_count"] += 1
                
            except Exception as e:
                print(f"❌ {name} 失败: {e}")
    
    async def start(self):
        """
        启动所有任务！
        
        示例:
            await agent.start()
        """
        self._running = True
        print("\n" + "="*60)
        print("  🤖 Agent 启动！")
        print("="*60)
        print(f"\n📊 共 {len(self.tasks)} 个任务")
        
        # 收集所有任务
        coroutines = []
        
        # 定时任务
        for task_info in self.tasks.values():
            if task_info["type"] == "scheduled" and task_info["enabled"]:
                coroutines.append(self._run_scheduled_task(task_info))
        
        # 循环任务
        for task_info in self.tasks.values():
            if task_info["type"] == "loop" and task_info["enabled"]:
                coroutines.append(self._run_loop_task(task_info))
        
        # 队列任务
        if [t for t in self.tasks.values() if t["type"] == "queue" and t["enabled"]]:
            coroutines.append(self._run_queue_tasks())
        
        if coroutines:
            # 运行所有任务
            await asyncio.gather(*coroutines)
        else:
            print("⚠️  没有可运行的任务")
    
    def stop(self):
        """停止所有任务"""
        self._running = False
        print("\n⏹️  Agent 正在停止...")
    
    def list_tasks(self) -> list:
        """列出所有任务"""
        result = []
        for task_info in self.tasks.values():
            result.append({
                "id": task_info["id"],
                "name": task_info["name"],
                "type": task_info["type"],
                "enabled": task_info["enabled"],
                "run_count": task_info["run_count"]
            })
        return result


# ============================================
# 🎮 使用示例
# ============================================

def example_1_scheduled_task():
    """示例 1：定时任务"""
    print("\n" + "="*60)
    print("  示例 1：定时任务（每隔几秒运行一次）")
    print("="*60)
    
    agent = ContinuousAgent()
    
    # 你的任务
    def check_data():
        current_time = datetime.now().strftime("%H:%M:%S")
        print(f"📊 检查数据... ({current_time})")
        return f"检查完成 {current_time}"
    
    # 添加定时任务（每3秒运行一次）
    agent.add_scheduled_task("数据检查", 3, check_data)
    
    # 启动（运行10秒看看效果）
    async def run():
        task = asyncio.create_task(agent.start())
        await asyncio.sleep(10)  # 运行10秒
        agent.stop()
        await task
    
    asyncio.run(run())


def example_2_loop_task():
    """示例 2：循环任务（一直运行）"""
    print("\n" + "="*60)
    print("  示例 2：循环任务（一直运行，失败自动重试）")
    print("="*60)
    
    agent = ContinuousAgent()
    
    # 你的任务
    count = 0
    def monitor_health():
        nonlocal count
        count += 1
        print(f"❤️  健康检查... 第 {count} 次")
        
        # 偶尔失败一下，看看重试效果
        if count % 3 == 0:
            raise Exception("模拟失败！")
            
        return f"健康检查 OK"
    
    # 添加循环任务
    agent.add_loop_task("健康检查", monitor_health, max_retries=3)
    
    # 启动（运行8秒看看效果）
    async def run():
        task = asyncio.create_task(agent.start())
        await asyncio.sleep(8)  # 运行8秒
        agent.stop()
        await task
    
    asyncio.run(run())


def example_3_queue_task():
    """示例 3：队列任务（按顺序一个接一个）"""
    print("\n" + "="*60)
    print("  示例 3：队列任务（一个接一个运行）")
    print("="*60)
    
    agent = ContinuousAgent()
    
    # 任务 1
    def step_1():
        print("📥 步骤 1: 下载数据...")
        time.sleep(0.5)
        return "下载完成"
    
    # 任务 2
    def step_2():
        print("🔄 步骤 2: 处理数据...")
        time.sleep(0.5)
        return "处理完成"
    
    # 任务 3
    def step_3():
        print("📤 步骤 3: 上传数据...")
        time.sleep(0.5)
        return "上传完成"
    
    # 添加到队列
    agent.add_queue_task("下载数据", step_1)
    agent.add_queue_task("处理数据", step_2)
    agent.add_queue_task("上传数据", step_3)
    
    # 启动
    asyncio.run(agent.start())


def example_4_mixed():
    """示例 4：混合使用（定时 + 循环 + 队列）"""
    print("\n" + "="*60)
    print("  示例 4：混合使用（定时 + 循环 + 队列）")
    print("="*60)
    
    agent = ContinuousAgent()
    
    # 定时任务：每5秒打印一次时间
    def print_time():
        now = datetime.now().strftime("%H:%M:%S")
        print(f"⏰ 当前时间: {now}")
        return now
    
    agent.add_scheduled_task("时间打印", 5, print_time)
    
    # 循环任务：一直计数
    count = 0
    def counter():
        nonlocal count
        count += 1
        print(f"🔢 计数: {count}")
        return count
    
    agent.add_loop_task("计数器", counter)
    
    # 队列任务：初始化
    def init():
        print("🚀 系统初始化...")
        time.sleep(0.5)
        return "初始化完成"
    
    agent.add_queue_task("初始化", init)
    
    # 启动（运行12秒）
    async def run():
        task = asyncio.create_task(agent.start())
        await asyncio.sleep(12)
        agent.stop()
        await task
    
    asyncio.run(run())


def main():
    print("\n" + "🤖"*30)
    print("  AgentTaskSystem - 持续运行任务演示")
    print("🤖"*30)
    
    # 运行示例
    example_1_scheduled_task()
    example_2_loop_task()
    example_3_queue_task()
    example_4_mixed()
    
    print("\n" + "="*60)
    print("  🎉 所有示例完成！")
    print("="*60)
    print("\n💡 使用说明:")
    print("  1. agent.add_scheduled_task() - 定时任务")
    print("  2. agent.add_loop_task() - 循环任务")
    print("  3. agent.add_queue_task() - 队列任务")
    print("  4. await agent.start() - 启动所有任务")
    print("  5. agent.stop() - 停止所有任务")


if __name__ == "__main__":
    main()
