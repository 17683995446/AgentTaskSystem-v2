import uuid
from typing import Dict, Any, Optional
from ..interfaces.IChartRender import IChartRender
from ..interfaces.ChartTypeEnum import ChartTypeEnum
from .ChartConfigDto import ChartConfigDto


class _ChartRenderImpl(IChartRender):
    def __init__(self, data_core=None):
        self._data_core = data_core
        self._chart_instances: Dict[str, Dict[str, Any]] = {}
        self._chart_configs: Dict[str, ChartConfigDto] = {}
        self._default_config = self._create_default_config()

    def _create_default_config(self) -> ChartConfigDto:
        return ChartConfigDto(
            chart_id="default",
            chart_type=ChartTypeEnum.LINE,
            title="Chart",
            width=600,
            height=400,
            colors=["#007bff", "#28a745", "#ffc107", "#dc3545", "#17a2b8"],
            show_legend=True,
            show_tooltip=True,
            enable_animation=True,
            interactive_mode="hover"
        )

    def render_chart(self, chart_type: str, data: Dict[str, Any], config: Any) -> str:
        chart_id = self._generate_chart_id()
        chart_config = self._build_chart_config(chart_id, chart_type, config)
        self._store_chart_instance(chart_id, data, chart_config)
        return chart_id

    def _generate_chart_id(self) -> str:
        return f"chart_{uuid.uuid4().hex[:8]}"

    def _build_chart_config(self, chart_id: str, chart_type: str, config: Any) -> ChartConfigDto:
        if config:
            return ChartConfigDto(
                chart_id=chart_id,
                chart_type=ChartTypeEnum(chart_type),
                title=config.get("title", "Chart"),
                width=config.get("width", 600),
                height=config.get("height", 400),
                colors=config.get("colors", self._default_config.colors),
                show_legend=config.get("show_legend", True),
                show_tooltip=config.get("show_tooltip", True),
                enable_animation=config.get("enable_animation", True),
                interactive_mode=config.get("interactive_mode", "hover")
            )
        return ChartConfigDto(
            chart_id=chart_id,
            chart_type=ChartTypeEnum(chart_type),
            title=self._default_config.title,
            width=self._default_config.width,
            height=self._default_config.height,
            colors=self._default_config.colors,
            show_legend=self._default_config.show_legend,
            show_tooltip=self._default_config.show_tooltip,
            enable_animation=self._default_config.enable_animation,
            interactive_mode=self._default_config.interactive_mode
        )

    def _store_chart_instance(self, chart_id: str, data: Dict[str, Any], config: ChartConfigDto) -> None:
        self._chart_instances[chart_id] = {
            "data": data,
            "config": config
        }
        self._chart_configs[chart_id] = config

    def update_chart(self, chart_id: str, new_data: Dict[str, Any]) -> bool:
        if chart_id not in self._chart_instances:
            return False
        self._chart_instances[chart_id]["data"] = new_data
        return True

    def get_chart_config(self, chart_type: str) -> ChartConfigDto:
        base_config = self._create_default_config()
        base_config.chart_type = ChartTypeEnum(chart_type)
        base_config.title = f"{chart_type.capitalize()} Chart"
        return base_config

    def export_chart(self, chart_id: str, format: str) -> bytes:
        if chart_id not in self._chart_instances:
            return b""
        instance = self._chart_instances[chart_id]
        return self._generate_export_data(instance, format)

    def _generate_export_data(self, instance: Dict[str, Any], format: str) -> bytes:
        data = instance["data"]
        config = instance["config"]
        if format == "json":
            export = {
                "config": config.to_dict(),
                "data": data
            }
            import json
            return json.dumps(export, indent=2).encode()
        elif format == "csv":
            return self._data_to_csv(data)
        return b""

    def _data_to_csv(self, data: Dict[str, Any]) -> bytes:
        if "labels" in data and "datasets" in data:
            labels = data["labels"]
            csv_lines = [",".join(["Label"] + [f"Series {i+1}" for i in range(len(data["datasets"]))])]
            for i, label in enumerate(labels):
                row = [label]
                for dataset in data["datasets"]:
                    if i < len(dataset.get("data", [])):
                        row.append(str(dataset["data"][i]))
                csv_lines.append(",".join(row))
            return "\n".join(csv_lines).encode()
        return b""


def create_chart_render(data_core=None) -> IChartRender:
    return _ChartRenderImpl(data_core)
