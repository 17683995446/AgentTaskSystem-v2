#!/usr/bin/env python3
"""
AgentTaskSystem 插件系统演示
展示如何使用各种开源工具插件
"""

import json
from AgentTaskSystem.PluginManager import create_plugin_manager
from AgentTaskSystem.PluginManager.plugins import (
    RequestsPlugin,
    BeautifulSoupPlugin,
    PandasPlugin,
    SchedulePlugin,
    EmailPlugin
)


def demo_requests_plugin():
    """演示 HTTP请求插件 """
    print("\n" + "="*60)
    print("  RequestsPlugin - HTTP请求插件演示")
    print("="*60)

    manager = create_plugin_manager()
    plugin = RequestsPlugin()

    # 注册插件
    manager.register_plugin(plugin)

    # 1. GET 请求示例
    print("\n🌐 1. GET请求 httpbin.org")
    result = manager.execute_plugin("requests_http", {
        "method": "GET",
        "url": "https://httpbin.org/get",
        "params": {"foo": "bar"}
    })
    print(f"状态码: {result['result'].get('status_code')}")
    print(f"响应预览: {json.dumps(result['result'].get('json', {}), indent=2)[:200]}...")

    # 2. POST 请求示例
    print("\n📤 2. POST请求")
    result = manager.execute_plugin("requests_http", {
        "method": "POST",
        "url": "https://httpbin.org/post",
        "data": {"name": "AgentTaskSystem", "version": "1.0"}
    })
    print(f"状态码: {result['result'].get('status_code')}")

    manager.shutdown_all()


def demo_bs4_plugin():
    """演示 网页解析插件 """
    print("\n" + "="*60)
    print("  BeautifulSoupPlugin - 网页解析插件演示")
    print("="*60)

    manager = create_plugin_manager()
    plugin = BeautifulSoupPlugin()

    manager.register_plugin(plugin)

    # 抓取网页并提取文本
    print("\n🕷️ 抓取示例网页")
    result = manager.execute_plugin("beautifulsoup_scraper", {
        "action": "scrape",
        "url": "https://httpbin.org/html",
        "selector": "h1"
    })

    if result["success"]:
        print(f"标题: {result['result'].get('title', 'N/A')}")
        print(f"找到元素数: {result['result'].get('count', 0)}")
        if result['result'].get('elements'):
            print(f"内容: {result['result']['elements'][0][:100]}...")

    manager.shutdown_all()


def demo_pandas_plugin():
    """演示 数据处理插件 """
    print("\n" + "="*60)
    print("  PandasPlugin - 数据处理插件演示")
    print("="*60)

    manager = create_plugin_manager()
    plugin = PandasPlugin()

    manager.register_plugin(plugin)

    # 数据分析示例
    print("\n📊 数据分析")
    sample_data = [
        {"name": "产品A", "sales": 100, "price": 50},
        {"name": "产品B", "sales": 150, "price": 30},
        {"name": "产品C", "sales": 80, "price": 70},
        {"name": "产品A", "sales": 120, "price": 50},
        {"name": "产品B", "sales": 90, "price": 30}
    ]

    result = manager.execute_plugin("pandas_data", {
        "action": "analyze",
        "data": sample_data
    })

    if result["success"]:
        print(f"数据形状: {result['result'].get('shape')}")
        print(f"列名: {result['result'].get('columns')}")
        print(f"统计摘要: {json.dumps(result['result'].get('describe', {}), indent=2)[:300]}...")

    # 数据聚合
    print("\n📈 按产品名称聚合销售数据")
    result = manager.execute_plugin("pandas_data", {
        "action": "aggregate",
        "data": sample_data,
        "group_by": "name",
        "agg_func": "sum"
    })

    if result["success"]:
        print(f"聚合结果: {json.dumps(result['result'].get('result', []), indent=2)}")

    manager.shutdown_all()


def demo_schedule_plugin():
    """演示 定时任务插件 """
    print("\n" + "="*60)
    print("  SchedulePlugin - 定时任务插件演示")
    print("="*60)

    manager = create_plugin_manager()
    plugin = SchedulePlugin()

    manager.register_plugin(plugin)

    # 添加定时任务
    print("\n⏰ 添加定时任务")
    result = manager.execute_plugin("schedule_timer", {
        "action": "add_job",
        "job_id": "heartbeat",
        "interval": 2,
        "unit": "seconds"
    })
    print(f"添加结果: {result}")

    # 列出任务
    result = manager.execute_plugin("schedule_timer", {
        "action": "list_jobs"
    })
    print(f"任务列表: {json.dumps(result, indent=2)}")

    manager.shutdown_all()


def demo_all_plugins():
    """展示所有可用插件 """
    print("\n" + "="*60)
    print("  所有可用插件列表")
    print("="*60)

    plugins = [
        ("requests_http", "HTTP请求", "requests", "网络请求、API调用"),
        ("beautifulsoup_scraper", "网页抓取", "beautifulsoup4", "网页解析、数据提取"),
        ("pandas_data", "数据处理", "pandas", "CSV/Excel处理、数据分析"),
        ("selenium_browser", "浏览器自动化", "selenium", "网页截图、表单操作"),
        ("schedule_timer", "定时任务", "schedule", "定时执行、循环任务"),
        ("email_sender", "邮件发送", "smtplib", "SMTP邮件通知"),
    ]

    print("\n📦 内置插件清单:")
    print("-" * 60)
    for name, desc, dep, usage in plugins:
        print(f"  🔌 {name}")
        print(f"     功能: {desc}")
        print(f"     依赖: {dep}")
        print(f"     用途: {usage}")
        print()


def main():
    """主函数 - 运行所有演示"""
    print("\n" + "🚀"*30)
    print("  AgentTaskSystem 插件系统演示")
    print("  展示如何集成各种开源工具")
    print("🚀"*30)

    # 显示所有插件
    demo_all_plugins()

    # 运行各个插件演示
    try:
        demo_requests_plugin()
    except Exception as e:
        print(f"⚠️ Requests插件演示出错: {e}")

    try:
        demo_bs4_plugin()
    except Exception as e:
        print(f"⚠️ BeautifulSoup插件演示出错: {e}")

    try:
        demo_pandas_plugin()
    except Exception as e:
        print(f"⚠️ Pandas插件演示出错: {e}")

    try:
        demo_schedule_plugin()
    except Exception as e:
        print(f"⚠️ Schedule插件演示出错: {e}")

    print("\n" + "="*60)
    print("  演示完成！")
    print("="*60)
    print("""
💡 使用提示:

1. 注册插件:
   manager = create_plugin_manager()
   manager.register_plugin(RequestsPlugin())

2. 执行插件:
   result = manager.execute_plugin("requests_http", {
       "method": "GET",
       "url": "https://api.example.com"
   })

3. 查看所有插件:
   plugins = manager.list_plugins()

4. 系统会自动安装缺失的依赖！
    """)


if __name__ == "__main__":
    main()
