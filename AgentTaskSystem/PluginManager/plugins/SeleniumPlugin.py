"""
SeleniumPlugin - 浏览器自动化插件
基于 selenium，支持网页自动化、截图、表单填写
"""

from typing import Dict, Any, List
from ..interfaces.IPlugin import IPlugin, PluginType


class SeleniumPlugin(IPlugin):
    """
    浏览器自动化插件
    功能: 网页截图、表单填写、元素点击、页面导航
    """

    @property
    def name(self) -> str:
        return "selenium_browser"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def plugin_type(self) -> PluginType:
        return PluginType.WEB_SCRAPING

    @property
    def description(self) -> str:
        return "浏览器自动化插件，支持网页截图、表单操作、元素交互"

    @property
    def dependencies(self) -> List[str]:
        return ["selenium"]

    def initialize(self, config: Dict[str, Any] = None) -> bool:
        self.config = config or {}
        self.driver = None
        return True

    def _get_driver(self):
        """获取浏览器驱动"""
        if self.driver is None:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options

            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")

            self.driver = webdriver.Chrome(options=chrome_options)

        return self.driver

    def execute(self, task_params: Dict[str, Any]) -> Dict[str, Any]:
        action = task_params.get("action", "screenshot")

        if action == "screenshot":
            return self._screenshot(task_params)
        elif action == "navigate":
            return self._navigate(task_params)
        elif action == "click":
            return self._click(task_params)
        elif action == "fill_form":
            return self._fill_form(task_params)
        elif action == "get_text":
            return self._get_text(task_params)
        else:
            return {"error": f"不支持的操作: {action}"}

    def _screenshot(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """网页截图"""
        url = params.get("url", "")
        output = params.get("output", "screenshot.png")

        if not url:
            return {"error": "URL不能为空"}

        try:
            driver = self._get_driver()
            driver.get(url)
            driver.save_screenshot(output)
            return {"success": True, "output": output, "url": url}
        except Exception as e:
            return {"error": str(e)}

    def _navigate(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """页面导航"""
        url = params.get("url", "")

        if not url:
            return {"error": "URL不能为空"}

        try:
            driver = self._get_driver()
            driver.get(url)
            return {
                "success": True,
                "url": url,
                "title": driver.title,
                "current_url": driver.current_url
            }
        except Exception as e:
            return {"error": str(e)}

    def _click(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """点击元素"""
        selector = params.get("selector", "")
        by = params.get("by", "css_selector")

        if not selector:
            return {"error": "选择器不能为空"}

        try:
            from selenium.webdriver.common.by import By

            driver = self._get_driver()
            by_map = {
                "css_selector": By.CSS_SELECTOR,
                "id": By.ID,
                "xpath": By.XPATH,
                "class_name": By.CLASS_NAME
            }

            element = driver.find_element(by_map.get(by, By.CSS_SELECTOR), selector)
            element.click()

            return {"success": True, "selector": selector}
        except Exception as e:
            return {"error": str(e)}

    def _fill_form(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """填写表单"""
        fields = params.get("fields", {})

        if not fields:
            return {"error": "表单字段不能为空"}

        try:
            from selenium.webdriver.common.by import By

            driver = self._get_driver()
            results = []

            for selector, value in fields.items():
                element = driver.find_element(By.CSS_SELECTOR, selector)
                element.clear()
                element.send_keys(value)
                results.append({"selector": selector, "value": value})

            return {"success": True, "filled_fields": results}
        except Exception as e:
            return {"error": str(e)}

    def _get_text(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """获取元素文本"""
        selector = params.get("selector", "")

        try:
            from selenium.webdriver.common.by import By

            driver = self._get_driver()

            if selector:
                element = driver.find_element(By.CSS_SELECTOR, selector)
                text = element.text
            else:
                text = driver.find_element(By.TAG_NAME, "body").text

            return {"success": True, "text": text[:2000]}
        except Exception as e:
            return {"error": str(e)}

    def health_check(self) -> bool:
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            return True
        except:
            return False

    def shutdown(self) -> bool:
        if self.driver:
            self.driver.quit()
            self.driver = None
        return True
