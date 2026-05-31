from .DataCore import DataCore, create_data_core
from .ViewCore import ViewCore, create_view_core


class DataVistaSystem:
    def __init__(self):
        self.data_core = create_data_core()
        self.view_core = create_view_core(self.data_core)

    def get_system_info(self):
        return {
            "name": "DataVistaSystem",
            "version": "1.0.0",
            "architecture": "Binary Tree V2.0"
        }


def create_dataview_system():
    return DataVistaSystem()


__all__ = ["DataVistaSystem", "create_dataview_system", "DataCore", "ViewCore"]
