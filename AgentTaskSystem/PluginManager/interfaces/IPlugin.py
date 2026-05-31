"""
IPlugin 接口 - 插件标准接口
所有插件必须实现此接口
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, Any, List, Optional


class PluginType(Enum):
    """插件类型"""
    DATA_COLLECTION = "data_collection"      # 数据采集
    DATA_PROCESSING = "data_processing"      # 数据处理
    MONITORING = "monitoring"                # 监控告警
    NOTIFICATION = "notification"            # 通知推送
    STORAGE = "storage"                      # 数据存储
    AI_LLM = "ai_llm"                        # AI大模型
    WEB_SCRAPING = "web_scraping"            # 网页抓取
    FILE_OPERATION = "file_operation"        # 文件操作
    NETWORK = "network"                      # 网络请求
    DATABASE = "database"                    # 数据库
    CUSTOM = "custom"                        # 自定义


class IPlugin(ABC):
    """
    插件接口
    所有外部工具集插件必须实现此接口
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """插件名称"""
        pass

    @property
    @abstractmethod
    def version(self) -> str:
        """插件版本"""
        pass

    @property
    @abstractmethod
    def plugin_type(self) -> PluginType:
        """插件类型"""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """插件描述"""
        pass

    @property
    def dependencies(self) -> List[str]:
        """依赖的第三方库列表"""
        return []

    @abstractmethod
    def initialize(self, config: Dict[str, Any] = None) -> bool:
        """
        初始化插件

        Args:
            config: 插件配置参数

        Returns:
            初始化是否成功
        """
        pass

    @abstractmethod
    def execute(self, task_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行插件任务

        Args:
            task_params: 任务参数

        Returns:
            执行结果
        """
        pass

    @abstractmethod
    def health_check(self) -> bool:
        """
        健康检查

        Returns:
            插件是否健康
        """
        pass

    @abstractmethod
    def shutdown(self) -> bool:
        """
        关闭插件

        Returns:
            关闭是否成功
        """
        pass
