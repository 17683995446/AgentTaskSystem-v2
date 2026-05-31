from dataclasses import dataclass
from typing import List, Any
from ..interfaces.ChartTypeEnum import ChartTypeEnum


@dataclass
class ChartConfigDto:
    chart_id: str
    chart_type: ChartTypeEnum
    title: str
    width: int
    height: int
    colors: List[str]
    show_legend: bool
    show_tooltip: bool
    enable_animation: bool
    interactive_mode: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "chart_id": self.chart_id,
            "chart_type": self.chart_type.value,
            "title": self.title,
            "width": self.width,
            "height": self.height,
            "colors": self.colors,
            "show_legend": self.show_legend,
            "show_tooltip": self.show_tooltip,
            "enable_animation": self.enable_animation,
            "interactive_mode": self.interactive_mode
        }
