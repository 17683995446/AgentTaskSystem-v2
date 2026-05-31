from abc import ABC, abstractmethod
from typing import Callable, Optional


class ITaskSchedule(ABC):
    @abstractmethod
    def enqueue_task(self, task_id: str) -> bool:
        pass

    @abstractmethod
    def dequeue_task(self) -> Optional[str]:
        pass

    @abstractmethod
    def check_retry(self, task_id: str) -> bool:
        pass

    @abstractmethod
    def check_timeout(self, task_id: str) -> bool:
        pass

    @abstractmethod
    def set_task_callback(self, callback: Callable[[str, Any], None]) -> None:
        pass
