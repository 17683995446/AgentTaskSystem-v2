from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class IDashboardLayout(ABC):
    @abstractmethod
    def create_dashboard(self, name: str, layout_type: str) -> str:
        pass

    @abstractmethod
    def add_component(self, dashboard_id: str, component: Dict[str, Any]) -> bool:
        pass

    @abstractmethod
    def remove_component(self, dashboard_id: str, component_id: str) -> bool:
        pass

    @abstractmethod
    def update_layout(self, dashboard_id: str, layout_config: Dict[str, Any]) -> bool:
        pass

    @abstractmethod
    def get_dashboard(self, dashboard_id: str) -> Optional[Dict[str, Any]]:
        pass
