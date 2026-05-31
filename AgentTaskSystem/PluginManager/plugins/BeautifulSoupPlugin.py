"""
BeautifulSoupPlugin - 网页解析插件
基于 beautifulsoup4，支持网页抓取和数据提取
"""

import requests
from bs4 import BeautifulSoup
from typing import Dict, Any, List
from ..interfaces.IPlugin import IPlugin, PluginType


class BeautifulSoupPlugin(IPlugin):
    """
    网页解析插件
    功能: 网页抓取、HTML解析、数据提取
    """

    @property
    def name(self) -> str:
        return "beautifulsoup_scraper"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def plugin_type(self) -> PluginType:
        return PluginType.WEB_SCRAPING

    @property
    def description(self) -> str:
        return "网页抓取插件，支持HTML解析、CSS选择器、数据提取"

    @property
    def dependencies(self) -> List[str]:
        return ["beautifulsoup4", "requests"]

    def initialize(self, config: Dict[str, Any] = None) -> bool:
        self.config = config or {}
        return True

    def execute(self, task_params: Dict[str, Any]) -> Dict[str, Any]:
        action = task_params.get("action", "scrape")

        if action == "scrape":
            return self._scrape(task_params)
        elif action == "parse":
            return self._parse_html(task_params)
        elif action == "extract_links":
            return self._extract_links(task_params)
        elif action == "extract_text":
            return self._extract_text(task_params)
        else:
            return {"error": f"不支持的操作: {action}"}

    def _scrape(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """抓取网页"""
        url = params.get("url", "")
        selector = params.get("selector", "")

        if not url:
            return {"error": "URL不能为空"}

        try:
            response = requests.get(url, timeout=30)
            soup = BeautifulSoup(response.text, 'html.parser')

            result = {
                "title": soup.title.string if soup.title else "",
                "url": url,
            }

            if selector:
                elements = soup.select(selector)
                result["elements"] = [str(el) for el in elements]
                result["count"] = len(elements)
            else:
                result["text"] = soup.get_text(strip=True)[:2000]

            return result

        except Exception as e:
            return {"error": str(e)}

    def _parse_html(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """解析HTML"""
        html = params.get("html", "")
        selector = params.get("selector", "")

        if not html:
            return {"error": "HTML内容不能为空"}

        try:
            soup = BeautifulSoup(html, 'html.parser')
            elements = soup.select(selector) if selector else []

            return {
                "text": soup.get_text(strip=True)[:2000],
                "elements_count": len(elements),
                "elements": [str(el) for el in elements[:10]]
            }

        except Exception as e:
            return {"error": str(e)}

    def _extract_links(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """提取链接"""
        url = params.get("url", "")

        try:
            response = requests.get(url, timeout=30)
            soup = BeautifulSoup(response.text, 'html.parser')

            links = []
            for a in soup.find_all('a', href=True):
                links.append({
                    "text": a.get_text(strip=True),
                    "href": a['href']
                })

            return {
                "url": url,
                "links_count": len(links),
                "links": links[:50]
            }

        except Exception as e:
            return {"error": str(e)}

    def _extract_text(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """提取文本"""
        url = params.get("url", "")

        try:
            response = requests.get(url, timeout=30)
            soup = BeautifulSoup(response.text, 'html.parser')

            for script in soup(["script", "style"]):
                script.decompose()

            text = soup.get_text(separator='\n', strip=True)
            lines = [line.strip() for line in text.split('\n') if line.strip()]

            return {
                "url": url,
                "text": '\n'.join(lines[:100]),
                "lines_count": len(lines)
            }

        except Exception as e:
            return {"error": str(e)}

    def health_check(self) -> bool:
        try:
            html = "<html><body><p>Test</p></body></html>"
            soup = BeautifulSoup(html, 'html.parser')
            return soup.p.string == "Test"
        except:
            return False

    def shutdown(self) -> bool:
        return True
