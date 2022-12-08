import unittest
import logging

from cheater_app.logic import algorithm, utils
from cheater_app.logic.structures import Country
from cheater_app.logic.trie import create_trie_for_country
from cheater_app.logger import logger, formatter
from cheater_app.logic import exceptions as exc


class Testing(unittest.TestCase):
    def setUp(self):
        # stream_handler = logging.StreamHandler()
        # stream_handler.setLevel(logging.INFO)
        # stream_handler.setFormatter(formatter)
        # logger.addHandler(stream_handler)
        self.country = Country.ES
        self.trie = create_trie_for_country(self.country)

    def test_core(self):
        board = utils.get_clear_board()
        alg = algorithm.Algorithm(['e', 'p', 'e', 'h', 'c', 'i'], board, self.country)
        best_moves = alg.algorithm_engine(self.trie)
        logger.info(best_moves)

    def test_raising_invalid_letter_exception(self):
        board = utils.get_clear_board()
        with self.assertRaises(exc.InvalidLetterException):
            alg = algorithm.Algorithm(['e', 'p', 'e', 'h', 'cc', 'i'], board, self.country)
            alg.algorithm_engine(self.trie)

    def test_raising_invalid_letter_exception_on_board(self):
        board = utils.get_clear_board()
        board[5][6] = "ą"
        with self.assertRaises(exc.InvalidLetterException):
            alg = algorithm.Algorithm(['e', 'p', 'e', 'h', 'cc', 'i'], board, self.country)
            alg.algorithm_engine(self.trie)


if __name__ == "__main__":
    unittest.main()
