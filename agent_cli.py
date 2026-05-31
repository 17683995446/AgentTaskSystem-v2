#!/usr/bin/env python3
"""
🖥️ AgentTaskSystem CLI 命令行工具！
在终端里直接操作！
"""

import sys
import time
import asyncio
import argparse
from typing import Callable


class AgentCLI:
    """
    命令行版 Agent！
    用法：python agent_cli.py [命令] [参数]
    """
    
    def __init__(self):
        self.tasks = {}
        self.task_counter = 0
        self.running = False
    
    def add_task(self, name: str, interval: int, func: Callable):
        """添加定时任务"""
        self.task_counter += 1
        task_id = f"task_{self.task_counter}"
        self.tasks[task_id] = {
            "id": task_id,
            "name": name,
            "interval": interval,
            "func": func,
            "type": "scheduled"
        }
        print(f"✅ 添加任务: {name} (每{interval}秒)")
        return task_id
    
    def list_tasks(self):
        """列出所有任务"""
        if not self.tasks:
            print("📭 暂无任务")
            return
        
        print("\n📋 任务列表:")
        print("-" * 50)
        for task_id, task in self.tasks.items():
            print(f"  {task_id}: {task['name']} (每{task['interval']}秒)")
        print("-" * 50)
    
    def run_all(self, duration: int = None):
        """运行所有任务"""
        if not self.tasks:
            print("❌ 没有任务可运行")
            return
        
        print(f"\n🚀 启动 {len(self.tasks)} 个任务...")
        print("💡 按 Ctrl+C 停止\n")
        
        async def _run():
            tasks = []
            for task in self.tasks.values():
                async def _task_loop(t=task):
                    while True:
                        try:
                            t["func"]()
                        except Exception as e:
                            print(f"❌ {t['name']}: {e}")
                        await asyncio.sleep(t["interval"])
                
                tasks.append(asyncio.create_task(_task_loop()))
            
            if duration:
                await asyncio.wait_for(asyncio.gather(*tasks), timeout=duration)
            else:
                await asyncio.gather(*tasks)
        
        try:
            asyncio.run(_run())
        except asyncio.TimeoutError:
            print(f"\n⏹️  运行 {duration} 秒，已停止")
        except KeyboardInterrupt:
            print("\n⏹️  已停止")


# ========== 内置示例任务 ==========

def demo_check_website():
    """示例：检查网站"""
    print("🌐 检查网站状态... OK")

def demo_check_database():
    """示例：检查数据库"""
    print("🗄️  检查数据库... OK")

def demo_generate_report():
    """示例：生成报告"""
    print("📊 生成报告... 完成")

def demo_clean_cache():
    """示例：清理缓存"""
    print("🧹 清理缓存... 完成")


def main():
    """主函数 - 处理命令行参数"""
    parser = argparse.ArgumentParser(
        description="AgentTaskSystem CLI - 任务调度工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python agent_cli.py demo          运行演示
  python agent_cli.py run 30        运行30秒
  python agent_cli.py list          列出任务
        """
    )
    
    parser.add_argument(
        "command",
        choices=["demo", "run", "list", "help"],
        help="命令: demo(演示), run(运行), list(列表)"
    )
    
    parser.add_argument(
        "duration",
        nargs="?",
        type=int,
        default=None,
        help="运行时长(秒)，不填则一直运行"
    )
    
    args = parser.parse_args()
    
    # 创建 CLI
    cli = AgentCLI()
    
    if args.command == "demo":
        # 演示模式
        print("\n" + "🎯"*20)
        print("  AgentTaskSystem CLI 演示")
        print("🎯"*20 + "\n")
        
        # 添加演示任务
        cli.add_task("网站检查", 3, demo_check_website)
        cli.add_task("数据库检查", 5, demo_check_database)
        cli.add_task("生成报告", 8, demo_generate_report)
        cli.add_task("清理缓存", 10, demo_clean_cache)
        
        # 运行
        cli.run_all(args.duration or 20)
        
    elif args.command == "run":
        # 运行模式（需要先添加任务）
        print("\n🚀 运行模式")
        print("💡 请先编辑 agent_cli.py 添加你的任务\n")
        
        # 这里可以加载用户自定义任务
        # cli.add_task("你的任务", 10, your_function)
        # cli.run_all(args.duration)
        
    elif args.command == "list":
        # 列表模式
        cli.list_tasks()
        
    elif args.command == "help":
        parser.print_help()


if __name__ == "__main__":
    main()
