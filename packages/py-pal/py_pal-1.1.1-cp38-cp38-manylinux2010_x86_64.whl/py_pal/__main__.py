import argparse
import inspect
import sys

from py_pal.data_collection.tracer import Tracer

from py_pal import __version__
from py_pal.analysis.estimator import AllArgumentEstimator, SeparateArgumentEstimator
from py_pal.core import profile_python_file
from py_pal.export import save_statistics, plot_function_complexity
from py_pal.util import Columns, set_log_level, levels


def main():
    """Command line entry point."""
    assert sys.version_info >= (3, 7)

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--function', type=str, help='specify a function')
    parser.add_argument('-l', '--line', help='Calculate complexity for each line', action='store_true')
    parser.add_argument('-V', '--version', help='Output the package version', action='store_true')
    parser.add_argument('-v', '--visualize', help='Plot runtime graphs', action='store_true')
    parser.add_argument('-s', '--separate', help='Estimate function complexity for each argument', action='store_true')
    parser.add_argument('-o', '--out', type=str, help='Output directory', default='stats')
    parser.add_argument('--save', help='Save statistics', action='store_true')
    parser.add_argument(
        "--log-level",
        default="warning",
        help="Provide logging level. Example --log-level=debug, default='warning'",
    ),
    parser.add_argument('--format', type=str, help='Output format, possible types are: csv, html, excel, json',
                        default='csv')
    parser.add_argument('target', type=str, help='a Python file or import path', nargs='?')

    if len(sys.argv) == 1:
        # Display help message if no argument is supplied.
        parser.print_help(sys.stderr)
        return sys.exit(1)

    args, unknown_args = parser.parse_known_args()

    level = levels.get(args.log_level.lower())
    if level is None:
        raise ValueError(
            f"log level given: {args.log_level} -- must be one of: {' | '.join(levels.keys())}"
        )
    set_log_level(level)

    sys.path.insert(0, '.')

    if args.version:
        print(__version__)
        return

    function = None
    if args.function:
        function = getattr(__import__(args.target, fromlist=[args.function]), args.function)
        sys.argv = [inspect.getfile(function), *unknown_args]

    tracer = profile_python_file(args.target, unknown_args)

    if not function and not tracer:
        raise ValueError("File or function could not be loaded")

    if function:
        tracer = Tracer()
        try:
            tracer.trace()
            function()
        finally:
            tracer.stop()

    if args.separate:
        res = SeparateArgumentEstimator(tracer.get_call_stats(), tracer.get_opcode_stats(), per_line=args.line).export()
    else:
        res = AllArgumentEstimator(tracer.get_call_stats(), tracer.get_opcode_stats(), per_line=args.line).export()

    print(res[[
        Columns.FUNCTION_NAME, Columns.ARG_DEP, Columns.COMPLEXITY, Columns.FUNCTION_LINE, Columns.FILE,
        Columns.DATA_POINTS
    ]].to_string())

    if not args.save and args.visualize:
        plot_function_complexity(res)

    if args.save:
        save_statistics(res, args.out, args.target, args.format, args.visualize)


if __name__ == "__main__":
    main()
