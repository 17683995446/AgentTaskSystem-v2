#!/usr/bin/env python3
"""
🤖 AgentTaskSystem + 硅基流动 API！
使用真实的大模型服务！
"""

import json
import asyncio
import argparse
import requests
from typing import Dict, List
from datetime import datetime


class SiliconFlowAPI:
    """
    硅基流动 API 客户端
    官网: https://siliconflow.cn
    """

    # 推荐的免费模型列表（已验证可用）
    FREE_MODELS = [
        "Qwen/Qwen3.6-27B",
        "Qwen/Qwen3.6-35B-A3B",
        "deepseek-ai/DeepSeek-V4-Flash",
        "THUDM/glm-4-9b-chat",
    ]

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.siliconflow.cn/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def chat(self, message: str, model: str = None) -> str:
        """
        调用聊天接口

        可用免费模型:
        - Qwen/Qwen3.6-27B
        - Qwen/Qwen3.6-35B-A3B
        - deepseek-ai/DeepSeek-V4-Flash
        - THUDM/glm-4-9b-chat
        """
        if model is None:
            model = self.FREE_MODELS[0]
        try:
            url = f"{self.base_url}/chat/completions"
            
            data = {
                "model": model,
                "messages": [
                    {"role": "system", "content": "你是一个 helpful 的AI助手。"},
                    {"role": "user", "content": message}
                ],
                "stream": False,
                "max_tokens": 1024,
                "temperature": 0.7
            }
            
            response = requests.post(url, headers=self.headers, json=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
            
        except requests.exceptions.RequestException as e:
            return f"❌ API 请求失败: {e}"
        except (KeyError, IndexError) as e:
            return f"❌ 解析响应失败: {e}"
        except Exception as e:
            return f"❌ 未知错误: {e}"
    
    def list_models(self) -> List[str]:
        """列出可用模型"""
        try:
            url = f"{self.base_url}/models"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            models = [model["id"] for model in result.get("data", [])]
            return models
            
        except Exception as e:
            print(f"❌ 获取模型列表失败: {e}")
            return []


class SiliconFlowAgent:
    """硅基流动 Agent"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.api = SiliconFlowAPI(api_key)
        print("✅ 硅基流动 Agent 初始化完成！")

    def chat(self, message: str, model: str = None):
        """单次对话"""
        print(f"\n🚀 发送请求到硅基流动...")
        print(f"📝 输入: {message[:50]}...")
        print("⏳ 等待响应...\n")
        
        result = self.api.chat(message, model)
        
        print("📥 响应:")
        print("-" * 60)
        print(result)
        print("-" * 60)
        
        return result
    
    def interactive_chat(self, model: str = None):
        """交互式对话"""
        if model is None:
            model = SiliconFlowAPI.FREE_MODELS[0]
        print(f"\n🤖 进入交互模式 (模型: {model})")
        print("💡 输入 'exit' 退出，输入 'model' 切换模型\n")
        
        while True:
            try:
                user_input = input("你: ").strip()
                
                if user_input.lower() in ["exit", "quit", "退出"]:
                    print("👋 再见！")
                    break
                
                if not user_input:
                    continue
                
                self.chat(user_input, model)
                
            except KeyboardInterrupt:
                print("\n👋 再见！")
                break
            except EOFError:
                break
    
    def batch_process(self, tasks: List[Dict], model: str = None):
        """批量处理任务"""
        if model is None:
            model = SiliconFlowAPI.FREE_MODELS[0]
        print(f"\n🚀 批量处理 {len(tasks)} 个任务...\n")
        
        results = []
        for i, task in enumerate(tasks, 1):
            print(f"[{i}/{len(tasks)}] 处理: {task['name']}")
            result = self.api.chat(task["prompt"], model)
            results.append({
                "name": task["name"],
                "result": result
            })
            print(f"✅ 完成\n")
        
        return results
    
    def list_models(self):
        """列出可用模型"""
        print("\n🤖 获取可用模型列表...")
        models = self.api.list_models()
        
        if models:
            print(f"\n📋 可用模型 ({len(models)} 个):")
            print("-" * 60)
            for model in models[:20]:  # 只显示前20个
                print(f"  • {model}")
            if len(models) > 20:
                print(f"  ... 还有 {len(models) - 20} 个")
            print("-" * 60)
        else:
            print("❌ 无法获取模型列表")
        
        return models


# 预设任务模板
TASK_TEMPLATES = {
    "summary": {
        "name": "文本摘要",
        "prompt": "请对以下内容进行摘要，提取关键信息：\n\n{content}"
    },
    "translate": {
        "name": "翻译",
        "prompt": "请将以下内容翻译成中文：\n\n{content}"
    },
    "code_review": {
        "name": "代码审查",
        "prompt": "请审查以下代码，指出潜在问题并给出改进建议：\n\n```\n{content}\n```"
    },
    "explain": {
        "name": "解释说明",
        "prompt": "请用通俗易懂的语言解释以下内容：\n\n{content}"
    },
    "generate": {
        "name": "内容生成",
        "prompt": "请根据以下要求生成内容：\n\n{content}"
    }
}


def main():
    parser = argparse.ArgumentParser(
        description="AgentTaskSystem + 硅基流动 API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 交互式对话
  python agent_siliconflow.py chat
  
  # 单次对话
  python agent_siliconflow.py ask "你好，请介绍一下自己"
  
  # 使用特定模型
  python agent_siliconflow.py --model Qwen/Qwen2.5-7B-Instruct ask "你好"
  
  # 批量处理文件
  python agent_siliconflow.py batch input.txt
  
  # 列出可用模型
  python agent_siliconflow.py models

可用免费模型:
  Qwen/Qwen3.6-27B             (推荐)
  Qwen/Qwen3.6-35B-A3B
  deepseek-ai/DeepSeek-V4-Flash
  THUDM/glm-4-9b-chat
        """
    )
    
    parser.add_argument(
        "--api-key",
        default="sk-uqelhavcdhfxjzjesdenxpbtqombamjniazzjtbssmdcwdvg",
        help="API Key"
    )
    
    parser.add_argument(
        "--model",
        default=None,
        help="模型名称 (默认: Qwen/Qwen3.6-27B)"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # chat 命令
    subparsers.add_parser("chat", help="交互式对话")
    
    # ask 命令
    ask_parser = subparsers.add_parser("ask", help="单次对话")
    ask_parser.add_argument("message", help="消息内容")
    
    # batch 命令
    batch_parser = subparsers.add_parser("batch", help="批量处理")
    batch_parser.add_argument("file", help="输入文件")
    batch_parser.add_argument("--template", default="summary", choices=TASK_TEMPLATES.keys(),
                             help="任务模板")
    
    # models 命令
    subparsers.add_parser("models", help="列出可用模型")
    
    args = parser.parse_args()
    
    # 创建 Agent
    agent = SiliconFlowAgent(args.api_key)
    
    if args.command == "chat":
        agent.interactive_chat(args.model)
        
    elif args.command == "ask":
        agent.chat(args.message, args.model)
        
    elif args.command == "batch":
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            template = TASK_TEMPLATES[args.template]
            prompt = template["prompt"].format(content=content)
            
            tasks = [{"name": template["name"], "prompt": prompt}]
            agent.batch_process(tasks, args.model)
            
        except FileNotFoundError:
            print(f"❌ 文件不存在: {args.file}")
        except Exception as e:
            print(f"❌ 处理失败: {e}")
            
    elif args.command == "models":
        agent.list_models()
        
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
