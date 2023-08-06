import types
from cpython.object cimport PyObject_HasAttr
from py_pal.data_collection.metric cimport CallMetric
from py_pal.data_collection.arguments cimport unpack_oparg
from py_pal.data_collection.metric import AvgBuiltinFuncComplexity

cdef class OpcodeMetric:
    """Base opcode metric."""

    def __init__(self):
        """`builtin_calls` counts calls to Python builtin functions. `hits` indicates how many builtin calls were
        weighted by a function from :class:`py_pal.data_collection.AvgBuiltinFuncComplexity`.
        """
        self.hits = 0
        self.builtin_calls = 0

    cdef Py_ssize_t get_value(self, FrameType frame) except -1:
        return 1

    cdef bint in_complexity_map(self, function) except -1:
        return PyObject_HasAttr(function, '__qualname__') and function.__qualname__ in AvgBuiltinFuncComplexity.mapping

    cdef Py_ssize_t get_function_opcodes(self, object function, object args, object kwargs) except -1:
        cdef CallMetric instance

        if isinstance(function, types.BuiltinFunctionType):
            # Statistics
            self.builtin_calls += 1
            if self.in_complexity_map(function):
                self.hits += 1

        if self.in_complexity_map(function):
            complexity_class = AvgBuiltinFuncComplexity.mapping[function.__qualname__]
            instance = complexity_class(args, kwargs)
            return instance.value()

        return 1

cdef class AdvancedOpcodeMetric(OpcodeMetric):
    """Extended opcode metric that assigns a value dependent on the arguments to builtin calls instead of a constant
    value.
    """
    cdef Py_ssize_t get_value(self, FrameType frame) except -1:
        if frame.f_lasti < 0:
            return 1

        code = frame.f_code.co_code
        op = code[frame.f_lasti]

        if op == 131:
            # CALL_FUNCTION
            argc = unpack_oparg(code[frame.f_lasti:])
            valuestack = <list> get_valuestack(<PyFrameObject *> frame, argc + 1)
            args = valuestack[1:]
            _callable = valuestack[0]

            return self.get_function_opcodes(_callable, args, {})

        elif op == 141:
            # CALL_FUNCTION_KW
            argc = unpack_oparg(code[frame.f_lasti:])
            valuestack = <list> get_valuestack(<PyFrameObject *> frame, argc + 2)

            _callable = valuestack.pop(0)
            kw_names = valuestack.pop()
            kwargs = {}
            for name in kw_names:
                kwargs[name] = valuestack.pop()

            return self.get_function_opcodes(_callable, valuestack, kwargs)

        return 1
