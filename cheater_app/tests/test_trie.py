import unittest
import logging

from cheater_app.logic import trie, structures
from cheater_app.logger import logger, formatter


class Testing(unittest.TestCase):
    def setUp(self):
        # setup logger
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    def test_speed_of_creating_gb_trie(self):
        trie.get_trie_for_country(structures.Country.GB.name)

    def test_speed_of_creating_pl_trie(self):
        trie.get_trie_for_country(structures.Country.PL.name)


if __name__ == "__main__":
    unittest.main()
