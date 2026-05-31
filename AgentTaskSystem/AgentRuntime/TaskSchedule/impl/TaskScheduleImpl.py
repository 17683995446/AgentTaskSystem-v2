import asyncio
from typing import Callable, Optional, List, Dict
from datetime import datetime, timedelta
from ..interfaces.ITaskSchedule import ITaskSchedule


class _TaskScheduleImpl(ITaskSchedule):
    def __init__(self, task_define_impl):
        self._task_define = task_define_impl
        self._queue: List[str] = []
        self._callback: Optional[Callable[[str, Any], None]] = None
        self._task_start_times: Dict[str, datetime] = {}

    def _sort_queue(self) -> None:
        def get_priority(task_id: str):
            task = self._task_define.get_task_dto(task_id)
            return task.priority if task else 0
        self._queue.sort(key=get_priority, reverse=True)

    def enqueue_task(self, task_id: str) -> bool:
        if task_id in self._queue:
            return False
        return self._add_to_queue(task_id)

    def _add_to_queue(self, task_id: str) -> bool:
        self._queue.append(task_id)
        self._sort_queue()
        return True

    def dequeue_task(self) -> Optional[str]:
        if not self._queue:
            return None
        return self._pop_from_queue()

    def _pop_from_queue(self) -> str:
        task_id = self._queue.pop(0)
        self._task_start_times[task_id] = datetime.now()
        return task_id

    def check_retry(self, task_id: str) -> bool:
        task = self._task_define.get_task_dto(task_id)
        if not task or task.retry_count >= task.max_retries:
            return False
        return self._increment_retry(task)

    def _increment_retry(self, task) -> bool:
        task.retry_count += 1
        self._task_define.update_task(task)
        return True

    def check_timeout(self, task_id: str) -> bool:
        task = self._task_define.get_task_dto(task_id)
        if not task:
            return False
        return self._check_elapsed_time(task_id, task)

    def _check_elapsed_time(self, task_id: str, task) -> bool:
        start_time = self._task_start_times.get(task_id)
        if not start_time:
            return False
        elapsed = (datetime.now() - start_time).total_seconds()
        return elapsed > task.timeout_seconds

    def set_task_callback(self, callback: Callable[[str, Any], None]):
        self._callback = callback

    def notify_callback(self, task_id: str, status):
        if self._callback:
            self._callback(task_id, status)


def create_task_schedule(task_define_impl):
    return _TaskScheduleImpl(task_define_impl)
