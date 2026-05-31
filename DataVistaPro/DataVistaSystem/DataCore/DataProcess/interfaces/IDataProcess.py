from abc import ABC, abstractmethod
from typing import Dict, Any, List
from .DataFormatEnum import DataFormatEnum


class IDataProcess(ABC):
    @abstractmethod
    def process_data(self, data: List[Dict[str, Any]], process_type: str) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def aggregate_data(self, data: List[Dict[str, Any]], group_by: List[str]) -> Dict[str, Any]:
        pass

    @abstractmethod
    def transform_data(self, data: List[Dict[str, Any]], transforms: List[str]) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def validate_data(self, data: List[Dict[str, Any]], rules: Dict[str, Any]) -> Dict[str, Any]:
        pass
