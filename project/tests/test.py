import os
import sys
from functools import wraps
from time import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from logic.trie import make_trie
from logic.algorithm import Algorithm
from logic.variables import change_resource_path, change_country


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
    return algorithm.algorithm_engine(trie)


country = "gb"
change_resource_path("../resources")
change_country(country.upper())

trie = get_trie(country)
letters = "tmarian"
board = [[' ' for i in range(15)] for x in range(15)]

sixth_line = [' ', 'o', 'p', 'e', 'r', 'a', 't', 'i', 'o', 'n', 'a', 'l', ' ', ' ', ' ']
eighth_line = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'l', ' ', ' ', ' ']
board[6] = sixth_line
# board[8] = sixth_line
board[11] = sixth_line
# board[14] = sixth_line
for line in board:
    print(line)

best_moves = get_best_moves(trie)
quantity = int(best_moves['quantity'])

points = 0

print(best_moves['moves'][0:10])
print(quantity)
for move in best_moves['moves']:
    points += int(move['points'])
print(points)
