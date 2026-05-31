import uuid
from typing import Dict, Any, Optional, List
from datetime import datetime
from ..interfaces.IIndicatorDefine import IIndicatorDefine
from ..interfaces.IndicatorTypeEnum import IndicatorTypeEnum
from .IndicatorDataDto import IndicatorDataDto


class _IndicatorDefineImpl(IIndicatorDefine):
    def __init__(self):
        self._indicators: Dict[str, IndicatorDataDto] = {}

    def create_indicator(self, name: str, indicator_type: str, config: Dict[str, Any]) -> str:
        indicator_id = self._generate_id()
        indicator = self._build_indicator(indicator_id, name, indicator_type, config)
        self._save_indicator(indicator)
        return indicator_id

    def _generate_id(self) -> str:
        return str(uuid.uuid4())

    def _build_indicator(self, indicator_id: str, name: str, indicator_type: str, config: Dict[str, Any]) -> IndicatorDataDto:
        now = datetime.now()
        return IndicatorDataDto(
            indicator_id=indicator_id,
            name=name,
            indicator_type=IndicatorTypeEnum(indicator_type),
            unit=config.get("unit", ""),
            threshold_min=config.get("threshold_min", 0.0),
            threshold_max=config.get("threshold_max", 100.0),
            refresh_interval=config.get("refresh_interval", 60),
            data_source=config.get("data_source", ""),
            created_at=now,
            updated_at=now
        )

    def _save_indicator(self, indicator: IndicatorDataDto) -> None:
        self._indicators[indicator.indicator_id] = indicator

    def update_indicator(self, indicator_id: str, updates: Dict[str, Any]) -> bool:
        indicator = self._indicators.get(indicator_id)
        if not indicator:
            return False
        self._apply_updates(indicator, updates)
        return True

    def _apply_updates(self, indicator: IndicatorDataDto, updates: Dict[str, Any]) -> None:
        if "name" in updates:
            indicator.name = updates["name"]
        if "threshold_min" in updates:
            indicator.threshold_min = updates["threshold_min"]
        if "threshold_max" in updates:
            indicator.threshold_max = updates["threshold_max"]
        if "refresh_interval" in updates:
            indicator.refresh_interval = updates["refresh_interval"]
        indicator.updated_at = datetime.now()

    def delete_indicator(self, indicator_id: str) -> bool:
        if indicator_id not in self._indicators:
            return False
        del self._indicators[indicator_id]
        return True

    def get_indicator(self, indicator_id: str) -> Optional[Dict[str, Any]]:
        indicator = self._indicators.get(indicator_id)
        return self._format_indicator(indicator) if indicator else None

    def _format_indicator(self, indicator: IndicatorDataDto) -> Dict[str, Any]:
        return {
            "indicator_id": indicator.indicator_id,
            "name": indicator.name,
            "indicator_type": indicator.indicator_type.value,
            "unit": indicator.unit,
            "threshold_min": indicator.threshold_min,
            "threshold_max": indicator.threshold_max,
            "refresh_interval": indicator.refresh_interval,
            "data_source": indicator.data_source,
            "created_at": indicator.created_at.isoformat(),
            "updated_at": indicator.updated_at.isoformat()
        }

    def list_indicators(self, filters: Optional[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not filters:
            return self._list_all_indicators()
        return self._filter_indicators(filters)

    def _list_all_indicators(self) -> List[Dict[str, Any]]:
        return [self._format_indicator(ind) for ind in self._indicators.values()]

    def _filter_indicators(self, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        result = []
        for indicator in self._indicators.values():
            if self._matches_filter(indicator, filters):
                result.append(self._format_indicator(indicator))
        return result

    def _matches_filter(self, indicator: IndicatorDataDto, filters: Dict[str, Any]) -> bool:
        if "indicator_type" in filters:
            if indicator.indicator_type.value != filters["indicator_type"]:
                return False
        if "name" in filters:
            if filters["name"] not in indicator.name:
                return False
        return True


def create_indicator_define() -> IIndicatorDefine:
    return _IndicatorDefineImpl()
