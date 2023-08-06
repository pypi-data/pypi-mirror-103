import os
from pathlib import Path

import pandas as pd
from matplotlib import pyplot as plt

from py_pal.analysis.complexity import Complexity
from py_pal.settings import PandasOutputFormat, Settings
from py_pal.util import Columns, scale_column, escape


def plot_data_points(data_frame):
    # Add subplot
    plt.cla()

    tracing_data = data_frame[Columns.TRACING_DATA]
    current_axis = plt.gca()
    x_axis = tracing_data.columns[0]
    tracing_data[Columns.NORM_OPCODE_WEIGHT] = scale_column(
        tracing_data[Columns.NORM_OPCODE_WEIGHT],
        data_frame[Columns.NORM_OPCODE_SCALE]
    )
    tracing_data.plot(
        x=x_axis,
        y=Columns.NORM_OPCODE_WEIGHT,
        kind='scatter',
        title="Function: {}, Args: {}".format(data_frame[Columns.FUNCTION_NAME], data_frame[Columns.ARG_DEP]),
        ax=current_axis,
    )
    x_values = tracing_data[x_axis].to_numpy()
    complexity = data_frame[Columns.COMPLEXITY]
    current_axis.plot(
        x_values,
        scale_column(pd.DataFrame(complexity.compute(x_values)), data_frame[Columns.NORM_OPCODE_SCALE]).to_numpy(),
        color='red'
    )
    return plt


def write_statistics(data_frame: pd.DataFrame, filename: str, format: PandasOutputFormat = Settings.FORMAT_STATISTICS,
                     output_dir: str = Settings.OUTPUT_DIR):
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    data_frame[[Columns.TRACING_DATA]] = [
        x if isinstance(x, list) else [tuple(x) for x in x.to_numpy()] for x in data_frame[Columns.TRACING_DATA]
    ]

    if format == PandasOutputFormat.CSV:
        data_frame.to_csv(Path(output_dir) / "{}.{}".format(filename, format.value), sep=";")
    else:
        data_frame.to_html(Path(output_dir) / "{}.{}".format(filename, format.value))


def write_plots(original_df, output_dir=Settings.OUTPUT_DIR, plot_format=Settings.FORMAT_PLOT):
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    original_df['Plot'] = [""] * len(original_df)
    filtered_df = original_df[[isinstance(x, Complexity) for x in original_df[Columns.COMPLEXITY]]]

    for index, filtered_df in filtered_df.iterrows():
        filename = "{}_{}_{}.{}".format(
            filtered_df[Columns.FUNCTION_NAME],
            filtered_df[Columns.ARG_DEP],
            index,
            plot_format
        )
        filename_escaped = escape(filename)
        plot = plot_data_points(filtered_df)
        plot.savefig(Path(output_dir) / filename_escaped)
        original_df.iloc[index, -1] = Path(output_dir) / filename_escaped


def show_function_complexity_plots(res, show=True):
    res = res[[isinstance(x, Complexity) for x in res[Columns.COMPLEXITY]]]
    for index, data_frame in res.iterrows():
        plot = plot_data_points(data_frame)
        if show:
            plot.show()
    return res


def write_files(df, target, save_statistics=False, statistics_output_dir=None,
                statistics_format=Settings.FORMAT_STATISTICS, save_plot=False, plot_output_dir=None,
                plot_format=Settings.FORMAT_PLOT):
    """Helper function to allow file output configuration via environment variables. Environment variables have the
    highest precedence."""
    env_plot_output_dir = os.getenv(Settings.ENV_SAVE_PLOTS)
    if env_plot_output_dir:
        plot_output_dir = env_plot_output_dir
        save_plot = True
    elif not plot_output_dir:
        plot_output_dir = Settings.OUTPUT_DIR

    if save_plot:
        write_plots(df, output_dir=plot_output_dir, plot_format=plot_format)

    env_statistics_output_dir = os.getenv(Settings.ENV_SAVE_STATISTICS)
    if env_statistics_output_dir:
        statistics_output_dir = env_statistics_output_dir
        save_statistics = True
    elif not statistics_output_dir:
        statistics_output_dir = Settings.OUTPUT_DIR

    if save_statistics:
        write_statistics(df, target, output_dir=statistics_output_dir, format=statistics_format)
