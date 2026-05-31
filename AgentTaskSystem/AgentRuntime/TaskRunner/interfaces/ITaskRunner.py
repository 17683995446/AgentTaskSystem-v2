from abc import ABC, abstractmethod
from typing import Dict, Any, Callable, Tuple


class ITaskRunner(ABC):
    @abstractmethod
    async def start_task(self, task_id: str, business_logic: Callable[[str, Dict[str, Any]], Tuple[Any, bool]]) -> bool:
        pass

    @abstractmethod
    async def resume_task(self, task_id: str, business_logic: Callable[[str, Dict[str, Any]], Tuple[Any, bool]]) -> bool:
        pass

    @abstractmethod
    async def stop_task(self, task_id: str) -> bool:
        pass

    @abstractmethod
    def register_business_logic(self, task_type: str, logic: Callable[[str, Dict[str, Any]], Tuple[Any, bool]]) -> None:
        pass
