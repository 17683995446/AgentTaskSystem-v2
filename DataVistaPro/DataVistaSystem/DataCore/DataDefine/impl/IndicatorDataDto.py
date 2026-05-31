from dataclasses import dataclass
from typing import Any
from datetime import datetime
from ..interfaces.IndicatorTypeEnum import IndicatorTypeEnum


@dataclass
class IndicatorDataDto:
    indicator_id: str
    name: str
    indicator_type: IndicatorTypeEnum
    unit: str
    threshold_min: float
    threshold_max: float
    refresh_interval: int
    data_source: str
    created_at: datetime
    updated_at: datetime
