from typing import Dict, Any, List
from ..interfaces.IDataProcess import IDataProcess
from .ProcessResultDto import ProcessResultDto


class _DataProcessImpl(IDataProcess):
    def __init__(self):
        self._aggregation_functions = {
            "sum": self._sum_agg,
            "avg": self._avg_agg,
            "count": self._count_agg,
            "min": self._min_agg,
            "max": self._max_agg
        }

    def process_data(self, data: List[Dict[str, Any]], process_type: str) -> List[Dict[str, Any]]:
        if process_type == "filter":
            return self._filter_data(data)
        elif process_type == "sort":
            return self._sort_data(data)
        elif process_type == "dedup":
            return self._deduplicate_data(data)
        return data

    def _filter_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [item for item in data if item.get("value") is not None]

    def _sort_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return sorted(data, key=lambda x: x.get("timestamp", ""))

    def _deduplicate_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        seen = set()
        result = []
        for item in data:
            key = item.get("id")
            if key not in seen:
                seen.add(key)
                result.append(item)
        return result

    def aggregate_data(self, data: List[Dict[str, Any]], group_by: List[str]) -> Dict[str, Any]:
        groups = self._group_data(data, group_by)
        results = {}
        for group_key, group_data in groups.items():
            results[group_key] = self._calculate_aggregates(group_data)
        return results

    def _group_data(self, data: List[Dict[str, Any]], group_by: List[str]) -> Dict[str, List[Dict[str, Any]]]:
        groups = {}
        for item in data:
            key = tuple(item.get(g, "unknown") for g in group_by)
            key_str = str(key)
            if key_str not in groups:
                groups[key_str] = []
            groups[key_str].append(item)
        return groups

    def _calculate_aggregates(self, group_data: List[Dict[str, Any]]) -> Dict[str, float]:
        values = [item.get("value", 0) for item in group_data if "value" in item]
        if not values:
            return {"count": 0}
        return {
            "sum": sum(values),
            "avg": sum(values) / len(values),
            "count": len(values),
            "min": min(values),
            "max": max(values)
        }

    def _sum_agg(self, values: List[float]) -> float:
        return sum(values)

    def _avg_agg(self, values: List[float]) -> float:
        return sum(values) / len(values) if values else 0

    def _count_agg(self, values: List[float]) -> float:
        return len(values)

    def _min_agg(self, values: List[float]) -> float:
        return min(values) if values else 0

    def _max_agg(self, values: List[float]) -> float:
        return max(values) if values else 0

    def transform_data(self, data: List[Dict[str, Any]], transforms: List[str]) -> List[Dict[str, Any]]:
        result = data
        for transform in transforms:
            if transform == "normalize":
                result = self._normalize_values(result)
            elif transform == "standardize":
                result = self._standardize_values(result)
        return result

    def _normalize_values(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        values = [item.get("value", 0) for item in data if "value" in item]
        if not values:
            return data
        min_val, max_val = min(values), max(values)
        if max_val == min_val:
            return data
        for item in data:
            if "value" in item:
                item["normalized"] = (item["value"] - min_val) / (max_val - min_val)
        return data

    def _standardize_values(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        values = [item.get("value", 0) for item in data if "value" in item]
        if not values:
            return data
        mean = sum(values) / len(values)
        variance = sum((v - mean) ** 2 for v in values) / len(values)
        std = variance ** 0.5
        if std == 0:
            return data
        for item in data:
            if "value" in item:
                item["standardized"] = (item["value"] - mean) / std
        return data

    def validate_data(self, data: List[Dict[str, Any]], rules: Dict[str, Any]) -> Dict[str, Any]:
        result = ProcessResultDto(success=True)
        for item in data:
            errors = self._validate_item(item, rules)
            if errors:
                result.success = False
                result.errors.extend(errors)
        return {
            "success": result.success,
            "errors": result.errors,
            "validated_count": len(data)
        }

    def _validate_item(self, item: Dict[str, Any], rules: Dict[str, Any]) -> List[str]:
        errors = []
        if "required_fields" in rules:
            for field in rules["required_fields"]:
                if field not in item:
                    errors.append(f"Missing required field: {field}")
        if "value_range" in rules:
            if "value" in item:
                min_val, max_val = rules["value_range"]
                if not (min_val <= item["value"] <= max_val):
                    errors.append(f"Value {item['value']} out of range")
        return errors


def create_data_process() -> IDataProcess:
    return _DataProcessImpl()
