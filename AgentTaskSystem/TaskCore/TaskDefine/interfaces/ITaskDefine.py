from abc import ABC, abstractmethod
from typing import Dict, Any
from .TaskStatusEnum import TaskStatusEnum


class ITaskDefine(ABC):
    @abstractmethod
    def create_task(self, task_type: str, priority: int, params: Dict[str, Any]) -> str:
        pass

    @abstractmethod
    def validate_params(self, task_type: str, params: Dict[str, Any]) -> bool:
        pass

    @abstractmethod
    def get_task_info(self, task_id: str) -> Dict[str, Any]:
        pass
