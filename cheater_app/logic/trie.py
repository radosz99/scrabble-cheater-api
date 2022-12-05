import os

from .constants import RESOURCES_PATH
from .structures import Country
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
def create_trie(words, country):
    root = {}
    for word in words:
        this_dict = root
        skip_next = False
        for index, letter in enumerate(word):
            if skip_next:
                skip_next = False
                continue
            if country == Country.ES:
                for spanish_double in spanish_doubles:
                    if index == len(word) - 1:
                        break
                    if letter == spanish_double[0] and word[index+1] == spanish_double[1]:
                        letter = spanish_double
                        skip_next = True
            this_dict = this_dict.setdefault(letter, {})
        this_dict[None] = None
    return root

@utils.timing
def get_trie_for_country(country):
    logger.info(f"Creating trie for a country = {country}")
    words = read_words(country.name)
    logger.info(f"Number of words loaded from a dictionary file = {len(words)}, creating trie...")
    trie = create_trie(words, country)
    return trie

spanish_doubles = ['ll', 'rr', 'ch']
