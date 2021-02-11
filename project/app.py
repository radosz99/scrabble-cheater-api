from flask import Flask, jsonify, request, abort, render_template, flash, redirect, url_for
from .logic.trie import make_trie
import logging
from .logic.algorithm import Algorithm
import json
import sys

app = Flask(__name__)
logging.basicConfig(filename='demo.log', level=logging.DEBUG)
        
#trie_PL = make_trie("PL")
trie_GB = make_trie("GB")


def get_trie(country):
    upper_country = country.upper()
    if(upper_country == "PL"):
        return trie_PL
    elif(upper_country == "GB"):
        return trie_GB


@app.route('/best_move/<country>', methods = ['POST'])
def add_computer(country):
    app.logger
    global get_trie
    data = request.get_json()
    logging.info(f"Data = {data}")
    try:
        letters = data["letters"]
        json_board = data["board"]  
        logging.info(f"New request, letter:{letters}, board:{json_board}")
        board = []
        for line in json_board:
            board.append([line[str(i)] for i in range(15)])
        algorithm = Algorithm(letters,board)
        best_moves = algorithm.algorithm_engine(get_trie(country))
        return jsonify(best_moves)
    except TypeError as e:
        logging.info(f"Missing parameters in request - {e}")
        abort(400, description="No letters or no board, how can I handle it?")
    except (KeyError, IndexError) as e:
        logging.info(f"Invalid format of parameters - {e}") 
        abort(422, description="Syntax is good, but I cannot process it, make sure you provide letters and board in appropriate format")


if __name__ == '__main__':
    app.run(host='0.0.0.0')
