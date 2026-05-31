"""
核心系统测试
测试AgentTaskSystem的核心功能
"""

import asyncio
import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import AgentTaskSystem, TaskStatusEnum


class TestAgentTaskSystem(unittest.TestCase):
    """测试核心系统"""

    def setUp(self):
        self.system = AgentTaskSystem()

    def test_create_task(self):
        """测试创建任务"""
        task_id = self.system.create_task("test", 1, {"data": "test"})
        self.assertIsNotNone(task_id)
        self.assertEqual(len(task_id), 36)  # UUID长度

    def test_get_task_info(self):
        """测试获取任务信息"""
        task_id = self.system.create_task("test", 1, {"data": "test"})
        info = self.system.get_task_info(task_id)
        self.assertEqual(info["task_type"], "test")
        self.assertEqual(info["priority"], 1)
        self.assertEqual(info["status"], "pending")

    def test_task_status_enum(self):
        """测试状态枚举"""
        self.assertEqual(TaskStatusEnum.PENDING.value, "pending")
        self.assertEqual(TaskStatusEnum.RUNNING.value, "running")
        self.assertEqual(TaskStatusEnum.COMPLETED.value, "completed")
        self.assertEqual(TaskStatusEnum.FAILED.value, "failed")


class TestAsyncExecution(unittest.TestCase):
    """测试异步执行"""

    def setUp(self):
        self.system = AgentTaskSystem()

    def test_start_task(self):
        """测试启动任务"""
        async def run_test():
            task_id = self.system.create_task("async_test", 1, {})

            async def logic(task_id, context):
                step = context.get("step", 0) + 1
                context["step"] = step
                return f"step_{step}", step < 3

            result = await self.system.start_task(task_id, logic)
            self.assertTrue(result)

        asyncio.run(run_test())


if __name__ == "__main__":
    unittest.main()
