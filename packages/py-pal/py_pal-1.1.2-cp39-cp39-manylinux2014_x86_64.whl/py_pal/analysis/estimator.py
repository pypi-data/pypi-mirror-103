import abc
import warnings
from abc import ABC
from typing import List, Tuple, Union

import numpy as np
import pandas
import pandas as pd
from numpy.linalg import LinAlgError
from pandas import DataFrame

from py_pal.analysis.complexity import ALL_CLASSES, UnderDeterminedEquation, Complexity
from py_pal.util import Columns, setup_logging, normalize_column

logger = setup_logging(__name__)


class Estimator(ABC):
    """
    Base class which provides functionality to transform statistics collected by the
    :class:`py_pal.data_collection.Tracer` to :class:`pandas.DataFrame` objects, ways to aggregate opcode statistics per
    function call and fit the :class:`py_pal.analysis.complexity` classes.
    """

    def __init__(self, call_stats: np.ndarray, opcode_stats: np.ndarray, per_line: bool = False):
        self.call_stats = call_stats
        self.opcode_stats = opcode_stats
        self.per_line = per_line
        self.df_tracer_calls = [
            Columns.CALL_ID, Columns.FUNCTION_ID, Columns.FILE, Columns.FUNCTION_LINE, Columns.FUNCTION_NAME,
            Columns.ARGS_NAMES, Columns.ARGS_PROXY, Columns.KWARGS_NAMES, Columns.KWARGS_PROXY,
            Columns.VARARGS_NAMES, Columns.VARARGS_PROXY, Columns.VARKW_NAMES, Columns.VARKW_PROXY,
        ]
        self.df_tracer_opcodes = [Columns.CALL_ID, Columns.LINE, Columns.OPCODE_WEIGHT]
        self.df_analyze_order = [
            Columns.FILE, Columns.FUNCTION_LINE, Columns.FUNCTION_NAME, Columns.ARG_DEP, Columns.COMPLEXITY,
            Columns.DATA_POINTS, Columns.TRACING_DATA, Columns.NORM_OPCODE_SCALE
        ]
        self.df_export_output_order = [
            Columns.FUNCTION_NAME, Columns.ARG_DEP, Columns.COMPLEXITY, Columns.FUNCTION_LINE, Columns.FILE,
            Columns.DATA_POINTS, Columns.TRACING_DATA, Columns.NORM_OPCODE_SCALE
        ]

    @property
    def calls(self) -> pd.DataFrame:
        data_frame = DataFrame(columns=self.df_tracer_calls, data=self.call_stats)

        # Remove columns if arguments are not present
        data_frame.dropna(axis=1, how='all', inplace=True)
        logger.info(f"Received {len(data_frame)} rows of call entries.")
        return data_frame

    @property
    def opcodes(self) -> pd.DataFrame:
        if self.opcode_stats.size == 0:
            # Opcode statistics can be empty if no opcode executions are traced
            return DataFrame(columns=self.df_tracer_opcodes)

        data_frame = DataFrame(columns=self.df_tracer_opcodes, data=self.opcode_stats)
        logger.info(f"Received {len(data_frame)} rows of opcode statistics.")
        return data_frame

    # Data transformation
    def aggregate_opcodes_per_target(self, target: List[Columns]) -> pd.DataFrame:
        # Sum opcode weights and map them to their respective calls.
        opcodes = self.opcodes
        calls = self.calls

        if opcodes.empty or calls.empty:
            logger.info("Empty opcode or call statistics.")
            return DataFrame()

        opcode_sum = opcodes.groupby(target)[Columns.OPCODE_WEIGHT].agg(OpcodeWeight=np.sum).reset_index()
        data_frame = pd.merge(calls, opcode_sum, on=Columns.CALL_ID)
        data_frame.drop_duplicates(inplace=True)
        logger.info(f"Aggregated {len(data_frame)} rows of opcode statistics.")
        return data_frame

    def group_opcodes_by_call(self, data: pd.DataFrame, group_by: List[Columns], result_columns: List[Columns]) -> \
            Tuple[str, int, str, List[str], pd.DataFrame, float]:
        logger.info(f"Grouping opcodes by {group_by}")
        for _, data_frame in data.groupby(group_by, sort=False):
            slice = DataFrame.copy(data_frame)
            filename = slice[Columns.FILE].to_numpy()[0]
            line = slice[Columns.LINE if self.per_line else Columns.FUNCTION_LINE].to_numpy()[0]
            function = slice[Columns.FUNCTION_NAME].to_numpy()[0]
            if Columns.ARGS_NAMES in slice:
                arg_names = slice[Columns.ARGS_NAMES].to_numpy()[0]
            else:
                arg_names = None

            # Normalize opcode weights for least squares
            normalized_col, scale = normalize_column(slice[Columns.OPCODE_WEIGHT])
            slice[Columns.NORM_OPCODE_WEIGHT] = normalized_col

            if all(map(lambda x: x in slice, result_columns)):
                data_frame_out = slice[result_columns]
            else:
                data_frame_out = DataFrame()

            logger.debug(f"Processed call: {function}, args: {arg_names}, rows: {len(data_frame_out)}, scale: {scale}")
            yield filename, line, function, arg_names, data_frame_out, scale

    @property
    def iterator(self) -> Tuple[str, int, str, List[str], pd.DataFrame, float]:
        if self.per_line:
            aggregated_opcodes = self.aggregate_opcodes_per_target([Columns.CALL_ID, Columns.LINE])
            if aggregated_opcodes.empty:
                raise StopIteration()
            return self.group_opcodes_by_call(
                aggregated_opcodes,
                [Columns.FUNCTION_ID, Columns.LINE],
                [Columns.ARGS_PROXY, Columns.NORM_OPCODE_WEIGHT, Columns.OPCODE_WEIGHT, Columns.LINE]
            )
        aggregated_opcodes = self.aggregate_opcodes_per_target(Columns.CALL_ID)
        if aggregated_opcodes.empty:
            raise StopIteration()
        return self.group_opcodes_by_call(
            aggregated_opcodes,
            [Columns.FUNCTION_ID],
            [Columns.ARGS_PROXY, Columns.NORM_OPCODE_WEIGHT, Columns.OPCODE_WEIGHT]
        )

    @staticmethod
    def infer_complexity(data_frame: pd.DataFrame, arg_column: Columns) -> Complexity:
        """
        Derive the big O complexity class.

        Arguments:
            arg_column(:class:`py_pal.util.Columns`): Argument column to use as x-axis.
            data_frame(:class:`pandas.DataFrame`): Time series-like data, x-axis is argument size, y-axis is executed \
                opcodes.
        Returns:
             :class:`py_pal.analysis.complexity.Complexity`: Best fitting complexity class
        """
        best_class = None
        best_residuals = np.inf
        fitted = {}

        for _class in ALL_CLASSES:
            inst = _class()

            x = data_frame[arg_column].to_numpy().astype(float)
            y = data_frame[Columns.NORM_OPCODE_WEIGHT].to_numpy().astype(float)
            logger.debug(f"Fit complexity class: {_class}")
            logger.debug(x)
            logger.debug(y)

            try:
                residuals = inst.fit(x, y)

                fitted[inst] = residuals

                if residuals < best_residuals - 1e-6:
                    best_residuals = residuals
                    best_class = inst

            except (LinAlgError, UnderDeterminedEquation) as exception:
                logger.debug(
                    f"Encountered exception in complexity calculation: {exception.__class__.__name__}('{exception}')"
                )
                if not best_class:
                    best_class = exception

        logger.debug(f"Best fitting complexity class: {best_class}")
        return best_class

    def analyze(self) -> Tuple[str, int, str, List[str], Complexity, int, pd.DataFrame, float]:
        logger.info('%s(per_line=%s)', self.__class__.__name__, self.per_line)

        try:
            for filename, function_line, function, _arg_names, data_frame, scale in self.iterator:
                for arg_names, complexity, data_points in self.infer_complexity_per_argument(data_frame, _arg_names):
                    yield filename, function_line, function, arg_names, complexity, len(data_points), data_points, scale

        except StopIteration:
            warnings.warn("Empty opcode statistics, how did you do that?", UserWarning)

    @abc.abstractmethod
    def infer_complexity_per_argument(self, data_frame: pd.DataFrame, arg_names: List[str]) -> \
            Tuple[List[str], Complexity, pd.DataFrame]:
        """Abstract method definition for the data transformation function. The implementation prepares the dataset for
        evaluation with the least squares method. The dataset is transformed with respect to the arguments (their proxy
        value) of the function. Finally, :meth:`py_pal.analysis.estimator.infer_complexity` is executed and the result
        is returned.

            Arguments:
                data_frame (:class:`pandas.DataFrame`): dataset
                arg_names (List[str]): argument names of function

            Returns:
                :class:`pandas.DataFrame`: arguments considered in the analysis, estimated complexity class and the \
                    data considered in the analysis
        """
        raise NotImplementedError()

    def export(self) -> pd.DataFrame:
        """Export results. The output order can be controlled with `df_analyze_order`."""
        data_frame = DataFrame(self.analyze(), columns=self.df_analyze_order)
        return data_frame[self.df_export_output_order]


