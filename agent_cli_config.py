#!/usr/bin/env python3
"""
🖥️ AgentTaskSystem CLI - 配置文件版！
不用改代码，改JSON配置就行！
"""

import json
import asyncio
import subprocess
import argparse
from datetime import datetime
from typing import Dict, List


class ConfigAgent:
    """配置版 Agent"""
    
    def __init__(self, config_file: str = "agent_config.json"):
        self.config_file = config_file
        self.tasks: List[Dict] = []
        self.load_config()
    
    def load_config(self):
        """加载配置文件"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                self.tasks = config.get("tasks", [])
            print(f"✅ 加载配置: {self.config_file}")
            print(f"📋 发现 {len(self.tasks)} 个任务\n")
        except FileNotFoundError:
            print(f"❌ 配置文件不存在: {self.config_file}")
            print("💡 创建默认配置...")
            self.create_default_config()
        except json.JSONDecodeError:
            print(f"❌ 配置文件格式错误")
    
    def create_default_config(self):
        """创建默认配置"""
        default_config = {
            "tasks": [
                {
                    "name": "hello",
                    "description": "示例任务",
                    "interval": 5,
                    "command": "echo '👋 Hello from Agent!'"
                }
            ]
        }
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=2, ensure_ascii=False)
        self.tasks = default_config["tasks"]
        print(f"✅ 已创建默认配置: {self.config_file}")
    
    def list_tasks(self):
        """列出所有任务"""
        if not self.tasks:
            print("📭 暂无任务")
            return
        
        print("\n📋 任务列表:")
        print("-" * 60)
        print(f"{'名称':<15} {'描述':<20} {'间隔':<10} {'命令'}")
        print("-" * 60)
        
        for task in self.tasks:
            print(f"{task['name']:<15} {task['description']:<20} "
                  f"{task['interval']}s{'':<5} {task['command'][:30]}...")
        print("-" * 60)
    
    def run_task(self, task_name: str):
        """执行单个任务"""
        for task in self.tasks:
            if task["name"] == task_name:
                try:
                    result = subprocess.run(
                        task["command"],
                        shell=True,
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    print(f"[{timestamp}] {task['description']}")
                    
                    if result.stdout:
                        print(result.stdout.strip())
                    if result.returncode != 0 and result.stderr:
                        print(f"⚠️  {result.stderr.strip()}")
                        
                    return True
                except Exception as e:
                    print(f"❌ 执行失败: {e}")
                    return False
        
        print(f"❌ 找不到任务: {task_name}")
        return False
    
    async def run_scheduled(self, task_name: str = None, duration: int = None):
        """定时运行任务"""
        tasks_to_run = self.tasks
        
        if task_name:
            tasks_to_run = [t for t in self.tasks if t["name"] == task_name]
            if not tasks_to_run:
                print(f"❌ 找不到任务: {task_name}")
                return
        
        print(f"\n🚀 启动 {len(tasks_to_run)} 个任务...")
        if duration:
            print(f"⏱️  运行时长: {duration} 秒")
        print("💡 按 Ctrl+C 停止\n")
        
        async def _run_task(task):
            """运行单个任务循环"""
            while True:
                self.run_task(task["name"])
                await asyncio.sleep(task["interval"])
        
        try:
            # 创建所有任务
            coroutines = [_run_task(task) for task in tasks_to_run]
            
            if duration:
                await asyncio.wait_for(
                    asyncio.gather(*coroutines),
                    timeout=duration
                )
            else:
                await asyncio.gather(*coroutines)
                
        except asyncio.TimeoutError:
            print(f"\n⏹️  运行 {duration} 秒完成")
        except KeyboardInterrupt:
            print("\n⏹️  用户停止")


def main():
    parser = argparse.ArgumentParser(
        description="AgentTaskSystem CLI - 配置文件版",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 列出所有任务
  python agent_cli_config.py list
  
  # 运行所有任务（演示）
  python agent_cli_config.py demo
  
  # 运行指定任务
  python agent_cli_config.py run website
  
  # 运行指定时间
  python agent_cli_config.py run --time 30 website
  
  # 使用其他配置文件
  python agent_cli_config.py --config my_config.json list
        """
    )
    
    parser.add_argument(
        "--config",
        default="agent_config.json",
        help="配置文件路径 (默认: agent_config.json)"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # list 命令
    list_parser = subparsers.add_parser("list", help="列出任务")
    
    # demo 命令
    demo_parser = subparsers.add_parser("demo", help="运行演示")
    demo_parser.add_argument("--time", type=int, default=20, help="运行时长(秒)")
    
    # run 命令
    run_parser = subparsers.add_parser("run", help="运行任务")
    run_parser.add_argument("task", nargs="?", help="任务名称")
    run_parser.add_argument("--time", type=int, help="运行时长(秒)")
    
    # once 命令（执行一次）
    once_parser = subparsers.add_parser("once", help="执行一次")
    once_parser.add_argument("task", help="任务名称")
    
    args = parser.parse_args()
    
    # 创建 Agent
    agent = ConfigAgent(args.config)
    
    if args.command == "list":
        agent.list_tasks()
        
    elif args.command == "demo":
        print("\n" + "🚀"*20)
        print("  AgentTaskSystem - 配置文件版")
        print("  演示模式")
        print("🚀"*20 + "\n")
        
        agent.list_tasks()
        asyncio.run(agent.run_scheduled(duration=args.time))
        
    elif args.command == "run":
        if args.task:
            print(f"\n🚀 运行任务: {args.task}\n")
            asyncio.run(agent.run_scheduled(args.task, args.time))
        else:
            print("\n🚀 运行所有任务\n")
            asyncio.run(agent.run_scheduled(duration=args.time))
            
    elif args.command == "once":
        print(f"\n🚀 执行一次: {args.task}\n")
        agent.run_task(args.task)
        
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
