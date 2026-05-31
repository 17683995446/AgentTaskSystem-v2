"""
PluginManagerImpl - 插件管理器实现
管理所有插件的注册、加载、执行
"""

import importlib
import subprocess
import sys
from typing import Dict, Any, List, Optional, Type
from datetime import datetime

from ..interfaces.IPlugin import IPlugin, PluginType


class PluginInfo:
    """插件信息"""

    def __init__(self, plugin: IPlugin, config: Dict[str, Any] = None):
        self.plugin = plugin
        self.config = config or {}
        self.enabled = True
        self.registered_at = datetime.now().isoformat()
        self.last_executed = None
        self.execution_count = 0
        self.error_count = 0


class PluginManagerImpl:
    """
    插件管理器
    负责插件的全生命周期管理
    """

    def __init__(self):
        self._plugins: Dict[str, PluginInfo] = {}
        self._plugins_by_type: Dict[PluginType, List[str]] = {
            pt: [] for pt in PluginType
        }
        print("✅ 插件管理器初始化完成")

    def register_plugin(self, plugin: IPlugin, config: Dict[str, Any] = None) -> bool:
        """
        注册插件

        Args:
            plugin: 插件实例
            config: 插件配置

        Returns:
            注册是否成功
        """
        try:
            # 检查依赖
            if not self._check_dependencies(plugin):
                print(f"❌ 插件 {plugin.name} 依赖检查失败")
                return False

            # 初始化插件
            if not plugin.initialize(config):
                print(f"❌ 插件 {plugin.name} 初始化失败")
                return False

            # 健康检查
            if not plugin.health_check():
                print(f"❌ 插件 {plugin.name} 健康检查失败")
                return False

            # 注册
            plugin_info = PluginInfo(plugin, config)
            self._plugins[plugin.name] = plugin_info
            self._plugins_by_type[plugin.plugin_type].append(plugin.name)

            print(f"✅ 插件注册成功: {plugin.name} v{plugin.version}")
            return True

        except Exception as e:
            print(f"❌ 插件 {plugin.name} 注册异常: {e}")
            return False

    def unregister_plugin(self, plugin_name: str) -> bool:
        """
        注销插件

        Args:
            plugin_name: 插件名称

        Returns:
            注销是否成功
        """
        if plugin_name not in self._plugins:
            print(f"⚠️ 插件 {plugin_name} 未注册")
            return False

        try:
            plugin_info = self._plugins[plugin_name]
            plugin = plugin_info.plugin

            # 关闭插件
            plugin.shutdown()

            # 移除注册
            del self._plugins[plugin_name]
            if plugin_name in self._plugins_by_type[plugin.plugin_type]:
                self._plugins_by_type[plugin.plugin_type].remove(plugin_name)

            print(f"✅ 插件 {plugin_name} 已注销")
            return True

        except Exception as e:
            print(f"❌ 插件 {plugin_name} 注销异常: {e}")
            return False

    def execute_plugin(self, plugin_name: str, task_params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        执行插件任务

        Args:
            plugin_name: 插件名称
            task_params: 任务参数

        Returns:
            执行结果
        """
        if plugin_name not in self._plugins:
            return {"success": False, "error": f"插件 {plugin_name} 未注册"}

        plugin_info = self._plugins[plugin_name]
        if not plugin_info.enabled:
            return {"success": False, "error": f"插件 {plugin_name} 已禁用"}

        try:
            plugin = plugin_info.plugin
            result = plugin.execute(task_params or {})

            plugin_info.last_executed = datetime.now().isoformat()
            plugin_info.execution_count += 1

            return {"success": True, "result": result}

        except Exception as e:
            plugin_info.error_count += 1
            return {"success": False, "error": str(e)}

    def get_plugin(self, plugin_name: str) -> Optional[IPlugin]:
        """获取插件实例"""
        if plugin_name in self._plugins:
            return self._plugins[plugin_name].plugin
        return None

    def list_plugins(self, plugin_type: PluginType = None) -> List[Dict[str, Any]]:
        """
        列出所有插件

        Args:
            plugin_type: 按类型筛选

        Returns:
            插件信息列表
        """
        result = []

        if plugin_type:
            plugin_names = self._plugins_by_type.get(plugin_type, [])
        else:
            plugin_names = list(self._plugins.keys())

        for name in plugin_names:
            info = self._plugins[name]
            result.append({
                "name": name,
                "version": info.plugin.version,
                "type": info.plugin.plugin_type.value,
                "description": info.plugin.description,
                "enabled": info.enabled,
                "registered_at": info.registered_at,
                "execution_count": info.execution_count,
                "error_count": info.error_count,
                "last_executed": info.last_executed
            })

        return result

    def enable_plugin(self, plugin_name: str) -> bool:
        """启用插件"""
        if plugin_name in self._plugins:
            self._plugins[plugin_name].enabled = True
            print(f"✅ 插件 {plugin_name} 已启用")
            return True
        return False

    def disable_plugin(self, plugin_name: str) -> bool:
        """禁用插件"""
        if plugin_name in self._plugins:
            self._plugins[plugin_name].enabled = False
            print(f"⏸️ 插件 {plugin_name} 已禁用")
            return True
        return False

    def _check_dependencies(self, plugin: IPlugin) -> bool:
        """检查并安装依赖"""
        if not plugin.dependencies:
            return True

        missing = []
        for dep in plugin.dependencies:
            try:
                importlib.import_module(dep.split('>=')[0].split('==')[0].strip())
            except ImportError:
                missing.append(dep)

        if missing:
            print(f"📦 插件 {plugin.name} 缺少依赖: {', '.join(missing)}")
            print(f"🔄 尝试自动安装...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "-q"] + missing)
                print(f"✅ 依赖安装完成")
                return True
            except Exception as e:
                print(f"❌ 依赖安装失败: {e}")
                return False

        return True

    def shutdown_all(self):
        """关闭所有插件"""
        print("🔄 正在关闭所有插件...")
        for name, info in list(self._plugins.items()):
            try:
                info.plugin.shutdown()
                print(f"✅ 插件 {name} 已关闭")
            except Exception as e:
                print(f"❌ 插件 {name} 关闭异常: {e}")

        self._plugins.clear()
        self._plugins_by_type = {pt: [] for pt in PluginType}
        print("✅ 所有插件已关闭")


def create_plugin_manager() -> PluginManagerImpl:
    """创建插件管理器"""
    return PluginManagerImpl()