class AllArgumentEstimator(Estimator):
    """
    :class:`py_pal.analysis.estimator` implementation that treats all arguments as one by averaging out the proxy
    value of all arguments.
    """

    def infer_complexity_per_argument(self, data_frame: pd.DataFrame, arg_names: List[str]) -> Tuple[
            List[str], Union[Exception, Complexity], pd.DataFrame]:
        """View all argument axes together and sort argument proxy value ascending"""
        if Columns.ARGS_PROXY not in data_frame:
            return None, DataFrame()

        args_df = pd.DataFrame(data_frame[Columns.ARGS_PROXY].tolist(), index=data_frame.index)
        args_df[Columns.MEAN] = args_df.mean(axis=1)
        args_df[Columns.NORM_OPCODE_WEIGHT] = data_frame[Columns.NORM_OPCODE_WEIGHT]

        # Take average of ArgProxy values and opcode weights
        if not args_df.empty:
            args_df = args_df.groupby(Columns.MEAN)[Columns.NORM_OPCODE_WEIGHT].mean().reset_index()
            args_df.sort_values(Columns.MEAN, inplace=True)

        logger.debug(f"Infer complexity for all arguments in {arg_names}")
        yield arg_names, self.infer_complexity(args_df, Columns.MEAN), \
            args_df[[Columns.MEAN, Columns.NORM_OPCODE_WEIGHT]]


