"""
AgentTaskSystem Plugin Manager - 插件管理器
支持引入外部开源工具集，扩展系统能力
"""

from .interfaces.IPlugin import IPlugin, PluginType
from .impl.PluginManagerImpl import PluginManagerImpl, create_plugin_manager

__all__ = [
    "IPlugin",
    "PluginType",
    "PluginManagerImpl",
    "create_plugin_manager"
]
