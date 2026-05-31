"""
🎯 超简单的 AgentTaskSystem 接口演示！
这个文件独立运行，不依赖其他复杂模块
"""

import time
from typing import Callable, Any, Dict


class SimpleTask:
    """一个简单的任务类"""
    
    def __init__(self, task_id: str, name: str):
        self.task_id = task_id
        self.name = name
        self.status = "pending"
        self.created_at = time.time()
        self.result = None


class SimpleAgentAPI:
    """
    超简单的 Agent API！
    这是一个简化演示版，让你快速上手
    """
    
    def __init__(self):
        self.tasks: Dict[str, SimpleTask] = {}
        self._task_counter = 0
        print("✅ SimpleAgent 准备好了！")
    
    def create_task(self, name: str) -> str:
        """
        【1行代码】创建任务
        
        参数:
            name: 任务名称
            
        返回:
            task_id: 任务ID
            
        示例:
            agent = SimpleAgentAPI()
            task_id = agent.create_task("我的任务")
        """
        self._task_counter += 1
        task_id = f"task_{self._task_counter}"
        
        task = SimpleTask(task_id, name)
        self.tasks[task_id] = task
        
        print(f"✅ 任务创建成功: {name} (ID: {task_id})")
        return task_id
    
    def run_task(self, task_id: str, task_logic: Callable) -> Any:
        """
        【1行代码】运行任务
        
        参数:
            task_id: 任务ID
            task_logic: 你的业务函数
            
        示例:
            def my_job():
                print("干活啦！")
                return "完成！"
                
            agent.run_task(task_id, my_job)
        """
        task = self.tasks.get(task_id)
        if not task:
            print(f"❌ 找不到任务: {task_id}")
            return None
        
        print(f"\n🚀 开始运行任务: {task.name}")
        task.status = "running"
        
        try:
            # 运行你的业务逻辑
            result = task_logic()
            
            task.status = "completed"
            task.result = result
            print(f"✅ 任务完成！结果: {result}")
            return result
            
        except Exception as e:
            task.status = "failed"
            print(f"❌ 任务失败: {e}")
            return None
    
    def create_and_run(self, name: str, task_logic: Callable) -> str:
        """
        【1行代码】一步到位！创建+运行
        
        示例:
            def job():
                print("干活啦！")
                
            task_id = agent.create_and_run("我的任务", job)
        """
        task_id = self.create_task(name)
        self.run_task(task_id, task_logic)
        return task_id
    
    def get_status(self, task_id: str) -> str:
        """
        【1行代码】获取状态
        
        示例:
            status = agent.get_status(task_id)
        """
        task = self.tasks.get(task_id)
        if task:
            return task.status
        return "unknown"
    
    def list_tasks(self) -> list:
        """
        【1行代码】列出所有任务
        
        示例:
            for task in agent.list_tasks():
                print(task)
        """
        result = []
        for task_id, task in self.tasks.items():
            result.append({
                "id": task_id,
                "name": task.name,
                "status": task.status
            })
        return result


# ============================================
# 🎮 使用示例（复制粘贴就能用！）
# ============================================

def example_1_hello_world():
    """示例 1: 最最简单的 Hello World"""
    print("\n" + "="*60)
    print("  示例 1: Hello World")
    print("="*60)
    
    # 1. 创建 Agent
    agent = SimpleAgentAPI()
    
    # 2. 定义你的任务（写个普通函数就行！）
    def hello():
        print("👋 Hello, AgentTaskSystem!")
        return "Hello 成功！"
    
    # 3. 运行（就这一行！）
    agent.create_and_run("Hello任务", hello)


def example_2_data_collect():
    """示例 2: 模拟数据采集"""
    print("\n" + "="*60)
    print("  示例 2: 数据采集")
    print("="*60)
    
    agent = SimpleAgentAPI()
    
    # 这是你的业务逻辑
    def collect_data():
        print("📊 开始采集数据...")
        time.sleep(0.5)
        
        print("   步骤 1/3: 连接数据库...")
        time.sleep(0.3)
        
        print("   步骤 2/3: 读取数据...")
        time.sleep(0.3)
        
        print("   步骤 3/3: 处理数据...")
        time.sleep(0.3)
        
        print("✅ 数据采集完成！")
        return {"count": 100, "status": "success"}
    
    # 运行！
    agent.create_and_run("数据采集", collect_data)


def example_3_multiple_tasks():
    """示例 3: 多个任务"""
    print("\n" + "="*60)
    print("  示例 3: 多个任务")
    print("="*60)
    
    agent = SimpleAgentAPI()
    
    # 任务 1
    def task_sales():
        print("📈 生成销售报表...")
        time.sleep(0.2)
        print("✅ 销售报表完成")
    
    # 任务 2
    def task_users():
        print("👥 生成用户报表...")
        time.sleep(0.2)
        print("✅ 用户报表完成")
    
    # 任务 3
    def task_inventory():
        print("📦 生成库存报表...")
        time.sleep(0.2)
        print("✅ 库存报表完成")
    
    # 全部运行！
    print("\n🚀 开始运行多个任务...")
    agent.create_and_run("销售报表", task_sales)
    agent.create_and_run("用户报表", task_users)
    agent.create_and_run("库存报表", task_inventory)
    
    # 查看所有任务
    print("\n📋 所有任务:")
    for task in agent.list_tasks():
        print(f"  - {task['name']}: {task['status']}")


def main():
    """运行所有示例"""
    print("\n" + "🎯"*30)
    print("  AgentTaskSystem - 超简单接口演示")
    print("🎯"*30)
    
    # 运行示例
    example_1_hello_world()
    example_2_data_collect()
    example_3_multiple_tasks()
    
    print("\n" + "="*60)
    print("  🎉 所有示例完成！")
    print("="*60)
    
    print("\n💡 总结:")
    print("  1. 定义你的函数（普通函数就行！）")
    print("  2. agent.create_and_run() 一步运行")
    print("  3. 就这么简单！")


if __name__ == "__main__":
    main()
