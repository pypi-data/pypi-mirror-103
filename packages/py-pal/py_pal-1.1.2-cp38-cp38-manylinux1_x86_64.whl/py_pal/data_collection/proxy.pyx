from copy import deepcopy

from cpython.object cimport PyObject_HasAttr
from pympler import asizeof

from py_pal.util import setup_logging

logger = setup_logging(__name__)

cdef tuple default_filter_types = (set, list, tuple, dict)

cpdef float get_input_factor(object args, coll_filter=default_filter_types) except -1:
    """Proxy for input arguments.
    
    It is used to infer complexity with the least squares algorithm. Therefore all returned values have to be positive
    and greater than zero. 
    
    If a collection of non-collection types is encountered, the elements of the collection are assigned the value 1.
    If the collection contains other collections, :meth:`py_pal.data_collection.get_input_factor` is called recursively 
    to determine its value. By default this happens for 'set', 'list', 'tuple' and 'dict', with 'coll_filter' you can 
    control this behavior.
    
    Keyword Arguments:
        coll_filter (tuple): A tuple of Python types for which the :meth:`py_pal.data_collection.get_input_factor` \
            function descends recursively. Passing an empty tuple might improve profiling results in use cases where \
            non-standard data types (e.g. :class:`numpy.ndarray`) are used as arguments.
    
    Returns:
        int: proxy value
    """
    if args is None or NULL or isinstance(args, (type, Exception)):
        return 0

    if isinstance(args, (int, float, complex, bool)):
        # Return absolute ``float`` value for numeric types.
        logger.debug(f"Numeric argument: {type(args)}")
        if args is False:
            # Special case, bool is internally represented as int.
            # Explicitly return 1 in this case, else it would be 0.
            return 1

        if isinstance(args, (int, float)):
            return abs(args)

        if isinstance(args, complex):
            return abs(args.real)

        return 1

    if isinstance(args, str):
        logger.debug(f"String: {type(args)}")
        return len(args)

    if PyObject_HasAttr(args, '__iter__'):
        logger.debug(f"Collection type: {type(args)}")
        # Collections
        if PyObject_HasAttr(args, '__next__'):
            # Do not consume the original, try to create a copy.
            try:
                args = [deepcopy(args)]
            except (TypeError, RecursionError):
                return 1

        iterable = args
        if isinstance(args, dict):
            iterable = args.values()

        value = 0
        try:
            for argument in iterable:
                if isinstance(argument, coll_filter) or (not coll_filter and PyObject_HasAttr(argument, '__iter__')):
                    logger.debug(f"Recursive descent: {type(argument)}")
                    value += get_input_factor(argument, coll_filter)
                    continue
                value += 1
        except AttributeError:
            pass

        return value

    try:
        # Memory size for complex objects
        logger.debug(f"Object size: {type(args)}")
        return asizeof.asizeof(args)
    except ModuleNotFoundError:
        return 0
