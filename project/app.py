from flask import Flask, jsonify, request, abort
import traceback
from .logic.trie import make_trie
import logging
from .logic.algorithm import Algorithm
from .logic.anagram import find_words

app = Flask(__name__)
logging.basicConfig(filename='demo.log', level=logging.DEBUG)

# trie_PL = make_trie("PL")
trie_GB = make_trie("GB")


def get_trie(country):
    upper_country = country.lower()
    if(upper_country == "pl"):
        return trie_PL
    elif(upper_country == "gb"):
        return trie_GB


@app.route('/best-move/<country>', methods=['POST'])
def get_best_move(country):
    app.logger
    global get_trie
    data = request.get_json()
    logging.info(f"Data = {data}")
    try:
        letters = data["letters"]
        board = data["board"]
        logging.info(f"New request for best move, letter:{letters}, board:{board}")
        algorithm = Algorithm(letters, board, country.lower())
        best_moves = algorithm.algorithm_engine(get_trie(country))
        return jsonify(best_moves)
    except TypeError:
        logging.info(f"Missing parameters in request - {traceback.format_exc()}")
        abort(400, description="No letters or no board, how can I handle it?")
    except (KeyError, IndexError):
        logging.info(f"Invalid format of parameters - {traceback.format_exc()}")
        abort(422, description="Syntax is good, but I cannot process it, make sure you provide letters and board in appropriate format")


@app.route('/check-words/<country>', methods=['POST'])
def check_if_word_in_dict(country):
    app.logger
    global get_trie
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
