import uuid
from datetime import datetime
from typing import Dict, Any
from ..interfaces.ITaskDefine import ITaskDefine
from ..interfaces.TaskStatusEnum import TaskStatusEnum
from .TaskDataDto import TaskDataDto


class _TaskDefineImpl(ITaskDefine):
    def __init__(self):
        self._task_storage: Dict[str, TaskDataDto] = {}

    def create_task(self, task_type: str, priority: int, params: Dict[str, Any]) -> str:
        task_id = self._generate_task_id()
        task = self._build_task_dto(task_id, task_type, priority, params)
        self._save_task(task)
        return task_id

    def _generate_task_id(self) -> str:
        return str(uuid.uuid4())

    def _build_task_dto(self, task_id: str, task_type: str, priority: int, params: Dict[str, Any]) -> TaskDataDto:
        now = datetime.now()
        return TaskDataDto(
            task_id=task_id,
            task_type=task_type,
            priority=priority,
            status=TaskStatusEnum.PENDING,
            params=params,
            created_at=now,
            updated_at=now
        )

    def _save_task(self, task: TaskDataDto) -> None:
        self._task_storage[task.task_id] = task

    def validate_params(self, task_type: str, params: Dict[str, Any]) -> bool:
        return isinstance(params, dict)

    def get_task_info(self, task_id: str) -> Dict[str, Any]:
        task = self._task_storage.get(task_id)
        return self._format_task_info(task) if task else {}

    def _format_task_info(self, task: TaskDataDto) -> Dict[str, Any]:
        return {
            "task_id": task.task_id,
            "task_type": task.task_type,
            "priority": task.priority,
            "status": task.status.value,
            "created_at": task.created_at.isoformat(),
            "retry_count": task.retry_count
        }

    def get_task_dto(self, task_id: str) -> TaskDataDto:
        return self._task_storage.get(task_id)

    def update_task(self, task: TaskDataDto) -> None:
        self._update_timestamp(task)
        self._save_task(task)

    def _update_timestamp(self, task: TaskDataDto) -> None:
        task.updated_at = datetime.now()


def create_task_define() -> ITaskDefine:
    return _TaskDefineImpl()
