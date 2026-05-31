"""
🚀 超级简单接口！
一行代码创建，一行代码运行！
"""

import time
import asyncio
import sys
from typing import Callable


class SuperSimpleAgent:
    """
    极简Agent！
    用法简单到爆炸！
    """
    
    def __init__(self):
        self._tasks = []
        print("✅ Agent 已启动！", flush=True)
    
    def every(self, seconds: int, task_name: str = "任务"):
        """
        装饰器：每隔N秒运行一次
        
        用法：
            @agent.every(5)
            def my_task():
                print("干活！")
        """
        def decorator(func: Callable):
            self._tasks.append({
                "type": "scheduled",
                "interval": seconds,
                "name": task_name,
                "func": func
            })
            print(f"✅ 添加定时任务: {task_name} (每{seconds}秒)", flush=True)
            return func
        return decorator
    
    def forever(self, task_name: str = "任务"):
        """
        装饰器：一直运行
        
        用法：
            @agent.forever()
            def my_task():
                print("一直运行！")
        """
        def decorator(func: Callable):
            self._tasks.append({
                "type": "loop",
                "name": task_name,
                "func": func
            })
            print(f"✅ 添加循环任务: {task_name}", flush=True)
            return func
        return decorator
    
    def run(self, duration: int = None):
        """
        启动所有任务！
        
        参数:
            duration: 运行多少秒后自动停止（不填就一直运行）
        
        用法：
            agent.run()           # 一直运行
            agent.run(10)         # 运行10秒
        """
        print("\n🚀 开始运行！\n", flush=True)
        
        async def _run():
            tasks = []
            
            for task in self._tasks:
                if task["type"] == "scheduled":
                    async def _scheduled(t=task):
                        while True:
                            try:
                                t["func"]()
                            except Exception as e:
                                print(f"❌ {t['name']} 失败: {e}", flush=True)
                            await asyncio.sleep(t["interval"])
                    
                    tasks.append(asyncio.create_task(_scheduled()))
                    
                elif task["type"] == "loop":
                    async def _loop(t=task):
                        while True:
                            try:
                                t["func"]()
                            except Exception as e:
                                print(f"❌ {t['name']} 失败: {e}", flush=True)
                            await asyncio.sleep(1)
                    
                    tasks.append(asyncio.create_task(_loop()))
            
            if tasks:
                if duration:
                    # 运行指定时间
                    await asyncio.wait_for(
                        asyncio.gather(*tasks),
                        timeout=duration
                    )
                else:
                    # 一直运行
                    await asyncio.gather(*tasks)
        
        try:
            asyncio.run(_run())
        except asyncio.TimeoutError:
            print(f"\n⏹️  运行 {duration} 秒，自动停止", flush=True)
        except KeyboardInterrupt:
            print("\n⏹️  Agent 已停止", flush=True)


# ============================================
# 🎮 使用示例（超级简单！）
# ============================================

if __name__ == "__main__":
    
    # 创建Agent
    agent = SuperSimpleAgent()
    
    # 示例1：每隔3秒运行一次
    @agent.every(2, "数据检查")
    def check_data():
        print("📊 检查数据...", flush=True)
    
    # 示例2：每隔5秒运行一次
    @agent.every(4, "健康检查")
    def check_health():
        print("❤️  检查健康...", flush=True)
    
    # 示例3：一直运行
    @agent.forever("监控任务")
    def monitor():
        print("👀 监控中...", flush=True)
        time.sleep(0.5)
    
    # 启动！运行10秒自动停止
    print("\n💡 运行10秒后自动停止\n", flush=True)
    agent.run(10)
    
    print("\n✅ 演示完成！", flush=True)
