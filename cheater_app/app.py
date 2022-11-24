from flask import Flask, jsonify, request, abort

from .logic.trie import get_trie_for_country
from .logic.algorithm import Algorithm
from .logic.anagram import find_words
from .logic.exceptions import NotSupportedCountry
from .logic.structures import Country
from .logic import utils
from cheater_app.logger import logger

app = Flask(__name__)

tries = {}


def get_trie(country):
    if country not in tries:
        tries[country] = get_trie_for_country(country)
    return tries[country]


@app.route('/best-move/<country>', methods=['POST'])
def get_best_move(country):
    country = Country[country.upper()]
    data = request.get_json()
    try:
        letters, board = data["letters"], data["board"]
        algorithm = Algorithm(letters, board, country)
        best_moves = algorithm.algorithm_engine(get_trie(country.name))
        return jsonify(best_moves)
    except NotSupportedCountry as e:
        abort(405, description=e)
    except TypeError as e:
        logger.info(f"Missing parameters in request - {str(e)}")
        abort(400, description="No letters or no board, how can I handle it?")
    except (KeyError, IndexError) as e:
        logger.info(f"Invalid format of parameters - {str(e)}")
        abort(422, description="Syntax is correct, but not possible to process it, "
                               "make sure you provide words in appropriate format")


@app.route('/check-words/<country>', methods=['POST'])
def check_if_word_in_dict(country):
    data = request.get_json()
    try:
        words_json = data["words"]
        words = [word for word in words_json]
        return jsonify(find_words(words, get_trie(country)))
    except TypeError as e:
        logger.info(f"Missing parameters in request - {str(e)}")
        abort(400, description="Request does not contain any words?")
    except (KeyError, IndexError) as e:
        logger.info(f"Invalid format of parameters - {str(e)}")
        abort(422, description="Syntax is correct, but not possible to process it, "
                               "make sure you provide words in appropriate format")


@app.before_request
def log_request_info():
    logger.info(f"Calling endpoint = {request.path}")
    logger.info(f"Headers: {request.headers}")
    logger.info(f"Body: {request.get_data()}")


if __name__ == '__main__':
    app.run(host='0.0.0.0')
