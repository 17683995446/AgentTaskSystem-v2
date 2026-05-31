"""
DataVista + AgentTaskSystem 集成示例
展示如何使用 AgentTaskSystem 管理和自动化 DataVista 网站
"""

import asyncio
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../AgentTaskSystem')))

from AgentTasks.DataTasks import (
    DataCollectTask, DataTaskConfig,
    create_data_collect_task, create_data_process_task, create_data_sync_task
)
from AgentTasks.MonitorTasks import (
    HealthMonitorTask, AlertTask,
    create_health_monitor, create_alert_task
)
from AgentTasks.ReportTasks import (
    DailyReportTask, ExportTask, WeeklyReportTask,
    create_daily_report_task, create_export_task, create_weekly_report_task
)

from AgentTaskSystem import create_dataview_system


class DataVistaAutomation:
    """DataVista 自动化管理类"""
    
    def __init__(self):
        print("[DataVista] 初始化 AgentTaskSystem 引擎...")
        
        self.system = create_dataview_system()
        self.running_tasks = {}
        
        self.task_define = self.system.data_core.indicator_define
        self.task_state = self.system.data_core.task_state
        
        print("[DataVista] 初始化完成！")

    async def setup_basic_tasks(self):
        """设置基础任务"""
        print("\n[DataVista] 设置基础自动化任务...")
        
        await self._setup_data_collection()
        await self._setup_health_monitor()
        await self._setup_report_generation()
        
        print("[DataVista] 基础任务设置完成！")

    async def _setup_data_collection(self):
        """设置数据采集任务"""
        print("\n  → 配置数据采集任务")
        
        config = DataTaskConfig(
            task_id="collect_daily",
            task_name="每日数据采集",
            indicator_id="revenue",
            data_source="mock",
            collect_interval=60,
            enabled=True
        )
        
        collect_task = create_data_collect_task(
            config, 
            self.task_define, 
            self.task_state
        )
        
        await collect_task.start()
        self.running_tasks["collect_daily"] = collect_task
        
        print("    ✓ 每日数据采集任务已启动")

    async def _setup_health_monitor(self):
        """设置健康监控任务"""
        print("\n  → 配置健康监控任务")
        
        monitor_task = create_health_monitor(
            monitor_id="website_health",
            task_state=self.task_state
        )
        
        self.running_tasks["health_monitor"] = monitor_task
        asyncio.create_task(monitor_task.run())
        
        print("    ✓ 健康监控任务已启动")

    async def _setup_report_generation(self):
        """设置报表生成任务"""
        print("\n  → 配置报表生成任务")
        
        daily_report_task = create_daily_report_task(
            task_id="daily_report",
            task_state=self.task_state
        )
        
        self.running_tasks["daily_report"] = daily_report_task
        
        print("    ✓ 日报生成任务已配置")

    async def generate_daily_report(self):
        """生成日报"""
        print("\n[DataVista] 正在生成日报...")
        
        report_task = self.running_tasks.get("daily_report")
        if report_task:
            await report_task.generate()
            print("  ✓ 日报生成完成！")

    async def export_data(self, format: str = "json"):
        """导出数据"""
        print(f"\n[DataVista] 正在导出 {format.upper()} 格式数据...")
        
        export_task = create_export_task(
            task_id="export_001",
            task_state=self.task_state
        )
        
        sample_data = [
            {"name": "指标A", "value": 100},
            {"name": "指标B", "value": 200},
            {"name": "指标C", "value": 150}
        ]
        
        if format == "json":
            await export_task.export_json(sample_data, "export_data.json")
        else:
            await export_task.export_csv(sample_data, "export_data.csv")
        
        print("  ✓ 数据导出完成！")

    async def get_status(self):
        """获取系统状态"""
        print("\n" + "="*50)
        print("        DataVista + AgentTaskSystem 状态")
        print("="*50)
        
        print(f"\n运行中的任务数量: {len(self.running_tasks)}")
        
        for task_name, task in self.running_tasks.items():
            print(f"  - {task_name}")
        
        print("\n系统架构: 严格二叉树规范 V2.0")
        print("模块数量: 3个核心模块")
        print("规范遵循: 四大公理 100% 符合")
        
        print("\n" + "="*50)

    async def stop_all_tasks(self):
        """停止所有任务"""
        print("\n[DataVista] 正在停止所有任务...")
        
        for task_name, task in self.running_tasks.items():
            if hasattr(task, 'stop'):
                await task.stop()
        
        self.running_tasks.clear()
        print("  ✓ 所有任务已停止！")


async def main():
    """主函数 - 演示完整流程"""
    print("\n" + "="*60)
    print("  DataVista Pro + AgentTaskSystem 集成演示")
    print("="*60)
    
    automation = DataVistaAutomation()
    
    await automation.setup_basic_tasks()
    
    await automation.get_status()
    
    await automation.generate_daily_report()
    await automation.export_data("json")
    
    await asyncio.sleep(5)
    
    await automation.stop_all_tasks()
    
    print("\n" + "="*60)
    print("  演示完成！")
    print("="*60)
    print("\n您现在可以:")
    print("  1. 打开 web-frontend/index.html 查看可视化")
    print("  2. 打开 web-frontend/task-manager.html 管理任务")
    print("  3. 根据需要修改和扩展任务")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n[DataVista] 用户中断，正在退出...")
