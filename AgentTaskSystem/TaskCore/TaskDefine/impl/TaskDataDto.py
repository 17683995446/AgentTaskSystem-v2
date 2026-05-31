from dataclasses import dataclass
from typing import Dict, Any
from datetime import datetime
from ..interfaces.TaskStatusEnum import TaskStatusEnum


@dataclass
class TaskDataDto:
    task_id: str
    task_type: str
    priority: int
    status: TaskStatusEnum
    params: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    retry_count: int = 0
    max_retries: int = 3
    timeout_seconds: int = 3600
