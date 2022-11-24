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
