import numpy as np
from py_pal.data_collection.opcode_metric cimport AdvancedOpcodeMetric, OpcodeMetric
from py_pal.data_collection.proxy cimport get_input_factor
from py_pal.data_collection.arguments cimport getfullargs

from py_pal.util import setup_logging

logger = setup_logging(__name__)

cdef class TraceEvent:
    CALL = 0
    EXCEPTION = 1
    LINE = 2
    RETURN = 3
    C_CALL = 4
    C_EXCEPTION = 5
    C_RETURN = 6
    OPCODE = 7

cdef class Tracer:
    """Tracing hook manager implemented as Cython extension class :doc:`cython:src/tutorial/cdef_classes`."""
    def __init__(self, OpcodeMetric metric=AdvancedOpcodeMetric(), tuple ignore_modules=()):
        self.blacklist = [
            "py_pal",
            "py_pal.analysis.complexity",
            "py_pal.core",
            "py_pal.datagen",
            "py_pal.analysis.estimator",
            "py_pal.util",
            "py_pal.data_collection.arguments",
            "py_pal.data_collection.metric",
            "py_pal.data_collection.opcode_metric",
            "py_pal.data_collection.proxy",
            "py_pal.data_collection.tracer",
            *ignore_modules
        ]
        self.metric = metric
        self.call_id = 0
        self.calls = [(self.call_id, 0, '__main__', 0, '<module>', None, None, None, None, None, None, None, None)]
        self.opcodes = {}
        self.f_weight_map = {}
        self.call_stack = [(self.call_id, 0)]
        self.call_id += 1

    def __call__(self, FrameType frame, int what, object arg) -> Tracer:
        if frame.f_globals.get('__name__', '') not in self.blacklist:
            # Do not measure inside of tracing machinery
            self.trace()

        return self

    def trace(self) -> Tracer:
        """Install tracing hook."""
        PyEval_SetTrace(<Py_tracefunc> trace_func, <PyObject *> self)
        return self

    def stop(self):
        """Remove tracing hook."""
        PyEval_SetTrace(NULL, NULL)

    cpdef get_call_stats(self):
        """Return function call statistics.
            
        Returns:
            :class:`numpy.ndarray`: Set of function calls with arguments and meta information.
        """
        return np.asarray(self.calls)

    cpdef get_opcode_stats(self):
        """Return opcode statistics.
    
        Returns:
            :class:`numpy.ndarray`: Map of function call ids to opcode statistics.
        """
        return np.asarray([(*k, v) for k, v in self.opcodes.items()])

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

cdef int last_lineno

def trace_func_doc():
    """`trace_func` is the central data collection functionality. The function is called for specific events within a
    frame, documented in detail in :meth:`sys.settrace`. The events are emitted after the opcode execution. The `call`
    and `return` events are used to structure the calls into a hierarchy.
    The function is currently not accessible from Python. It is used by the 'tracer' class as a tracing hook.
    """
    pass

cdef int trace_func(Tracer self, FrameType frame, int what, PyObject *arg) except -1:
    frame.f_trace_opcodes = 1
    frame.f_trace_lines = 0

    global last_lineno

    if frame.f_globals.get('__name__', '') in self.blacklist:
        return 0

    if what == TraceEvent.CALL:
        # Add call as row (module, function, args, kwargs)
        self.call_stack.append((self.call_id, last_lineno))

        PyFrame_FastToLocals(frame)
        _args, kwonlyargs, _varargs, _varkw = getfullargs(frame.f_code)

        if isinstance(_args, list):
            _args = tuple(_args)

        if isinstance(kwonlyargs, list):
            kwonlyargs = tuple(kwonlyargs)

        if isinstance(_varargs, list):
            _varargs = tuple(_varargs)

        if isinstance(_varkw, list):
            _varkw = tuple(_varkw)

        args = tuple(map(lambda x: frame.f_locals[x], _args)) if _args else ()
        kwargs = tuple(map(lambda x: frame.f_locals[x], kwonlyargs)) if kwonlyargs else ()
        varargs = frame.f_locals[_varargs] if _varargs else ()
        varkw = frame.f_locals[_varkw].values() if _varkw else ()

        self.calls.append((
            self.call_id,
            id(frame.f_code),
            frame.f_code.co_filename,
            frame.f_lineno,
            frame.f_code.co_name,
            _args,
            tuple(map(lambda x: get_input_factor(x), args)) if args else None,
            kwonlyargs,
            tuple(map(lambda x: get_input_factor(x), kwargs)) if kwargs else None,
            _varargs,
            tuple(map(lambda x: get_input_factor(x), varargs)) if varargs else None,
            _varkw,
            tuple(map(lambda x: get_input_factor(x), varkw)) if varkw else None
        ))
        self.call_id += 1
        logger.debug(f"Call: {self.calls[len(self.calls) - 1]}")

    elif what == TraceEvent.RETURN:
        if len(self.call_stack) > 1:
            # Do not pop root call row
            child = self.call_stack.pop()
        else:
            child = self.call_stack[0]

        # Add opcode weight to parent call
        parent = self.call_stack[len(self.call_stack) - 1]
        value = self.f_weight_map.get(child[0], 0)
        parent_weight = self.opcodes.get(parent, 0)
        self.opcodes[parent] = parent_weight + value

        _value = self.f_weight_map.get(parent[0], 0)
        self.f_weight_map[parent[0]] = _value + value
        logger.debug(f"Return call: {child[0]}, opcodes: {value}")

    elif what == TraceEvent.OPCODE:
        # Anything in here should cause minimal overhead
        last_lineno = frame.f_lineno
        metric_value = self.metric.get_value(frame)

        # Save opcode weight per line in current call
        call = self.call_stack[len(self.call_stack) - 1][0]
        key = (call, frame.f_lineno)
        value_line = self.opcodes.get(key, 0)
        self.opcodes[key] = value_line + metric_value

        # Keep track of all opcodes executed within call
        value = self.f_weight_map.get(call, 0)
        self.f_weight_map[call] = value + metric_value

    return 0
