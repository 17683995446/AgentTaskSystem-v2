"""
插件系统测试
测试所有内置插件
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from AgentTaskSystem.PluginManager import create_plugin_manager
from AgentTaskSystem.PluginManager.plugins import (
    RequestsPlugin,
    BeautifulSoupPlugin,
    PandasPlugin,
    SchedulePlugin,
    EmailPlugin
)


class TestRequestsPlugin(unittest.TestCase):
    """测试HTTP请求插件"""

    def setUp(self):
        self.manager = create_plugin_manager()
        self.plugin = RequestsPlugin()
        self.manager.register_plugin(self.plugin)

    def tearDown(self):
        self.manager.shutdown_all()

    def test_get_request(self):
        """测试GET请求"""
        result = self.manager.execute_plugin("requests_http", {
            "method": "GET",
            "url": "https://httpbin.org/get"
        })
        self.assertTrue(result["success"])
        self.assertEqual(result["result"]["status_code"], 200)

    def test_post_request(self):
        """测试POST请求"""
        result = self.manager.execute_plugin("requests_http", {
            "method": "POST",
            "url": "https://httpbin.org/post",
            "data": {"test": "data"}
        })
        self.assertTrue(result["success"])
        self.assertEqual(result["result"]["status_code"], 200)


class TestBeautifulSoupPlugin(unittest.TestCase):
    """测试网页解析插件"""

    def setUp(self):
        self.manager = create_plugin_manager()
        self.plugin = BeautifulSoupPlugin()
        self.manager.register_plugin(self.plugin)

    def tearDown(self):
        self.manager.shutdown_all()

    def test_parse_html(self):
        """测试HTML解析"""
        result = self.manager.execute_plugin("beautifulsoup_scraper", {
            "action": "parse",
            "html": "<html><body><h1>Test</h1></body></html>",
            "selector": "h1"
        })
        self.assertTrue(result["success"])


class TestPandasPlugin(unittest.TestCase):
    """测试数据处理插件"""

    def setUp(self):
        self.manager = create_plugin_manager()
        self.plugin = PandasPlugin()
        self.manager.register_plugin(self.plugin)

    def tearDown(self):
        self.manager.shutdown_all()

    def test_analyze(self):
        """测试数据分析"""
        result = self.manager.execute_plugin("pandas_data", {
            "action": "analyze",
            "data": [
                {"name": "A", "value": 100},
                {"name": "B", "value": 200}
            ]
        })
        self.assertTrue(result["success"])

    def test_aggregate(self):
        """测试数据聚合"""
        result = self.manager.execute_plugin("pandas_data", {
            "action": "aggregate",
            "data": [
                {"name": "A", "value": 100},
                {"name": "A", "value": 200},
                {"name": "B", "value": 50}
            ],
            "group_by": "name",
            "agg_func": "sum"
        })
        self.assertTrue(result["success"])


class TestSchedulePlugin(unittest.TestCase):
    """测试定时任务插件"""

    def setUp(self):
        self.manager = create_plugin_manager()
        self.plugin = SchedulePlugin()
        self.manager.register_plugin(self.plugin)

    def tearDown(self):
        self.manager.shutdown_all()

    def test_add_job(self):
        """测试添加任务"""
        result = self.manager.execute_plugin("schedule_timer", {
            "action": "add_job",
            "job_id": "test_job",
            "interval": 1,
            "unit": "minutes"
        })
        self.assertTrue(result["success"])


if __name__ == "__main__":
    unittest.main()
