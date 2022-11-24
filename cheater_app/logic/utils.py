import json
import operator
import functools
import inspect
from time import time
from cheater_app.logger import logger


def timing(f):
    @functools.wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        logger.info('Function: %r took: %2.4f sec' % (f.__name__, te - ts))
        return result
    return wrap


def remove_duplicates_from_list(lst):
    return list(set(lst))


def get_sorted_list_by_attribute(list, attr, reverse=True):
    list.sort(key=operator.attrgetter(attr), reverse=reverse)
    return list


def get_dictionary_from_file(file_path):
    with open(file_path, 'r', encoding='utf8') as f:
        data = f.read()
    return json.loads(data)


def funclog(logger):
    # If a Logger object is passed in, use that.  Otherwise, get default Logger.

    def get_arg_string(args, kwargs):
        """Convert args and kwargs to a pretty string."""
        return ', '.join(["'{}'".format(a) if type(a) == str else
                          '{}'.format(a) for a in args] +
                         ["{}='{}'".format(a, v) if type(v) == str else
                          '{}={}'.format(a, v) for a, v in kwargs.items()])

    def real_decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            frame = inspect.stack()[1][0]
            frame_info = inspect.getframeinfo(frame)
            filename = os.path.basename(frame_info.filename)
            lineno = frame_info.lineno
            func_name = getattr(fn, name_attr)
            arg_string = get_arg_string(args, kwargs)
            source_info = '{}:{}:{}({})'.format(filename, lineno, func_name,
                                                arg_string)
            real_logger.debug('calling {}'.format(source_info))
            try:
                res = fn(*args, **kwargs)
            except Exception as e:
                real_logger.exception('{} threw exception:\n{}'.format(source_info, e))
                raise
            real_logger.debug('{} returned: {}'.format(source_info, res))
            return res
        return wrapper

    if type(logger) == type(real_decorator):
        return real_decorator(logger)

    return real_decorator