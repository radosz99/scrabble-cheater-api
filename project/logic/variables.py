from .structures import Country
from .exceptions import NotSupportedCountry

RESOURCES_PATH = "project/resources"
COUNTRY = Country.PL
BOARD_SIZE = 15
BOARD_MAX_INDEX = BOARD_SIZE - 1  # indexing from 0 obviously
BOARD_MIN_INDEX = 0
BOARD_MIDDLE = int(BOARD_MAX_INDEX / 2)


def change_resource_path(new_resource_path):
    global RESOURCES_PATH
    RESOURCES_PATH = new_resource_path


def get_resource_path():
    return RESOURCES_PATH


def change_country(new_country):
    global COUNTRY
    try:
        COUNTRY = Country[new_country]
    except KeyError:
        raise NotSupportedCountry(f"There is no support for country \"{new_country}\"")


def get_country():
    return COUNTRY


def get_board():
    return [[" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "p", " ", " ", " ", " "],
            [" ", " ", " ", " ", "a", "r", "g", "u", "t", "e", "l", "y", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "a", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", "a", "g", "e", "n", "t", "u", "r", "y"],
            [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "e", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", "k", "o", "p", "e", "r", "t", "a", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "o", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "m", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "]]