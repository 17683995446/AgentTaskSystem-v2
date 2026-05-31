#!/usr/bin/env python3
"""
🖥️ AgentTaskSystem CLI v2.0
更强大的命令行工具！
"""

import sys
import time
import asyncio
import argparse
import json
from typing import Callable, Dict
from datetime import datetime


class AgentCLIv2:
    """增强版 CLI"""
    
    def __init__(self):
        self.tasks: Dict = {}
        self.task_counter = 0
        self.stats = {"started": 0, "completed": 0, "failed": 0}
    
    def add(self, name: str, interval: int, func: Callable, task_type: str = "scheduled"):
        """添加任务"""
        self.task_counter += 1
        task_id = f"task_{self.task_counter}"
        self.tasks[task_id] = {
            "id": task_id,
            "name": name,
            "interval": interval,
            "func": func,
            "type": task_type,
            "run_count": 0,
            "last_run": None,
            "status": "ready"
        }
        return task_id
    
    def status(self):
        """显示状态"""
        print("\n📊 Agent 状态")
        print("=" * 50)
        print(f"  任务总数: {len(self.tasks)}")
        print(f"  已启动: {self.stats['started']}")
        print(f"  已完成: {self.stats['completed']}")
        print(f"  失败: {self.stats['failed']}")
        print("=" * 50)
        
        if self.tasks:
            print("\n📋 任务详情:")
            for tid, task in self.tasks.items():
                status_icon = "🟢" if task['status'] == "running" else "⚪"
                print(f"  {status_icon} {task['name']} "
                      f"(每{task['interval']}s, 运行{task['run_count']}次)")
    
    def run(self, duration: int = None, task_filter: str = None):
        """运行任务"""
        if not self.tasks:
            print("❌ 没有任务")
            return
        
        # 过滤任务
        run_tasks = self.tasks
        if task_filter:
            run_tasks = {k: v for k, v in self.tasks.items() 
                        if task_filter.lower() in v['name'].lower()}
        
        print(f"\n🚀 启动 {len(run_tasks)} 个任务...")
        if duration:
            print(f"⏱️  运行时长: {duration} 秒")
        print("💡 按 Ctrl+C 停止\n")
        
        async def _run():
            tasks = []
            for task in run_tasks.values():
                task['status'] = "running"
                self.stats['started'] += 1
                
                async def _loop(t=task):
                    while t['status'] == "running":
                        try:
                            t['func']()
                            t['run_count'] += 1
                            t['last_run'] = datetime.now().strftime("%H:%M:%S")
                            self.stats['completed'] += 1
                        except Exception as e:
                            print(f"❌ {t['name']}: {e}")
                            self.stats['failed'] += 1
                        
                        await asyncio.sleep(t['interval'])
                
                tasks.append(asyncio.create_task(_loop()))
            
            if duration:
                await asyncio.wait_for(asyncio.gather(*tasks), timeout=duration)
            else:
                await asyncio.gather(*tasks)
        
        try:
            asyncio.run(_run())
        except asyncio.TimeoutError:
            print(f"\n⏹️  运行 {duration} 秒完成")
        except KeyboardInterrupt:
            print("\n⏹️  用户停止")
            for task in self.tasks.values():
                task['status'] = "stopped"


# ========== 内置任务库 ==========

def task_website_check():
    """检查网站"""
    print(f"🌐 [{datetime.now().strftime('%H:%M:%S')}] 网站检查... OK")

def task_database_check():
    """检查数据库"""
    print(f"🗄️  [{datetime.now().strftime('%H:%M:%S')}] 数据库检查... OK")

def task_generate_report():
    """生成报告"""
    print(f"📊 [{datetime.now().strftime('%H:%M:%S')}] 生成报告... 完成")

def task_clean_logs():
    """清理日志"""
    print(f"🧹 [{datetime.now().strftime('%H:%M:%S')}] 清理日志... 完成")

def task_backup_data():
    """备份数据"""
    print(f"💾 [{datetime.now().strftime('%H:%M:%S')}] 备份数据... 完成")


# 任务注册表
TASK_REGISTRY = {
    "website": ("网站检查", 5, task_website_check),
    "database": ("数据库检查", 10, task_database_check),
    "report": ("生成报告", 30, task_generate_report),
    "clean": ("清理日志", 60, task_clean_logs),
    "backup": ("备份数据", 300, task_backup_data),
}


def main():
    parser = argparse.ArgumentParser(
        description="AgentTaskSystem CLI v2.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 运行演示（所有内置任务）
  python agent_cli_v2.py demo
  
  # 运行特定任务
  python agent_cli_v2.py run website database
  
  # 运行30秒
  python agent_cli_v2.py run --time 30 website
  
  # 查看状态
  python agent_cli_v2.py status
  
可用任务:
  website   - 网站检查 (每5秒)
  database  - 数据库检查 (每10秒)
  report    - 生成报告 (每30秒)
  clean     - 清理日志 (每60秒)
  backup    - 备份数据 (每5分钟)
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # demo 命令
    demo_parser = subparsers.add_parser("demo", help="运行演示")
    demo_parser.add_argument("--time", type=int, default=30, help="运行时长(秒)")
    
    # run 命令
    run_parser = subparsers.add_parser("run", help="运行任务")
    run_parser.add_argument("tasks", nargs="+", help="任务名称")
    run_parser.add_argument("--time", type=int, help="运行时长(秒)")
    
    # status 命令
    status_parser = subparsers.add_parser("status", help="查看状态")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    cli = AgentCLIv2()
    
    if args.command == "demo":
        # 演示模式 - 加载所有任务
        print("\n" + "🚀"*20)
        print("  AgentTaskSystem CLI v2.0")
        print("  演示模式")
        print("🚀"*20 + "\n")
        
        for key, (name, interval, func) in TASK_REGISTRY.items():
            cli.add(name, interval, func)
        
        cli.status()
        cli.run(args.time)
        
    elif args.command == "run":
        # 运行指定任务
        print(f"\n🚀 运行任务: {', '.join(args.tasks)}\n")
        
        for task_name in args.tasks:
            if task_name in TASK_REGISTRY:
                name, interval, func = TASK_REGISTRY[task_name]
                cli.add(name, interval, func)
            else:
                print(f"⚠️  未知任务: {task_name}")
        
        if cli.tasks:
            cli.run(args.time)
        else:
            print("❌ 没有有效任务")
            
    elif args.command == "status":
        cli.status()


if __name__ == "__main__":
    main()
