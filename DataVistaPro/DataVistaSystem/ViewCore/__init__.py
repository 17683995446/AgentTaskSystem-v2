from .ViewChart import IChartRender, ChartTypeEnum, create_chart_render
from .ViewDashboard import IDashboardLayout, LayoutTypeEnum, create_dashboard_layout


class ViewCore:
    def __init__(self, data_core):
        self.chart_render = create_chart_render(data_core)
        self.dashboard_layout = create_dashboard_layout()

    def get_components(self):
        return {
            "chart_render": self.chart_render,
            "dashboard_layout": self.dashboard_layout
        }


def create_view_core(data_core=None):
    return ViewCore(data_core)


__all__ = ["ViewCore", "create_view_core", "IChartRender", "ChartTypeEnum", "IDashboardLayout", "LayoutTypeEnum"]
