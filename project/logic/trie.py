import logging
import os

from .variables import get_resource_path, get_country


def read_words(country):
    logging.basicConfig(filename='demo.log', level=logging.DEBUG)
    words = open(f"{get_resource_path()}/{country.lower()}/words.txt", "r")
    return [line.strip().lower() for line in words]


def make_trie(country):
    words = read_words(country)
    root = {}
    for word in words:
        this_dict = root
        for letter in word:
            this_dict = this_dict.setdefault(letter, {})
        this_dict[None] = None
    return root
