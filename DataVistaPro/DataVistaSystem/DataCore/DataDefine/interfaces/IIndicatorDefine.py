from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List


class IIndicatorDefine(ABC):
    @abstractmethod
    def create_indicator(self, name: str, indicator_type: str, config: Dict[str, Any]) -> str:
        pass

    @abstractmethod
    def update_indicator(self, indicator_id: str, updates: Dict[str, Any]) -> bool:
        pass

    @abstractmethod
    def delete_indicator(self, indicator_id: str) -> bool:
        pass

    @abstractmethod
    def get_indicator(self, indicator_id: str) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def list_indicators(self, filters: Optional[Dict[str, Any]]) -> List[Dict[str, Any]]:
        pass
