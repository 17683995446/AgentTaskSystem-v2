# AgentTaskSystem - AI可强制执行·严格二叉树层级模块化工程

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-10%20passed-brightgreen)](tests/)

AgentTaskSystem 是一个严格遵循二叉树层级模块化架构的智能任务调度系统，支持插件化扩展、AI大模型集成、可视化监控和多种任务执行模式。

## 核心特性

- **严格二叉树架构** - 所有非叶子节点严格有2个子模块
- **插件化扩展** - 内置6种开源工具插件，支持自定义扩展
- **AI大模型集成** - 已接入硅基流动(SiliconFlow)免费模型
- **可视化监控** - DataVista Pro 数据大屏
- **多种API接口** - 极简API、装饰器模式、CLI命令行
- **断点续跑** - 任务失败自动重试，支持快照恢复

## 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 运行核心系统演示
python main.py

# 运行插件演示
python agent_plugins_demo.py

# 使用AI对话
python agent_siliconflow.py ask "你好"

# 运行测试
python -m pytest tests/ -v
```

## 系统架构

```
AgentTaskSystem (Root)
├── TaskCore
│   ├── TaskDefine (任务定义)
│   └── TaskState (状态管理)
├── AgentRuntime
│   ├── TaskSchedule (任务调度)
│   └── TaskRunner (任务执行)
└── PluginManager (插件管理)
    ├── requests_http (HTTP请求)
    ├── beautifulsoup_scraper (网页抓取)
    ├── pandas_data (数据处理)
    ├── selenium_browser (浏览器自动化)
    ├── schedule_timer (定时任务)
    └── email_sender (邮件发送)
```

## 插件系统

| 插件 | 功能 | 依赖 |
|------|------|------|
| requests_http | HTTP请求、API调用 | requests |
| beautifulsoup_scraper | 网页解析、数据提取 | beautifulsoup4 |
| pandas_data | 数据分析、CSV/Excel处理 | pandas |
| selenium_browser | 网页截图、表单自动化 | selenium |
| schedule_timer | 定时任务、循环执行 | schedule |
| email_sender | SMTP邮件通知 | smtplib |

## AI大模型支持

已接入硅基流动(SiliconFlow)免费模型：
- Qwen/Qwen3.6-27B (默认)
- deepseek-ai/DeepSeek-V4-Flash
- THUDM/glm-4-9b-chat

```bash
# 单次对话
python agent_siliconflow.py ask "你好"

# 交互式对话
python agent_siliconflow.py chat

# 列出所有模型
python agent_siliconflow.py models
```

## 测试

```bash
# 运行所有测试
python -m pytest tests/ -v

# 测试核心系统
python -m pytest tests/test_core_system.py -v

# 测试插件系统
python -m pytest tests/test_plugins.py -v
```

## 项目结构

```
.
├── AgentTaskSystem/          # 核心系统
│   ├── TaskCore/              # 任务核心
│   ├── AgentRuntime/          # 运行时
│   ├── PluginManager/         # 插件管理
│   └── simple_api.py          # 简单API
├── DataVistaPro/              # 可视化系统
│   ├── web-frontend/          # 前端页面
│   └── AgentTasks/            # 任务模块
├── tests/                     # 测试用例
├── main.py                    # 主入口
├── agent_siliconflow.py       # AI集成
├── agent_plugins_demo.py      # 插件演示
├── requirements.txt           # 依赖
└── setup.py                   # 安装配置
```

## 规范遵循

- 二叉树架构: 所有非叶子节点严格有2个子模块
- 接口隔离: 跨模块只访问interfaces，不直接访问impl
- 命名规范: 文件有效单词数与所在层级匹配
- 单一职责: 每个模块/类功能单一明确

## License

MIT License
