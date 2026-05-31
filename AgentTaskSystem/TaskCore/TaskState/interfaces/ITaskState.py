from abc import ABC, abstractmethod
from typing import Dict, Any


class ITaskState(ABC):
    @abstractmethod
    def update_status(self, task_id: str, new_status: Any) -> bool:
        pass

    @abstractmethod
    def create_snapshot(self, task_id: str, context: Dict[str, Any]) -> str:
        pass

    @abstractmethod
    def restore_snapshot(self, task_id: str, snapshot_id: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_latest_snapshot(self, task_id: str) -> Dict[str, Any]:
        pass
