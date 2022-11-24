import os

from .constants import RESOURCES_PATH
from . import utils
from cheater_app.logger import logger


@utils.timing
def read_words(country):
    path = f"{RESOURCES_PATH}/{country.lower()}/words.txt"
    logger.info(f"Trying to load words from file with path = {path}")
    with open(path, "r") as f:
        words = f.readlines()
    return [line.strip().lower() for line in words]


@utils.timing
def create_trie(words):
    root = {}
    for word in words:
        this_dict = root
        for letter in word:
            this_dict = this_dict.setdefault(letter, {})
        this_dict[None] = None
    return root


def get_trie_for_country(country):
    logger.info(f"Creating trie for a country = {country}")
    words = read_words(country)
    logger.info(f"Number of words loaded from a dictionary file = {len(words)}, creating trie...")
    trie = create_trie(words)
    return trie


