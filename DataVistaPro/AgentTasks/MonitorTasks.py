"""
DataVista Monitor Tasks - 监控任务模块
严格遵循二叉树架构规范
"""

import asyncio
import time
import random
from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass

from AgentTaskSystem.TaskCore.TaskDefine.interfaces.ITaskState import ITaskState


@dataclass
class Alert:
    alert_id: str
    alert_type: str
    level: str
    message: str
    timestamp: str
    resolved: bool = False


@dataclass
class PerformanceMetric:
    metric_name: str
    value: float
    threshold: float
    status: str
    timestamp: str


class HealthMonitorTask:
    """健康监控任务"""
    
    def __init__(self, monitor_id: str, task_state: ITaskState):
        self.monitor_id = monitor_id
        self.task_state = task_state
        self._alerts: List[Alert] = []
        self._metrics: List[PerformanceMetric] = []

    async def run(self):
        """运行监控任务"""
        self.task_state.update_status(self.monitor_id, "running")
        
        while True:
            try:
                await self._check_once()
                await asyncio.sleep(10)
            except asyncio.CancelledError:
                break

    async def _check_once(self):
        """单次检查"""
        self._check_database()
        self._check_api_performance()
        self._check_disk_space()
        self._check_memory_usage()
        self._save_snapshot()

    def _check_database(self):
        """检查数据库状态"""
        is_healthy = random.random() > 0.1
        
        if not is_healthy:
            alert = Alert(
                alert_id=f"db_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                alert_type="database",
                level="warning",
                message="数据库连接异常",
                timestamp=datetime.now().isoformat()
            )
            self._alerts.append(alert)

    def _check_api_performance(self):
        """检查API性能"""
        response_time = random.uniform(0.1, 2)
        
        metric = PerformanceMetric(
            metric_name="api_response_time",
            value=response_time,
            threshold=1.0,
            status="normal" if response_time < 1.0 else "warning",
            timestamp=datetime.now().isoformat()
        )
        
        self._metrics.append(metric)
        
        if response_time > 1.0:
            alert = Alert(
                alert_id=f"api_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                alert_type="performance",
                level="warning",
                message=f"API响应时间过长: {response_time:.2f}s",
                timestamp=datetime.now().isoformat()
            )
            self._alerts.append(alert)

    def _check_disk_space(self):
        """检查磁盘空间"""
        usage = random.uniform(50, 85)
        
        if usage > 80:
            alert = Alert(
                alert_id=f"disk_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                alert_type="system",
                level="critical",
                message=f"磁盘空间使用率过高: {usage:.1f}%",
                timestamp=datetime.now().isoformat()
            )
            self._alerts.append(alert)

    def _check_memory_usage(self):
        """检查内存使用"""
        usage = random.uniform(30, 75)
        
        metric = PerformanceMetric(
            metric_name="memory_usage",
            value=usage,
            threshold=70,
            status="normal" if usage < 70 else "warning",
            timestamp=datetime.now().isoformat()
        )
        self._metrics.append(metric)

    def _save_snapshot(self):
        """保存快照"""
        self.task_state.create_snapshot(
            self.monitor_id,
            {
                "alerts_count": len([a for a in self._alerts if not a.resolved]),
                "metrics_count": len(self._metrics),
                "last_check": datetime.now().isoformat()
            }
        )

    def get_active_alerts(self):
        """获取活跃告警"""
        return [a for a in self._alerts if not a.resolved]

    def resolve_alert(self, alert_id: str):
        """解决告警"""
        for alert in self._alerts:
            if alert.alert_id == alert_id:
                alert.resolved = True
                return True
        return False

    def get_metrics(self, limit: int = 100):
        """获取性能指标"""
        return self._metrics[-limit:]


class AlertTask:
    """告警任务"""
    
    def __init__(self, alert_id: str, task_state: ITaskState):
        self.alert_id = alert_id
        self.task_state = task_state

    async def send_alert(self, alert: Alert):
        """发送告警"""
        print(f"[ALERT] {alert.level.upper()}: {alert.message}")
        await asyncio.sleep(0.5)
        self.task_state.update_status(self.alert_id, "completed")


def create_health_monitor(monitor_id: str, task_state: ITaskState) -> HealthMonitorTask:
    return HealthMonitorTask(monitor_id, task_state)


def create_alert_task(alert_id: str, task_state: ITaskState) -> AlertTask:
    return AlertTask(alert_id, task_state)
