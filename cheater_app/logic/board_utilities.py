from cheater_app.logic.constants import RESOURCES_PATH
from cheater_app.logic import utils


class BoardUtilities:
    def __init__(self, country):
        self.country = country
        self._initialize_data()

    def _initialize_data(self):
        self._word_multipliers, self._letter_multipliers = BoardUtilities.get_multipliers()
        self._letters_values = {}
        for key, value in self.get_letters_values().items():
            self._letters_values[key.upper()] = value

    def get_letters_values(self):
        path = f"{RESOURCES_PATH}/{self.country.name.lower()}/letters_values.txt"
        return utils.get_dictionary_from_file(path)

    def check_if_letter_valid_in_country(self, letter):
        return letter.upper() in self._letters_values

    @staticmethod
    def get_multipliers():
        path = f"{RESOURCES_PATH}/multipliers.txt"
        multipliers = utils.get_dictionary_from_file(path)
        return multipliers['word'], multipliers['letter']

    def get_field_letter_multiplier(self, x, y):
        return self._letter_multipliers[x][y]

    def get_field_word_multiplier(self, x, y):
        return self._word_multipliers[x][y]

    def get_letter_value(self, char):
        return self._letters_values[char.upper()]

    def evaluate_letter_value(self, letter):
        letter_value = self.get_letter_value(letter.get_char().upper())
        if letter.is_user_letter():
            letter_multiplier = self.get_field_letter_multiplier(letter.get_x(), letter.get_y())
        else:
            letter_multiplier = 1
        return letter_multiplier * letter_value
