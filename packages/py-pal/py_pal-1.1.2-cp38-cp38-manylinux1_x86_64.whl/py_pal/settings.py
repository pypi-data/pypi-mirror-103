from enum import Enum


class PandasOutputFormat(Enum):
    CSV = 'csv'
    HTML = 'html'
    EXCEL = 'xlsx'
    JSON = 'json'

    def __str__(self):
        return self.value


class Settings(object):
    OUTPUT_DIR = 'stats'
    FORMAT_STATISTICS = PandasOutputFormat.CSV
    FORMAT_PLOT = 'png'
    ENV_SAVE_PLOTS = 'PYPAL_SAVE_PLOTS'
    ENV_SAVE_STATISTICS = 'PYPAL_SAVE_STATISTICS'
