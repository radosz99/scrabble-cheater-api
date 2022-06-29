from enum import Enum
from .board_utilities import BoardUtilities


class Orientation(Enum):
    HORIZONTAL = 1
    VERTICAL = 2


class WordType(Enum):
    RIGHT_ANGLE = 1
    BRIDGE = 2


class Country(Enum):
    PL = 1
    GB = 2


class Letter:
    def __init__(self, x, y, char, user_letter=True):
        self._x = x
        self._y = y
        self._char = char
        self._user_letter = user_letter

    def __repr__(self):
        return f"\"x = {self._x}, y = {self._y}, char = {self._char}, user_letter = {self._user_letter}\""

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def get_char(self):
        return self._char

    def set_user_letter_on_false(self):
        self._user_letter = False

    def is_user_letter(self):
        return self._user_letter

    def __eq__(self, other):
        return self._x == other.get_x() and self._y == other.get_y()


class Move:
    def __init__(self, word, board_utilities, left_space_needed=0, pattern=None):
        self.board_utilities = board_utilities
        self._pattern = pattern
        self._word = word
        self.left_space_needed = left_space_needed
        self._orientation = pattern.get_orientation()
        self._start_x, self._start_y = self._get_first_letter_coordinates()
        self._position = self._get_position_from_coordinates_according_to_orientation()
        self._letters_list = self._create_letters_list()
        self._points = self._evaluate_move()

    def _check_if_letter_not_from_board(self, letter):
        return False if letter in self._pattern.get_letters_list() else True

    def _get_letter_instance_from_index_and_char(self, index, char):
        x, y = self.get_x_letter_coordinates(index)
        letter = Letter(x, y, char)
        if not self._check_if_letter_not_from_board(letter):
            letter.set_user_letter_on_false()
        return letter

    def _create_letters_list(self):
        return [self._get_letter_instance_from_index_and_char(index, char) for index, char in enumerate(self._word)]

    def _get_first_letter_coordinates(self):
        if self.get_pattern().get_orientation() == Orientation.VERTICAL:
            return self.get_pattern().get_x() - self.left_space_needed, self.get_pattern().get_y()
        elif self.get_pattern().get_orientation() == Orientation.HORIZONTAL:
            return self.get_pattern().get_x(), self.get_pattern().get_y() - self.left_space_needed

    def get_first_letter_coordinates(self):
        return self._start_x, self._start_y

    def get_x_letter_coordinates(self, counter):
        if self.get_orientation() == Orientation.VERTICAL:
            return self._start_x + counter, self._start_y
        elif self.get_orientation() == Orientation.HORIZONTAL:
            return self._start_x, self._start_y + counter

    def _evaluate_move(self):
        value = 0
        for counter, letter in enumerate(self._letters_list):
            value += self.board_utilities.evaluate_letter_value(letter)
        multiplier = self._calculate_overall_word_multiplier()
        seven_letters_bonus = 50 if self._check_if_seven_letters_move() else 0
        return value * multiplier + seven_letters_bonus

    def _check_if_seven_letters_move(self):
        if len(self.get_word()) - len(self.get_pattern().get_letters()) == 7:
            return True
        else:
            return False

    def _calculate_overall_word_multiplier(self):
        multiplier = 1
        for letter in self._letters_list:
            if letter.is_user_letter():
                multiplier *= self.board_utilities.get_field_word_multiplier(letter.get_x(), letter.get_y())
        return multiplier

    def _get_position_from_coordinates_according_to_orientation(self):
        x, y = self.get_first_letter_coordinates()
        if self.get_orientation() == Orientation.VERTICAL:
            return str(chr(65 + y)) + '_' + str(x)
        elif self.get_orientation() == Orientation.HORIZONTAL:
            return str(x) + '_' + str(chr(65 + y))

    def __str__(self):
        return f" {self._position}, word = {self._word}, points = {self._points}"

    def __hash__(self):
        return hash(('position', self._position, 'word', self._word))

    def __eq__(self, other):
        return self._position == other.get_position() and self._word == other.get_word()

    def set_points(self, points):
        self._points = points

    def get_pattern(self):
        return self._pattern

    def get_position(self):
        return self._position

    def get_orientation(self):
        return self._orientation

    def get_points(self):
        return self._points

    def get_word(self):
        return self._word
