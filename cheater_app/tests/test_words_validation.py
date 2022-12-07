import unittest
import logging

from cheater_app.logic import trie, structures, anagram
from cheater_app.logger import logger, formatter


class Testing(unittest.TestCase):
    def setUp(self):
        # setup logger
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    def test_speed_of_creating_es_trie(self):
        dict_trie = trie.create_trie_for_country(structures.Country.ES)
        print(anagram.validate_words(['rr', 'arriera'], dict_trie, structures.Country.ES))


if __name__ == "__main__":
    unittest.main()
