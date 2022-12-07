import os

from cheater_app.logic.constants import RESOURCES_PATH
from cheater_app.logic.structures import Country
from cheater_app.logic import utils
from cheater_app.logger import logger


@utils.timing
def get_words_from_dictionary_file(country):
    path = f"{RESOURCES_PATH}/{country.lower()}/words.txt"
    logger.info(f"Trying to load words from file with path = {path}")
    with open(path, "r") as f:
        words = f.readlines()
    return [line.strip().lower() for line in words]


@utils.timing
def create_trie(words, country):
    root = {}
    for word in words:
        this_dict = root
        skip_next = False
        for index, letter in enumerate(word):
            if skip_next:
                skip_next = False
                continue
            if country == Country.ES and index < len(word) - 1:
                letter, skip_next = utils.check_if_contains_spanish_doubles(word, index)
            this_dict = this_dict.setdefault(letter, {})
        this_dict[None] = None
    return root


@utils.timing
def create_trie_for_country(country, words=None):
    logger.info(f"Creating trie for a country = {country}")
    if not words:
        words = get_words_from_dictionary_file(country.name)
    logger.info(f"Number of words loaded from a dictionary file = {len(words)}, creating trie...")
    trie = create_trie(words, country)
    return trie


