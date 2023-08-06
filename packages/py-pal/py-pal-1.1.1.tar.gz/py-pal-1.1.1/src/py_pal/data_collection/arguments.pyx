from opcode import HAVE_ARGUMENT, EXTENDED_ARG

cpdef object unpack_oparg(object code):
    """Code from :mod:`dis`"""
    cdef int extended_arg = 0
    for i in range(0, len(code), 2):
        op = code[i]
        if op >= HAVE_ARGUMENT:
            arg = code[i + 1] | extended_arg
            extended_arg = (arg << 8) if op == EXTENDED_ARG else 0
        else:
            arg = None
        return arg

cpdef tuple getfullargs(object code):
    """Code from :mod:`inspect`"""
    nargs = code.co_argcount
    names = code.co_varnames
    nkwargs = code.co_kwonlyargcount
    args = list(names[:nargs])
    kwonlyargs = list(names[nargs:nargs + nkwargs])

    nargs += nkwargs
    varargs = None
    if code.co_flags & 4:
        varargs = code.co_varnames[nargs]
        nargs = nargs + 1
    varkw = None
    if code.co_flags & 8:
        varkw = code.co_varnames[nargs]
    return args, kwonlyargs, varargs, varkw
