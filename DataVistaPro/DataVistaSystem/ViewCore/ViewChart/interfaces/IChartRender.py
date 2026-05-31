from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class IChartRender(ABC):
    @abstractmethod
    def render_chart(self, chart_type: str, data: Dict[str, Any], config: Any) -> str:
        pass

    @abstractmethod
    def update_chart(self, chart_id: str, new_data: Dict[str, Any]) -> bool:
        pass

    @abstractmethod
    def get_chart_config(self, chart_type: str) -> Any:
        pass

    @abstractmethod
    def export_chart(self, chart_id: str, format: str) -> bytes:
        pass
