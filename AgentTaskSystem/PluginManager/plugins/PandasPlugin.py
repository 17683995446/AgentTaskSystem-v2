"""
PandasPlugin - 数据处理插件
基于 pandas，支持数据分析、CSV/Excel处理
"""

import json
from typing import Dict, Any, List
from ..interfaces.IPlugin import IPlugin, PluginType


class PandasPlugin(IPlugin):
    """
    数据处理插件
    功能: 数据分析、CSV读写、Excel处理、数据转换
    """

    @property
    def name(self) -> str:
        return "pandas_data"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def plugin_type(self) -> PluginType:
        return PluginType.DATA_PROCESSING

    @property
    def description(self) -> str:
        return "数据处理插件，支持CSV/Excel读写、数据分析、统计计算"

    @property
    def dependencies(self) -> List[str]:
        return ["pandas", "openpyxl"]

    def initialize(self, config: Dict[str, Any] = None) -> bool:
        import pandas as pd
        self.pd = pd
        self.config = config or {}
        return True

    def execute(self, task_params: Dict[str, Any]) -> Dict[str, Any]:
        action = task_params.get("action", "read_csv")

        if action == "read_csv":
            return self._read_csv(task_params)
        elif action == "write_csv":
            return self._write_csv(task_params)
        elif action == "read_excel":
            return self._read_excel(task_params)
        elif action == "analyze":
            return self._analyze(task_params)
        elif action == "filter":
            return self._filter(task_params)
        elif action == "aggregate":
            return self._aggregate(task_params)
        else:
            return {"error": f"不支持的操作: {action}"}

    def _read_csv(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """读取CSV"""
        filepath = params.get("filepath", "")
        if not filepath:
            return {"error": "文件路径不能为空"}

        try:
            df = self.pd.read_csv(filepath)
            return {
                "columns": list(df.columns),
                "rows": len(df),
                "preview": df.head(10).to_dict('records'),
                "summary": df.describe().to_dict()
            }
        except Exception as e:
            return {"error": str(e)}

    def _write_csv(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """写入CSV"""
        filepath = params.get("filepath", "")
        data = params.get("data", [])

        if not filepath or not data:
            return {"error": "文件路径和数据不能为空"}

        try:
            df = self.pd.DataFrame(data)
            df.to_csv(filepath, index=False)
            return {"success": True, "filepath": filepath, "rows": len(df)}
        except Exception as e:
            return {"error": str(e)}

    def _read_excel(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """读取Excel"""
        filepath = params.get("filepath", "")
        sheet = params.get("sheet", 0)

        if not filepath:
            return {"error": "文件路径不能为空"}

        try:
            df = self.pd.read_excel(filepath, sheet_name=sheet)
            return {
                "columns": list(df.columns),
                "rows": len(df),
                "preview": df.head(10).to_dict('records')
            }
        except Exception as e:
            return {"error": str(e)}

    def _analyze(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """数据分析"""
        data = params.get("data", [])
        if not data:
            return {"error": "数据不能为空"}

        try:
            df = self.pd.DataFrame(data)
            return {
                "shape": df.shape,
                "columns": list(df.columns),
                "dtypes": {k: str(v) for k, v in df.dtypes.items()},
                "describe": df.describe().to_dict(),
                "missing": df.isnull().sum().to_dict(),
                "correlation": df.corr().to_dict() if len(df.select_dtypes(include=['number']).columns) > 1 else {}
            }
        except Exception as e:
            return {"error": str(e)}

    def _filter(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """数据过滤"""
        data = params.get("data", [])
        condition = params.get("condition", "")

        if not data or not condition:
            return {"error": "数据和条件不能为空"}

        try:
            df = self.pd.DataFrame(data)
            filtered = df.query(condition)
            return {
                "original_rows": len(df),
                "filtered_rows": len(filtered),
                "result": filtered.to_dict('records')
            }
        except Exception as e:
            return {"error": str(e)}

    def _aggregate(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """数据聚合"""
        data = params.get("data", [])
        group_by = params.get("group_by", "")
        agg_func = params.get("agg_func", "sum")

        if not data or not group_by:
            return {"error": "数据和分组字段不能为空"}

        try:
            df = self.pd.DataFrame(data)
            result = df.groupby(group_by).agg(agg_func).reset_index()
            return {
                "result": result.to_dict('records'),
                "groups": len(result)
            }
        except Exception as e:
            return {"error": str(e)}

    def health_check(self) -> bool:
        try:
            import pandas as pd
            df = pd.DataFrame({"a": [1, 2, 3]})
            return len(df) == 3
        except:
            return False

    def shutdown(self) -> bool:
        return True
