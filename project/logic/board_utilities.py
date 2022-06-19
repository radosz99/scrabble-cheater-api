def get_field_letter_multiplier(x, y):
    if ((x in [5, 9]) and (y in [1, 5, 9, 13])) or ((x in [1, 13]) and (y in [5, 9])):
        return 3
    elif ((x in [0, 7, 14]) and (y in [3, 11])) or ((x in [3, 11]) and (y in [0, 7, 14])) or ((x in [2, 6, 8, 12])
                                                                                              and (y in [6, 8])) or (
            (y in [2, 6, 8, 12]) and (x in [6, 8])):
        return 2
    else:
        return 1


def get_field_word_multiplier(x, y):
    if ((x in [1, 13]) and (y in [1, 13])) or ((x in [2, 12]) and (y in [2, 12])) or (
            (x in [3, 11]) and (y in [3, 11])) or ((x in [4, 10]) and (y in [4, 10])) or (
            x == 7 and y == 7):
        return 2
    elif ((x in [0, 14]) and (y in [0, 7, 14])) or (x == 7 and (y in [0, 14])):
        return 3
    else:
        return 1


def get_char_value(char, country):
    from .structures import Country
    if country is Country.PL:
        if char in ['a', 'e', 'i', 'n', 'o', 'r', 's', 'w', 'z']:
            return 1
        elif char in ['c', 'd', 'k', 'l', 'm', 'p', 't', 'y']:
            return 2
        elif char in ['b', 'g', 'h', 'j', 'ł', 'u']:
            return 3
        elif char in ['ą', 'ę', 'f', 'ó', 'ś', 'ź']:
            return 5
        elif char == 'ć':
            return 6
        elif char == 'ń':
            return 7
        elif char == 'ź':
            return 9
        else:
            return 0

    elif country is Country.GB:
        if char in ['a', 'e', 'i', 'n', 'o', 'r', 's', 't', 'u', 'l']:
            return 1
        if char in ['g', 'd']:
            return 2
        if char in ['b', 'c', 'm', 'p']:
            return 3
        if char in ['h', 'v', 'w', 'y', 'f']:
            return 4
        if char == 'k':
            return 5
        if char in ['j', 'x']:
            return 8
        if char in ['q', 'z']:
            return 10
        else:
            return 1


def evaluate_letter_value(letter, country):
    letter_value = get_char_value(letter.get_char(), country)
    if letter.is_user_letter():
        letter_multiplier = get_field_letter_multiplier(letter.get_x(), letter.get_y())
    else:
        letter_multiplier = 1
    return letter_multiplier * letter_value
