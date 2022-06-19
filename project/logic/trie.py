import logging
import os

def read_words(country, resource_path):
    logging.basicConfig(filename='demo.log', level=logging.DEBUG)
    words = open(f"{resource_path}/words{country}.txt", "r")
    return [line.strip().lower() for line in words]


def make_trie(country, resource_path):
    words = read_words(country, resource_path)
    root = {}
    for word in words:
        this_dict = root
        for letter in word:
            this_dict = this_dict.setdefault(letter, {})
        this_dict[None] = None
    return root
