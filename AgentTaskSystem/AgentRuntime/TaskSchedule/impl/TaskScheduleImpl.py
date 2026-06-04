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
        """检查是否可以重试（增加计数并入队）。"""
        if not self._check_retry_conditions(task_id):
            return False
        return self._do_retry(task_id)

    def _check_retry_conditions(self, task_id: str) -> bool:
        """检查重试条件（不增加计数）。"""
        task = self._task_define.get_task_dto(task_id)
        if not task:
            return False
        if task.retry_count >= task.max_retries:
            return False
        # 检查状态是否允许转换到PENDING
        from ....TaskCore.TaskDefine.interfaces.TaskStatusEnum import TaskStatusEnum
        if task.status not in self._get_retry_allowed_statuses():
            return False
        return True

    def _get_retry_allowed_statuses(self):
        """返回允许重试的状态列表"""
        from ....TaskCore.TaskDefine.interfaces.TaskStatusEnum import TaskStatusEnum
        return [TaskStatusEnum.RUNNING, TaskStatusEnum.FAILED]

    def _do_retry(self, task_id: str) -> bool:
        """执行重试：增加计数并入队。"""
        task = self._task_define.get_task_dto(task_id)
        if not task:
            return False
        task.retry_count += 1
        self._task_define.update_task(task)
        self.enqueue_task(task_id)
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
