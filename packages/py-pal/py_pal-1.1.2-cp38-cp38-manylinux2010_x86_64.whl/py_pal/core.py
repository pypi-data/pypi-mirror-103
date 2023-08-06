import os
import sys
from functools import wraps
from sys import gettrace
from typing import List, Any

import numpy as np
from py_pal.data_collection.opcode_metric import OpcodeMetric
from py_pal.data_collection.tracer import Tracer

from py_pal.analysis.complexity import Complexity, UnderDeterminedEquation
from py_pal.analysis.estimator import AllArgumentEstimator
from py_pal.export import write_files
from py_pal.util import setup_logging, Columns

logger = setup_logging(__name__)


class DecoratorStore(object):
    """Data storage class to collect profiling information with the decorator."""
    CALLS = []
    OPCODES = []

    @classmethod
    def reset(cls) -> None:
        cls.CALLS = []
        cls.OPCODES = []

    @classmethod
    def get_call_stats(cls) -> np.ndarray:
        logger.info(f"Combining {len(cls.CALLS)} call statistics.")
        return np.vstack(cls.CALLS)

    @classmethod
    def get_opcode_stats(cls) -> np.ndarray:
        logger.info(f"Combining {len(cls.OPCODES)} opcode statistics.")
        return np.vstack(cls.OPCODES)


def profile(function_to_trace=None, **trace_options):
    """Implementation of the decorator protocol for the :class:`py_pal.data_collection.tracer.Tracer`. If a function is
    annotated with `@profile` and is then called, profiling data is collected.
    """

    def tracing_decorator(func):
        @wraps(func)
        def tracing_wrapper(*args, **kwargs):
            logger.debug(f"Wrapping {func}({args},{kwargs}) with tracer")
            if gettrace():
                return func(*args, **kwargs)

            tracer = Tracer(**trace_options)
            tracer.trace()
            try:
                return func(*args, **kwargs)
            finally:
                tracer.stop()
                DecoratorStore.OPCODES.append(tracer.get_opcode_stats())
                DecoratorStore.CALLS.append(tracer.get_call_stats())

        return tracing_wrapper

    if function_to_trace is None:
        return tracing_decorator
    return tracing_decorator(function_to_trace)


def profile_function(metric: OpcodeMetric, arguments: List[List[Any]], function: Any,
                     estimator=AllArgumentEstimator, save_plot: bool = False,
                     save_statistics: bool = False) -> Complexity:
    tracer = Tracer(metric=metric)
    for arg in arguments:
        logger.debug(f"Tracing python function: {function}({arg})")
        try:
            tracer.trace()
            function(*arg)
        finally:
            tracer.stop()

    estimator = estimator(tracer.get_call_stats(), tracer.get_opcode_stats())
    result = estimator.export()

    write_files(result, function.__name__, save_plot=save_plot, save_statistics=save_statistics)

    row = result.loc[result[Columns.FUNCTION_NAME] == function.__name__]
    if row.empty:
        raise UnderDeterminedEquation
    return row[Columns.COMPLEXITY].to_numpy()[0]


def profile_python_file(file_path: str, args: List[str]) -> Tracer:
    with open(file_path) as f:
        file = f.read()

    code = compile(file, filename=file_path, mode='exec')
    _globals = globals()
    # Execute as direct call e.g. 'python example.py'
    _globals['__name__'] = '__main__'
    # Append path to enable module import resolution in client code
    sys.path.append(os.path.dirname(file_path))
    # Pass arguments
    sys.argv = [file_path, *args]
    tracer = Tracer()

    logger.info(f"Tracing python file: {file_path} with args: {args}")
    try:
        tracer.trace()
        exec(code, _globals, _globals)
    finally:
        tracer.stop()
        return tracer
