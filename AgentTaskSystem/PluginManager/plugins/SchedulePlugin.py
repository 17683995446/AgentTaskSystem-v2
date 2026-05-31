"""
SchedulePlugin - 定时任务插件
基于 schedule，支持 cron 风格的定时任务
"""

import time
import threading
from typing import Dict, Any, List
from ..interfaces.IPlugin import IPlugin, PluginType


class SchedulePlugin(IPlugin):
    """
    定时任务插件
    功能: 定时执行任务、循环任务、延迟任务
    """

    @property
    def name(self) -> str:
        return "schedule_timer"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def plugin_type(self) -> PluginType:
        return PluginType.CUSTOM

    @property
    def description(self) -> str:
        return "定时任务插件，支持秒/分/时/天级别的定时执行"

    @property
    def dependencies(self) -> List[str]:
        return ["schedule"]

    def initialize(self, config: Dict[str, Any] = None) -> bool:
        import schedule
        self.schedule = schedule
        self.config = config or {}
        self._running = False
        self._thread = None
        self._jobs = {}
        return True

    def execute(self, task_params: Dict[str, Any]) -> Dict[str, Any]:
        action = task_params.get("action", "add_job")

        if action == "add_job":
            return self._add_job(task_params)
        elif action == "remove_job":
            return self._remove_job(task_params)
        elif action == "list_jobs":
            return self._list_jobs(task_params)
        elif action == "start_scheduler":
            return self._start_scheduler(task_params)
        elif action == "stop_scheduler":
            return self._stop_scheduler(task_params)
        else:
            return {"error": f"不支持的操作: {action}"}

    def _add_job(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """添加定时任务"""
        job_id = params.get("job_id", "")
        interval = params.get("interval", 1)
        unit = params.get("unit", "minutes")  # seconds, minutes, hours, days
        callback = params.get("callback", None)

        if not job_id:
            return {"error": "任务ID不能为空"}

        try:
            if unit == "seconds":
                job = self.schedule.every(interval).seconds
            elif unit == "minutes":
                job = self.schedule.every(interval).minutes
            elif unit == "hours":
                job = self.schedule.every(interval).hours
            elif unit == "days":
                job = self.schedule.every(interval).days
            else:
                return {"error": f"不支持的时间单位: {unit}"}

            def job_func():
                if callback:
                    callback()
                else:
                    print(f"⏰ 定时任务执行: {job_id}")

            job.do(job_func)
            self._jobs[job_id] = job

            return {"success": True, "job_id": job_id, "interval": interval, "unit": unit}

        except Exception as e:
            return {"error": str(e)}

    def _remove_job(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """移除定时任务"""
        job_id = params.get("job_id", "")

        if job_id in self._jobs:
            self.schedule.cancel_job(self._jobs[job_id])
            del self._jobs[job_id]
            return {"success": True, "job_id": job_id}
        else:
            return {"error": f"任务 {job_id} 不存在"}

    def _list_jobs(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """列出所有定时任务"""
        jobs = []
        for job_id, job in self._jobs.items():
            jobs.append({
                "job_id": job_id,
                "interval": str(job.interval),
                "unit": job.unit,
                "next_run": str(job.next_run) if job.next_run else None
            })

        return {"jobs": jobs, "count": len(jobs)}

    def _start_scheduler(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """启动调度器"""
        if self._running:
            return {"success": True, "message": "调度器已在运行"}

        self._running = True

        def run_scheduler():
            while self._running:
                self.schedule.run_pending()
                time.sleep(1)

        self._thread = threading.Thread(target=run_scheduler, daemon=True)
        self._thread.start()

        return {"success": True, "message": "调度器已启动"}

    def _stop_scheduler(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """停止调度器"""
        self._running = False
        if self._thread:
            self._thread.join(timeout=5)

        return {"success": True, "message": "调度器已停止"}

    def health_check(self) -> bool:
        try:
            import schedule
            return True
        except:
            return False

    def shutdown(self) -> bool:
        self._stop_scheduler({})
        self._jobs.clear()
        return True
