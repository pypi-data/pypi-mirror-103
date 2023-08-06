import argparse
import logging
import string
from typing import Tuple

import pandas as pd


def set_log_level(level):
    loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
    for logger in loggers:
        logger.setLevel(level)


def setup_logging(module, level=logging.WARNING):
    logging.basicConfig(level=level)
    logger = logging.getLogger(module)
    logger.setLevel(level)

    ch = logging.StreamHandler()
    ch.setLevel(level)

    formatter = logging.Formatter('[%(levelname)s, %(module)s, %(funcName)s]: %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger


logger = setup_logging(__name__)


def check_positive(value):
    int_value = int(value)
    if int_value <= 0:
        raise argparse.ArgumentTypeError("%s is an invalid positive int value" % value)
    return int_value


def scale_column(data_frame: pd.DataFrame, scale: float):
    return data_frame.apply(lambda x: x * scale)


def normalize_column(data_frame: pd.DataFrame) -> Tuple[pd.DataFrame, float]:
    _min = data_frame.min()
    _max = data_frame.max()
    div = _max - _min
    if _max == _min:
        div = _max
    logger.debug(f"Normalizing column with factor (x - {_min}) / {div}.")
    return data_frame.apply(lambda x: (x - _min) / div), div


VALID_CHARS = "-_.() %s%s" % (string.ascii_letters, string.digits)


def escape(filename):
    filename_escaped = ''.join(c for c in filename if c in VALID_CHARS)
    filename_escaped = filename_escaped.replace(' ', '_')
    return filename_escaped


class Columns:
    """Column names for the :class:`pandas.DataFrame` objects used in the :class:`py_pal.analysis.estimator.Estimator`
    classes."""
    CALL_ID = 'CallID'
    FILE = 'File'
    FUNCTION_NAME = 'FunctionName'
    ARGS_PROXY = 'ArgsProxy'
    ARGS_NAMES = 'Args'
    KWARGS_PROXY = 'KwargsProxy'
    KWARGS_NAMES = 'Kwargs'
    VARARGS_PROXY = 'VarArgsProxy'
    VARARGS_NAMES = 'VarArgs'
    VARKW_PROXY = 'VarKwProxy'
    VARKW_NAMES = 'VarKw'
    LINE = 'Line'
    FUNCTION_LINE = 'FunctionLine'
    OPCODE_WEIGHT = 'OpcodeWeight'
    NORM_OPCODE_WEIGHT = 'NormOpcodeWeight'
    NORM_OPCODE_SCALE = 'NormOpcodeScale'
    ARG_DEP = 'DependentArgs'
    COMPLEXITY = 'Complexity'
    DATA_POINTS = 'DataPoints'
    TRACING_DATA = 'TracingData'
    FUNCTION_ID = 'FunctionID'
    MEAN = 'Mean'


levels = {
    'critical': logging.CRITICAL,
    'error': logging.ERROR,
    'warn': logging.WARNING,
    'warning': logging.WARNING,
    'info': logging.INFO,
    'debug': logging.DEBUG
}
