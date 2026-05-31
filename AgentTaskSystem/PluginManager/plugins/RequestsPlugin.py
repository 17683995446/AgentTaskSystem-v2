"""
RequestsPlugin - HTTP请求插件
基于 requests 库，支持各种网络请求
"""

import requests
from typing import Dict, Any, List
from ..interfaces.IPlugin import IPlugin, PluginType


class RequestsPlugin(IPlugin):
    """
    HTTP请求插件
    功能: GET/POST/PUT/DELETE 请求、下载文件、API调用
    """

    @property
    def name(self) -> str:
        return "requests_http"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def plugin_type(self) -> PluginType:
        return PluginType.NETWORK

    @property
    def description(self) -> str:
        return "HTTP请求插件，支持GET/POST/PUT/DELETE，可用于调用API、下载文件"

    @property
    def dependencies(self) -> List[str]:
        return ["requests"]

    def initialize(self, config: Dict[str, Any] = None) -> bool:
        self.config = config or {}
        self.session = requests.Session()
        self.session.headers.update(self.config.get("headers", {}))
        return True

    def execute(self, task_params: Dict[str, Any]) -> Dict[str, Any]:
        method = task_params.get("method", "GET").upper()
        url = task_params.get("url", "")
        params = task_params.get("params", {})
        data = task_params.get("data", {})
        headers = task_params.get("headers", {})
        timeout = task_params.get("timeout", 30)

        if not url:
            return {"error": "URL不能为空"}

        try:
            if method == "GET":
                response = self.session.get(url, params=params, headers=headers, timeout=timeout)
            elif method == "POST":
                response = self.session.post(url, json=data, headers=headers, timeout=timeout)
            elif method == "PUT":
                response = self.session.put(url, json=data, headers=headers, timeout=timeout)
            elif method == "DELETE":
                response = self.session.delete(url, headers=headers, timeout=timeout)
            else:
                return {"error": f"不支持的HTTP方法: {method}"}

            result = {
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "content": response.text
            }

            try:
                result["json"] = response.json()
            except:
                pass

            return result

        except Exception as e:
            return {"error": str(e)}

    def health_check(self) -> bool:
        try:
            response = requests.get("https://httpbin.org/get", timeout=5)
            return response.status_code == 200
        except:
            return False

    def shutdown(self) -> bool:
        self.session.close()
        return True
