"""
🚀 AgentTaskSystem 超简单示例！
复制粘贴就能运行！
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

from AgentTaskSystem.simple_api import SimpleAgent, quick_start


# ========== 示例 1：最最简单的用法 ==========
def example_1_basic():
    print("\n" + "="*60)
    print("  示例 1：最最简单的用法")
    print("="*60)
    
    # 1. 创建 Agent（就这一行！）
    agent = SimpleAgent()
    
    # 2. 写你的任务（普通函数就行！）
    def hello_world():
        print("👋 Hello, AgentTaskSystem!")
        return "成功了！"
    
    # 3. 运行任务（就这一行！）
    task_id = agent.create_and_run("我的第一个任务", hello_world)
    
    # 4. 看看状态
    print(f"📋 任务 ID: {task_id}")
    print(f"✅ 完成！")


# ========== 示例 2：模拟数据采集 ==========
def example_2_data_collect():
    print("\n" + "="*60)
    print("  示例 2：模拟数据采集")
    print("="*60)
    
    agent = SimpleAgent()
    
    # 你的数据采集逻辑
    def collect_data():
        print("📊 开始采集数据...")
        
        # 模拟采集过程
        print("   步骤 1/3: 连接数据库...")
        import time
        time.sleep(0.5)
        
        print("   步骤 2/3: 读取数据...")
        time.sleep(0.5)
        
        print("   步骤 3/3: 处理数据...")
        time.sleep(0.5)
        
        print("✅ 数据采集成功！")
        return {"count": 100, "status": "success"}
    
    # 运行！
    agent.create_and_run("每日数据采集", collect_data)


# ========== 示例 3：多个任务一起 ==========
def example_3_multiple_tasks():
    print("\n" + "="*60)
    print("  示例 3：多个任务一起运行")
    print("="*60)
    
    agent = SimpleAgent()
    
    # 任务 1
    def task_1():
        print("📈 生成销售报表...")
        import time
        time.sleep(0.3)
        print("✅ 销售报表完成")
    
    # 任务 2
    def task_2():
        print("📊 生成用户报表...")
        import time
        time.sleep(0.3)
        print("✅ 用户报表完成")
    
    # 任务 3
    def task_3():
        print("📉 生成库存报表...")
        import time
        time.sleep(0.3)
        print("✅ 库存报表完成")
    
    # 全部运行！
    print("\n🚀 开始运行 3 个任务...\n")
    
    agent.create_and_run("销售报表", task_1)
    agent.create_and_run("用户报表", task_2)
    agent.create_and_run("库存报表", task_3)
    
    print("\n✅ 所有任务已启动！")


# ========== 示例 4：管理任务 ==========
def example_4_manage_tasks():
    print("\n" + "="*60)
    print("  示例 4：任务管理（查看、暂停、停止）")
    print("="*60)
    
    agent = SimpleAgent()
    
    # 创建一个任务
    def long_task():
        import time
        for i in range(5):
            print(f"⏳ 任务进行中... {i+1}/5")
            time.sleep(0.5)
        print("✅ 长时间任务完成！")
    
    task_id = agent.create_task("长时间任务")
    print(f"📋 任务创建: {task_id}")
    
    # 查看所有任务
    print("\n📋 所有任务:")
    tasks = agent.list_tasks()
    for task in tasks:
        print(f"  - {task['name']} (状态: {task.get('status', 'unknown')})")
    
    # 运行任务
    print("\n🚀 启动任务...")
    agent.run_task(task_id, long_task)


# ========== 主函数：运行所有示例 ==========
def main():
    print("\n" + "🚀"*30)
    print("  AgentTaskSystem - 超简单示例集合")
    print("🚀"*30)
    
    # 运行所有示例
    example_1_basic()
    example_2_data_collect()
    example_3_multiple_tasks()
    example_4_manage_tasks()
    
    print("\n" + "="*60)
    print("  🎉 所有示例运行完成！")
    print("="*60)
    print("\n💡 提示:")
    print("  1. 复制上面的代码，改改就能用！")
    print("  2. 把你的业务逻辑写成普通函数")
    print("  3. 用 agent.create_and_run() 直接运行！")
    print("  4. 就这么简单！")


if __name__ == "__main__":
    main()
