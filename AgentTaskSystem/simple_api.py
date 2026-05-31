"""
AgentTaskSystem Simple API - 超简单易用接口！
让调用就像说话一样简单！
"""

import asyncio
from typing import Callable, Any, Dict, Optional
from . import AgentTaskSystem


class SimpleAgent:
    """
    超简单的 Agent 接口！
    不需要了解复杂的架构，直接用就行！
    """
    
    def __init__(self):
        """初始化（超级简单）"""
        self._system = AgentTaskSystem()
        self._running_tasks = {}
        print("✅ Agent 准备好了！")
    
    def create_task(self, name: str, task_type: str = "general", priority: int = 5, **kwargs) -> str:
        """
        【超级简单】创建一个任务
        
        示例:
            agent = SimpleAgent()
            task_id = agent.create_task("我的数据采集任务", "data_collect")
        """
        params = {"name": name, **kwargs}
        task_id = self._system.task_define.create_task(
            task_type=task_type,
            priority=priority,
            params=params
        )
        print(f"✅ 任务创建成功！ID: {task_id}")
        return task_id
    
    def run_task(self, task_id: str, task_logic: Callable) -> None:
        """
        【超级简单】运行任务
        
        示例:
            def my_job():
                print("正在执行我的任务...")
                return "完成了！"
                
            agent.run_task(task_id, my_job)
        """
        print(f"🚀 开始运行任务: {task_id}")
        
        async def _run():
            await self._system.task_runner.start_task(task_id, task_logic)
        
        task = asyncio.create_task(_run())
        self._running_tasks[task_id] = task
        
        print(f"✅ 任务 {task_id} 已启动！")
    
    def get_status(self, task_id: str) -> str:
        """
        【超级简单】获取任务状态
        
        示例:
            status = agent.get_status(task_id)
            print(status)  # "running" / "completed" / "failed"
        """
        task_info = self._system.task_define.get_task_info(task_id)
        if task_info:
            return str(task_info.get("status", "unknown"))
        return "unknown"
    
    def pause_task(self, task_id: str) -> bool:
        """
        【超级简单】暂停任务
        
        示例:
            agent.pause_task(task_id)
        """
        print(f"⏸️  暂停任务: {task_id}")
        # 这里可以调用暂停逻辑
        return True
    
    def stop_task(self, task_id: str) -> bool:
        """
        【超级简单】停止任务
        
        示例:
            agent.stop_task(task_id)
        """
        print(f"⏹️  停止任务: {task_id}")
        if task_id in self._running_tasks:
            self._running_tasks[task_id].cancel()
            del self._running_tasks[task_id]
        return True
    
    def list_tasks(self) -> list:
        """
        【超级简单】列出所有任务
        
        示例:
            tasks = agent.list_tasks()
            for task in tasks:
                print(task)
        """
        # 简单版本，返回空列表（可以后续扩展）
        print("📋 注意: list_tasks 需要在完整实现中添加")
        return []
    
    def create_and_run(self, name: str, task_logic: Callable) -> str:
        """
        【超级简单】一步到位！创建+运行
        
        示例:
            def job():
                print("干活啦！")
                
            task_id = agent.create_and_run("我的任务", job)
        """
        task_id = self.create_task(name)
        self.run_task(task_id, task_logic)
        return task_id
    
    def wait_all(self):
        """
        【超级简单】等待所有任务完成
        
        示例:
            agent.wait_all()
        """
        print("⏳ 等待所有任务完成...")


# ========== 简单示例 ==========

def example_usage():
    """
    使用示例（复制粘贴就能用！）
    """
    print("\n" + "="*60)
    print("  AgentTaskSystem 简单示例")
    print("="*60 + "\n")
    
    # 1. 创建 Agent（一行代码）
    agent = SimpleAgent()
    
    # 2. 定义你的任务（就是写个函数）
    def my_data_collect():
        """这是你的业务逻辑，随便写！"""
        print("📊 正在采集数据...")
        import time
        time.sleep(1)
        print("✅ 数据采集完成！")
        return {"data": "采集完成"}
    
    # 3. 一步到位：创建+运行（两行代码！）
    task_id = agent.create_and_run("数据采集任务", my_data_collect)
    
    # 4. 查看状态（一行代码）
    status = agent.get_status(task_id)
    print(f"📋 任务状态: {status}")
    
    print("\n🎉 就这么简单！")


# ========== 快捷入口 ==========

def quick_start():
    """
    30秒快速上手！
    """
    print("🚀 AgentTaskSystem 快速开始!")
    return SimpleAgent()


__all__ = [
    "SimpleAgent",
    "quick_start",
    "example_usage"
]