class SeparateArgumentEstimator(Estimator):
    """Voodoo :class:`py_pal.analysis.estimator` that tries to infer complexity for each argument separately. Even
    though the influence of arguments on each other is minimized this may not produce reliable results and therefore
    should be viewed as experimental.
    """

    def analyze_args_separate_ascending(self, data_frame: pd.DataFrame):
        # View separate argument axes and sort argument proxy value ascending
        for column in data_frame:
            if column == Columns.NORM_OPCODE_WEIGHT:
                continue

            # Keep influence of other arguments as low as possible by selecting rows with smallest proxy value
            args_columns = data_frame.columns.to_list()[:-1]
            data_frame = data_frame.sort_values(args_columns)
            data_frame.drop_duplicates([column, Columns.NORM_OPCODE_WEIGHT], keep='first', inplace=True)
            yield self.infer_complexity(data_frame, column), column, data_frame[[column, Columns.NORM_OPCODE_WEIGHT]]

    @staticmethod
    def unpack_tuples(data_frame: pd.DataFrame):
        # Unpack tuples of arguments
        _slice = data_frame.copy()
        _slice.dropna(subset=[Columns.ARGS_PROXY], inplace=True)
        unpacked_data_frame = pd.DataFrame(zip(*_slice[Columns.ARGS_PROXY])).transpose()
        unpacked_data_frame[Columns.NORM_OPCODE_WEIGHT] = _slice[Columns.NORM_OPCODE_WEIGHT]
        unpacked_data_frame.dropna(inplace=True, )
        return unpacked_data_frame

    @staticmethod
    def map_arg_names(pos, names: List[str]):
        if not names:
            return ""
        if isinstance(pos, int):
            return names[pos]
        return list(map(lambda x: names[x], pos))

    def infer_complexity_per_argument(self, data_frame: pd.DataFrame, arg_names: List[str]):
        """Try to look at each argument individually and sort the argument proxy value in ascending order."""
        warnings.warn("You are using an experimental feature.", UserWarning)

        if Columns.ARGS_PROXY not in data_frame:
            return None, DataFrame()

        args_df = self.unpack_tuples(data_frame)

        for best, arg_pos, data_points in self.analyze_args_separate_ascending(args_df):
            yield self.map_arg_names(arg_pos, arg_names), best, data_points
