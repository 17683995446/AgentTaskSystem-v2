"""
AgentTaskSystem 内置插件集合
"""

from .RequestsPlugin import RequestsPlugin
from .BeautifulSoupPlugin import BeautifulSoupPlugin
from .PandasPlugin import PandasPlugin
from .SeleniumPlugin import SeleniumPlugin
from .SchedulePlugin import SchedulePlugin
from .EmailPlugin import EmailPlugin

__all__ = [
    "RequestsPlugin",
    "BeautifulSoupPlugin",
    "PandasPlugin",
    "SeleniumPlugin",
    "SchedulePlugin",
    "EmailPlugin"
]
