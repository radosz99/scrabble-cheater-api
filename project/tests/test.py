import os
import sys
import copy
import secrets

from functools import wraps
from time import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from logic.trie import make_trie
from logic.algorithm import Algorithm
from logic.variables import change_resource_path, change_country, get_resource_path, get_country, get_board
from logic.word_finder import get_updated_board_after_move
from logic.board_utilities import BoardUtilities
from logic.exceptions import IncorrectMove


def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        # print('func:%r args:[%r, %r] took: %2.4f sec' % (f.__name__, args, kw, te - ts))
        print('func:%r took: %2.4f sec' % (f.__name__, te - ts))
        return result
    return wrap


@timing
def get_trie(country):
    return make_trie(country)


@timing
def get_best_moves(trie):
    algorithm = Algorithm(letters, board)
    return algorithm.get_moves(trie)


def get_letters_bank():
    bank = []
    path = f"{get_resource_path()}/{str(get_country().name).lower()}/letters_occurrences.txt"
    dict_occurrences = BoardUtilities.get_dictionary_from_file(path)
    for key, value in dict_occurrences.items():
        bank.extend(key * value)
    return bank


def get_x_random_items_from_list_as_string(amount, items_list):
    return ''.join([secrets.choice(items_list) for _ in range(amount)])


country = "gb"
change_resource_path("../resources")
change_country(country.upper())

trie = get_trie(country)
board = [[' ' for i in range(15)] for x in range(15)]
# letters_bank = get_letters_bank()
board = get_board()
# print(letters_bank)

# sixth_line = [' ', ' ', 'p', 'e', 'r', 'a', 't', 'i', 'o', 'n', 'a', 'l', ' ', ' ', ' ']
# eighth_line = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']

# board[11] = sixth_line
letters = "arkafpo"
best_moves = get_best_moves(trie)
for move in best_moves[0:20]:
    print(move)

# try:
#     for _ in range(40):
#         letters = get_x_random_items_from_list_as_string(7, letters_bank)
#         best_moves = get_best_moves(trie)
#         for move in best_moves:
#             get_updated_board_after_move(copy.deepcopy(board), move)
#         board = get_updated_board_after_move(copy.deepcopy(board), best_moves[0])
#         print(best_moves[0])
#         for line in board:
#             print(line)
#         # print()
# except IncorrectMove as e:
#     print(e)
#

