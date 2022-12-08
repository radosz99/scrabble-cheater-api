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
    letters = fields.List(fields.String, required=True)

    @validates("board")
    def validate_length(self, row):
        if len(row) != BOARD_SIZE: raise ValidationError("Board has to be list with 15x15 size")
        for cell in row:
            if len(cell) != BOARD_SIZE: raise ValidationError("Board has to be list with 15x15 size")


class WordValidationRequestBody(Schema):
    words = fields.List(fields.String, required=True)


def parse_letters_string(letters, country):
    letters = letters.lower()
    logger.debug(f"Parsing letters string - {letters}")
    letters_list = []
    skip_next = False
    for index, letter in enumerate(letters):
        if skip_next:
            skip_next = False
            continue
        if country.name == "ES" and index < len(letters) - 1:
            letter, skip_next = check_if_contains_spanish_doubles(letters, index)
        letters_list.append(letter)
    logger.debug(f"Parsed letters string - {letters_list}")
    return letters_list


def check_if_contains_spanish_doubles(word, index):
    word = word.lower()
    spanish_doubles = ['ll', 'rr', 'ch']
    if (double := word[index:index + 2]) in spanish_doubles:
        return double, True
    else:
        return word[index].lower(), False


def get_clear_board():
    return [[' ' for x in range(BOARD_SIZE)] for y in range(BOARD_SIZE)]