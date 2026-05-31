import uuid
from typing import Dict, Any, Optional
from ..interfaces.IDashboardLayout import IDashboardLayout
from ..interfaces.LayoutTypeEnum import LayoutTypeEnum
from .DashboardConfigDto import DashboardConfigDto, ComponentConfig


class _DashboardLayoutImpl(IDashboardLayout):
    def __init__(self):
        self._dashboards: Dict[str, DashboardConfigDto] = {}

    def create_dashboard(self, name: str, layout_type: str) -> str:
        dashboard_id = self._generate_dashboard_id()
        dashboard = self._build_dashboard(dashboard_id, name, layout_type)
        self._save_dashboard(dashboard)
        return dashboard_id

    def _generate_dashboard_id(self) -> str:
        return f"dashboard_{uuid.uuid4().hex[:8]}"

    def _build_dashboard(self, dashboard_id: str, name: str, layout_type: str) -> DashboardConfigDto:
        return DashboardConfigDto(
            dashboard_id=dashboard_id,
            name=name,
            layout_type=LayoutTypeEnum(layout_type),
            grid_columns=12,
            grid_rows=8,
            components=[],
            theme="light",
            auto_refresh=True,
            refresh_interval=60
        )

    def _save_dashboard(self, dashboard: DashboardConfigDto) -> None:
        self._dashboards[dashboard.dashboard_id] = dashboard

    def add_component(self, dashboard_id: str, component: Dict[str, Any]) -> bool:
        dashboard = self._dashboards.get(dashboard_id)
        if not dashboard:
            return False
        new_component = self._build_component(component)
        dashboard.components.append(new_component)
        return True

    def _build_component(self, component: Dict[str, Any]) -> ComponentConfig:
        return ComponentConfig(
            component_id=self._generate_component_id(),
            type=component.get("type", "chart"),
            position_x=component.get("position_x", 0),
            position_y=component.get("position_y", 0),
            width=component.get("width", 4),
            height=component.get("height", 3),
            config=component.get("config", {})
        )

    def _generate_component_id(self) -> str:
        return f"component_{uuid.uuid4().hex[:8]}"

    def remove_component(self, dashboard_id: str, component_id: str) -> bool:
        dashboard = self._dashboards.get(dashboard_id)
        if not dashboard:
            return False
        dashboard.components = [c for c in dashboard.components if c.component_id != component_id]
        return True

    def update_layout(self, dashboard_id: str, layout_config: Dict[str, Any]) -> bool:
        dashboard = self._dashboards.get(dashboard_id)
        if not dashboard:
            return False
        self._apply_layout_updates(dashboard, layout_config)
        return True

    def _apply_layout_updates(self, dashboard: DashboardConfigDto, layout_config: Dict[str, Any]) -> None:
        if "grid_columns" in layout_config:
            dashboard.grid_columns = layout_config["grid_columns"]
        if "grid_rows" in layout_config:
            dashboard.grid_rows = layout_config["grid_rows"]
        if "theme" in layout_config:
            dashboard.theme = layout_config["theme"]
        if "auto_refresh" in layout_config:
            dashboard.auto_refresh = layout_config["auto_refresh"]
        if "refresh_interval" in layout_config:
            dashboard.refresh_interval = layout_config["refresh_interval"]

    def get_dashboard(self, dashboard_id: str) -> Optional[Dict[str, Any]]:
        dashboard = self._dashboards.get(dashboard_id)
        return dashboard.to_dict() if dashboard else None


def create_dashboard_layout() -> IDashboardLayout:
    return _DashboardLayoutImpl()
