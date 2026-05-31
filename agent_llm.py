#!/usr/bin/env python3
"""
🤖 AgentTaskSystem + LLM 服务！
让 Agent 拥有大模型能力！
"""

import json
import asyncio
import argparse
from typing import Dict, List, Optional
from datetime import datetime


class LLMService:
    """
    LLM 服务模拟器
    实际使用时可替换为真实 API 调用
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.model = config.get("model", "gpt-3.5-turbo")
        self.temperature = config.get("temperature", 0.7)
        self.max_tokens = config.get("max_tokens", 1000)
        self.prompt = config.get("prompt", "")
    
    async def chat(self, message: str) -> str:
        """对话"""
        # 模拟 LLM 响应
        await asyncio.sleep(0.5)
        
        responses = {
            "你好": "你好！我是AI助手，有什么可以帮你的？",
            "总结": f"{self.prompt}\n\n[这是模拟的总结内容]",
            "翻译": f"{self.prompt}\n\n[这是模拟的翻译结果]",
            "代码": f"{self.prompt}\n\n[这是模拟的代码审查意见]",
            "分析": f"{self.prompt}\n\n[这是模拟的数据分析结果]",
        }
        
        # 根据 prompt 匹配响应
        for key, response in responses.items():
            if key in self.prompt or key in message:
                return response
        
        return f"🤖 [{self.model}] 收到消息: {message}\n这是模拟的AI响应。"
    
    async def summarize(self, text: str) -> str:
        """摘要"""
        await asyncio.sleep(0.3)
        return f"📝 摘要:\n{text[:50]}...\n[这是AI生成的摘要内容]"
    
    async def translate(self, text: str, target_lang: str = "中文") -> str:
        """翻译"""
        await asyncio.sleep(0.3)
        return f"🌐 翻译为{target_lang}:\n{text}\n[这是AI翻译结果]"
    
    async def code_review(self, code: str) -> str:
        """代码审查"""
        await asyncio.sleep(0.5)
        return f"💻 代码审查:\n```\n{code[:100]}\n```\n[这是AI的代码审查意见]"
    
    async def analyze(self, data: str) -> str:
        """数据分析"""
        await asyncio.sleep(0.4)
        return f"📊 数据分析:\n{data[:100]}\n[这是AI的数据分析结果]"


class LLMAgent:
    """LLM Agent"""
    
    def __init__(self, config_file: str = "agent_config_llm.json"):
        self.config_file = config_file
        self.tasks: List[Dict] = []
        self.llm_services: Dict[str, LLMService] = {}
        self.load_config()
    
    def load_config(self):
        """加载配置"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                self.tasks = config.get("tasks", [])
            
            # 初始化 LLM 服务
            for task in self.tasks:
                if task.get("type") == "llm":
                    llm_config = task.get("llm_config", {})
                    self.llm_services[task["name"]] = LLMService(llm_config)
            
            print(f"✅ 加载 LLM 配置: {self.config_file}")
            print(f"📋 发现 {len(self.tasks)} 个任务")
            print(f"🤖 初始化 {len(self.llm_services)} 个 LLM 服务\n")
            
        except FileNotFoundError:
            print(f"❌ 配置文件不存在: {self.config_file}")
        except json.JSONDecodeError:
            print(f"❌ 配置文件格式错误")
    
    def list_services(self):
        """列出 LLM 服务"""
        print("\n🤖 LLM 服务列表:")
        print("-" * 60)
        print(f"{'名称':<20} {'描述':<20} {'模型':<15}")
        print("-" * 60)
        
        for task in self.tasks:
            if task.get("type") == "llm":
                llm_config = task.get("llm_config", {})
                model = llm_config.get("model", "unknown")
                print(f"{task['name']:<20} {task['description']:<20} {model:<15}")
        
        print("-" * 60)
    
    async def call_service(self, service_name: str, input_text: str) -> str:
        """调用 LLM 服务"""
        if service_name not in self.llm_services:
            return f"❌ 找不到服务: {service_name}"
        
        service = self.llm_services[service_name]
        
        print(f"\n🚀 调用 LLM 服务: {service_name}")
        print(f"📤 输入: {input_text[:50]}...")
        print("⏳ 处理中...")
        
        # 根据服务类型调用不同方法
        if "summary" in service_name:
            result = await service.summarize(input_text)
        elif "translate" in service_name:
            result = await service.translate(input_text)
        elif "code" in service_name:
            result = await service.code_review(input_text)
        elif "analysis" in service_name:
            result = await service.analyze(input_text)
        else:
            result = await service.chat(input_text)
        
        print(f"📥 结果:\n{result}")
        return result
    
    async def interactive_chat(self, service_name: str = "llm_chat"):
        """交互式对话"""
        print(f"\n🤖 进入交互模式 (服务: {service_name})")
        print("💡 输入 'exit' 退出\n")
        
        while True:
            try:
                user_input = input("你: ").strip()
                
                if user_input.lower() in ["exit", "quit", "退出"]:
                    print("👋 再见！")
                    break
                
                if not user_input:
                    continue
                
                result = await self.call_service(service_name, user_input)
                
            except KeyboardInterrupt:
                print("\n👋 再见！")
                break
            except EOFError:
                break
    
    async def run_scheduled_tasks(self, duration: int = None):
        """运行定时 LLM 任务"""
        scheduled_tasks = [t for t in self.tasks 
                          if t.get("type") == "llm" and t.get("interval", 0) > 0]
        
        if not scheduled_tasks:
            print("📭 没有定时 LLM 任务")
            return
        
        print(f"\n🚀 启动 {len(scheduled_tasks)} 个定时 LLM 任务...")
        if duration:
            print(f"⏱️  运行时长: {duration} 秒")
        print("💡 按 Ctrl+C 停止\n")
        
        async def _run_task(task):
            service_name = task["name"]
            interval = task["interval"]
            
            while True:
                try:
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    print(f"[{timestamp}] 执行: {task['description']}")
                    
                    # 模拟定时任务输入
                    sample_input = f"这是定时任务 {task['name']} 的示例输入"
                    await self.call_service(service_name, sample_input)
                    
                except Exception as e:
                    print(f"❌ 任务失败: {e}")
                
                await asyncio.sleep(interval)
        
        try:
            coroutines = [_run_task(task) for task in scheduled_tasks]
            
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
        description="AgentTaskSystem + LLM 服务",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 列出 LLM 服务
  python agent_llm.py list
  
  # 交互式对话
  python agent_llm.py chat
  
  # 调用特定服务
  python agent_llm.py call llm_summary "请总结这篇文章..."
  
  # 运行定时任务
  python agent_llm.py run --time 60
        """
    )
    
    parser.add_argument(
        "--config",
        default="agent_config_llm.json",
        help="配置文件路径"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # list 命令
    subparsers.add_parser("list", help="列出服务")
    
    # chat 命令
    chat_parser = subparsers.add_parser("chat", help="交互式对话")
    chat_parser.add_argument("--service", default="llm_chat", help="服务名称")
    
    # call 命令
    call_parser = subparsers.add_parser("call", help="调用服务")
    call_parser.add_argument("service", help="服务名称")
    call_parser.add_argument("input", help="输入文本")
    
    # run 命令
    run_parser = subparsers.add_parser("run", help="运行定时任务")
    run_parser.add_argument("--time", type=int, help="运行时长(秒)")
    
    args = parser.parse_args()
    
    # 创建 Agent
    agent = LLMAgent(args.config)
    
    if args.command == "list":
        agent.list_services()
        
    elif args.command == "chat":
        asyncio.run(agent.interactive_chat(args.service))
        
    elif args.command == "call":
        asyncio.run(agent.call_service(args.service, args.input))
        
    elif args.command == "run":
        asyncio.run(agent.run_scheduled_tasks(args.time))
        
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
