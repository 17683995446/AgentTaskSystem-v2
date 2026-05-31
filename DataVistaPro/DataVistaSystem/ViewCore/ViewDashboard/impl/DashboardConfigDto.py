from dataclasses import dataclass, field
from typing import List, Dict, Any
from ..interfaces.LayoutTypeEnum import LayoutTypeEnum


@dataclass
class ComponentConfig:
    component_id: str
    type: str
    position_x: int
    position_y: int
    width: int
    height: int
    config: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DashboardConfigDto:
    dashboard_id: str
    name: str
    layout_type: LayoutTypeEnum
    grid_columns: int
    grid_rows: int
    components: List[ComponentConfig]
    theme: str
    auto_refresh: bool
    refresh_interval: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "dashboard_id": self.dashboard_id,
            "name": self.name,
            "layout_type": self.layout_type.value,
            "grid_columns": self.grid_columns,
            "grid_rows": self.grid_rows,
            "components": [
                {
                    "component_id": c.component_id,
                    "type": c.type,
                    "position_x": c.position_x,
                    "position_y": c.position_y,
                    "width": c.width,
                    "height": c.height,
                    "config": c.config
                }
                for c in self.components
            ],
            "theme": self.theme,
            "auto_refresh": self.auto_refresh,
            "refresh_interval": self.refresh_interval
        }
