from .DataDefine import IIndicatorDefine, IndicatorTypeEnum, create_indicator_define
from .DataProcess import IDataProcess, DataFormatEnum, create_data_process


class DataCore:
    def __init__(self):
        self.indicator_define = create_indicator_define()
        self.data_process = create_data_process()

    def get_components(self):
        return {
            "indicator_define": self.indicator_define,
            "data_process": self.data_process
        }


def create_data_core():
    return DataCore()


__all__ = ["DataCore", "create_data_core", "IIndicatorDefine", "IndicatorTypeEnum", "IDataProcess", "DataFormatEnum"]
