from flask import Flask, jsonify, request, abort
import traceback
import logging

from .logic.trie import make_trie
from .logic.algorithm import Algorithm
from .logic.anagram import find_words
from .logic.variables import get_country, change_country
from .logic.exceptions import NotSupportedCountry
from .logic.structures import Country

app = Flask(__name__)
logging.basicConfig(filename='demo.log', level=logging.DEBUG)

tries = {}


def get_trie(country):
    if country not in tries:
        tries[country] = make_trie(country)
    return tries[country]


@app.route('/best-move/<country>', methods=['POST'])
def get_best_move(country):
    country = country.upper()
    data = request.get_json()
    logging.info(f"Data = {data}")
    try:
        change_country(country)
        letters, board = data["letters"], data["board"]
        logging.info(f"New request for best move, letter:{letters}, board:{board}")
        algorithm = Algorithm(letters, board)
        best_moves = algorithm.algorithm_engine(get_trie(country))
        return jsonify(best_moves)
    except NotSupportedCountry as e:
        abort(405, description=e)
    except TypeError:
        logging.info(f"Missing parameters in request - {traceback.format_exc()}")
        p
        abort(400, description="No letters or no board, how can I handle it?")
    except (KeyError, IndexError):
        logging.info(f"Invalid format of parameters - {traceback.format_exc()}")
        abort(422, description="Syntax is correct, but I cannot process it, make sure you provide letters and board in appropriate format")


@app.route('/check-words/<country>', methods=['POST'])
def check_if_word_in_dict(country):
    data = request.get_json()
    logging.info(f"Data = {data}")
    try:
        words_json = data["words"]
        logging.info(f"New request for checking word validness, words:{words_json}")
        words = []
        for word in words_json:
            words.append(word)
        return jsonify(find_words(words, get_trie(country)))
    except TypeError:
        logging.info(f"Missing parameters in request - {traceback.format_exc()}")
        abort(400, description="No words, how can I check anything?")
    except (KeyError, IndexError):
        logging.info(f"Invalid format of parameters - {traceback.format_exc()}")
        abort(422, description="Syntax is good, but I cannot process it, make sure you provide words in appropriate format")


if __name__ == '__main__':
    app.run(host='0.0.0.0')
