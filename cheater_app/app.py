import traceback
import functools

from flask import Flask, jsonify, request, abort
from marshmallow import ValidationError

from cheater_app.logic.trie import create_trie_for_country
from cheater_app.logic.algorithm import Algorithm
from cheater_app.logic.anagram import validate_words
from cheater_app.logic import exceptions as exc
from cheater_app.logic.structures import Country
from cheater_app.logic.constants import BOARD_SIZE
from cheater_app.logic import utils
from cheater_app.logger import logger

app = Flask(__name__)

tries = {}


@functools.lru_cache(maxsize=16)
def create_trie(country):
    return create_trie_for_country(country)


def get_trie(country):
    logger.info(f"Current dictionaries: {tries.keys()}")
    return tries.setdefault(country.name, create_trie(country))


def get_country_via_abbreviation(country_abb):
    try:
        return Country[country_abb.upper()]
    except KeyError as e:
        logger.debug(f"Could not get country with name {country_abb}, cause - {str(e)}")
        raise exc.NotSupportedCountryException(f"Country with abbreviation {country_abb} is not supported. List of "
                                               f"supported countries = {[e.name for e in Country]}")


@app.route('/best-move/<country>', methods=['POST'])
def get_best_move(country):
    # TODO: bug with spanish doubles, PACDEDLL and clear board, parse to list
    try:
        country = get_country_via_abbreviation(country)
        data = request.get_json()
        body = utils.BestMoveRequestBody()
        result = body.load(data)
        letters, board = result['letters'], result['board']
        algorithm = Algorithm(letters, board, country)
        best_moves = algorithm.algorithm_engine(get_trie(country))
        return jsonify(best_moves)
    except (exc.BaseCheaterException, ValidationError) as e:
        logger.debug(e)
        return jsonify({"detail": str(e), "error": e.__class__.__name__}), 400


@app.route('/check-words/<country>', methods=['POST'])
def validate_words_in_country_dictionary(country):
    try:
        country = get_country_via_abbreviation(country)
        data = request.get_json()
        body = utils.WordValidationRequestBody()
        result = body.load(data)
        words = result['words']
        validation_result = validate_words(words, get_trie(country))
        return jsonify(validation_result)
    except (exc.BaseCheaterException, ValidationError) as e:
        logger.debug(e)
        return jsonify({"detail": str(e), "error": e.__class__.__name__}), 400


@app.before_request
def log_request_info():
    logger.info(f"Calling endpoint = {request.path}")
    logger.info(f"Headers: {request.headers}")
    logger.info(f"Body: {request.get_data()}")


if __name__ == '__main__':
    app.run(host='0.0.0.0')
