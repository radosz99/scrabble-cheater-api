import json
import operator
import functools
from time import time

from marshmallow import Schema, fields, ValidationError, validates

from cheater_app.logger import logger
from cheater_app.logic.constants import BOARD_SIZE


def timing(f):
    @functools.wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        logger.info('Function: %r took: %2.5f sec' % (f.__name__, te - ts))
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


class BestMoveRequestBody(Schema):
    board = fields.List(fields.List(fields.String), required=True)
    letters = fields.String(required=True)

    @validates("board")
    def validate_length(self, row):
        if len(row) != BOARD_SIZE: raise ValidationError("Board has to be list with 15x15 size")
        for cell in row:
            if len(cell) != BOARD_SIZE: raise ValidationError("Board has to be list with 15x15 size")


class WordValidationRequestBody(Schema):
    words = fields.List(fields.String, required=True)
