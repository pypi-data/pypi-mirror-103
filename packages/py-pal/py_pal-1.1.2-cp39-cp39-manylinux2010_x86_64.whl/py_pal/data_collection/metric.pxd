cdef class CallMetric:
    cdef object args
    cdef object kwargs
    cdef Py_ssize_t value(self) except -1

cdef class ArgsLengthLinear(CallMetric):
    pass
