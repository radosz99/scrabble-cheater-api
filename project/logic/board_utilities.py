import json


class BoardUtilities:
    def __init__(self):
        self._initialize_data()

    def _initialize_data(self):
        self._word_multipliers, self._letter_multipliers = BoardUtilities.get_multipliers()
        self._letters_values = BoardUtilities.get_letters_values()

    @staticmethod
    def get_dictionary_from_file(file_path):
        with open(file_path) as f:
            data = f.read()
        return json.loads(data)

    @staticmethod
    def get_letters_values():
        from .variables import get_country, get_resource_path
        path = f"{get_resource_path()}/{str(get_country().name).lower()}/letters_values.txt"
        return BoardUtilities.get_dictionary_from_file(path)

    @staticmethod
    def get_multipliers():
        from .variables import get_resource_path
        path = f"{get_resource_path()}/multipliers.txt"
        multipliers = BoardUtilities.get_dictionary_from_file(path)
        return multipliers['word'], multipliers['letter']

    def get_field_letter_multiplier(self, x, y):
        return self._letter_multipliers[x][y]

    def get_field_word_multiplier(self, x, y):
        return self._word_multipliers[x][y]

    def get_letter_value(self, char):
        return self._letters_values[char]

    def evaluate_letter_value(self, letter):
        letter_value = self.get_letter_value(letter.get_char())
        if letter.is_user_letter():
            letter_multiplier = self.get_field_letter_multiplier(letter.get_x(), letter.get_y())
        else:
            letter_multiplier = 1
        return letter_multiplier * letter_value
