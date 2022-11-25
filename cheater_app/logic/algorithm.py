import copy

from .anagram import find_anagrams
from .structures import Orientation, Move, WordType, Country
from . import utils
from .pattern_finder import PatternFinder, Pattern
from .exceptions import WordDoesNotMatchToPattern
from . import constants
from .board_utilities import BoardUtilities
from cheater_app.logger import logger


class Algorithm:
    def __init__(self, letters, board, country):
        self.letters = letters.lower()
        self.board = board
        self.country = country
        self.patterns = self.__get_patterns()
        self.board_utilities = BoardUtilities(country)

    def __get_patterns(self):
        logger.info(f"Looking for patterns on board: {self.get_board_string()}")
        pattern_finder = PatternFinder()
        patterns = pattern_finder.create_patterns(self.board)
        logger.info(f"Created patterns = {patterns}")
        return patterns

    def algorithm_engine(self, trie):
        logger.info("Starting algorithm engine")
        sorted_list_of_valid_moves = self.__get_moves(trie)
        return self.convert_moves_to_json(sorted_list_of_valid_moves)

    @utils.timing
    def __get_moves(self, trie):
        if self.__check_if_board_is_clear():
            logger.info("Board is clear, getting move from clear board")
            return self.__get_valid_moves_from_clear_board(find_anagrams(str(self.letters), trie))
        else:
            letters_for_anagram = str(self.letters) + self.__get_letters_from_board()
            logger.info(f"Board is not clear, looking for anagrams from letters = {letters_for_anagram}")
            anagrams = find_anagrams(letters_for_anagram, trie)
            logger.debug(f"Created {len(anagrams)} anagrams = {anagrams}")
            return self.__get_valid_moves(anagrams)

    def __get_valid_moves_from_clear_board(self, anagrams):
        moves = []
        for index, word in enumerate(anagrams):
            logger.debug(f"Getting moves from word = {word}, progress = {index}/{len(anagrams)}")
            move_options = self.__get_all_possibilities_for_anagram_in_clear_board(word)
            logger.debug(f"Created move options = {move_options}")
            moves.extend(move_options)
        logger.info(f"Found {len(moves)} words, sorting...")
        return utils.get_sorted_list_by_attribute(moves, "_points")

    def __get_all_possibilities_for_anagram_in_clear_board(self, anagram):
        return [self.__get_move_instance_from_anagram_and_index(anagram, i) for i in range(len(anagram))]

    def __get_move_instance_from_anagram_and_index(self, anagram, i):
        pattern = Pattern(orientation=Orientation.HORIZONTAL)
        return Move(anagram, self.board_utilities, i, pattern)

    def __check_if_board_is_clear(self):
        for x in range(constants.BOARD_SIZE):
            for y in range(constants.BOARD_SIZE):
                if self.board[x][y] != ' ':
                    return False
        return True

    def __get_moves_by_word_type(self, pattern, anagram):
        if pattern.get_word_type() is WordType.RIGHT_ANGLE:
            return self.__get_right_angle_moves(anagram, pattern)
        elif pattern.get_word_type() is WordType.BRIDGE:
            return self.__get_bridge_moves(anagram, pattern)

    def __get_valid_moves(self, anagrams):
        moves = []
        logger.info("Getting valid moves")
        for index, word in enumerate(anagrams):
            logger.debug(f"Getting moves from word = {word}, progress = {index}/{len(anagrams)}")
            for pattern in self.patterns:
                logger.debug(f"For pattern = {pattern}")
                if self.__check_if_pattern_match_to_anagram(pattern, word):
                    moves_from_word = self.__get_moves_by_word_type(pattern, word)
                    logger.debug(f"Pattern matched, moves = {moves_from_word}")
                    moves.extend(moves_from_word)
        logger.info(f"Found {len(moves)} moves, removing duplicates...")
        moves = utils.remove_duplicates_from_list(moves)
        logger.info(f"{len(moves)} moves remain, sorting...")
        return utils.get_sorted_list_by_attribute(moves, "_points")

    def __check_if_word_without_pattern_letters_has_only_user_letters(self, pattern, word):
        try:
            word = self.remove_letters_from_string(pattern.get_letters(), word)
            self.check_if_string_contains_given_letters(letters=word, string=self.letters)
        except ValueError:
            raise WordDoesNotMatchToPattern("Word without pattern letters has some not-user letters")

    def __check_if_pattern_match_to_anagram(self, pattern, anagram):
        try:
            self.check_if_word_has_pattern_letters(pattern, anagram)
            self.__check_if_word_without_pattern_letters_has_only_user_letters(pattern, anagram)
        except WordDoesNotMatchToPattern:
            return False
        else:
            return True

    def __get_letters_from_board(self):
        right_angle_letters, bridges_letters = set(), set()
        for pattern in self.patterns:
            if pattern.get_word_type() == WordType.BRIDGE:
                bridges_letters.add(pattern.get_letters())
            elif pattern.get_word_type() == WordType.RIGHT_ANGLE:
                right_angle_letters.add(pattern.get_letters())

        board_letters = ''.join(list(right_angle_letters))
        for first_letter, second_letter in bridges_letters:
            if first_letter == second_letter:
                board_letters += first_letter
        return board_letters

    def get_board_string(self):
        board_string = "\n"
        for row in self.board:
            board_string += f"{str(row)}\n"
        return board_string

    @staticmethod
    def get_indexes_with_letter_occurrences_from_string(letter, string):
        letter_occurrences = string.count(letter)
        occurrences_list = []
        try:
            for x in range(letter_occurrences):
                index = string.index(letter)
                occurrences_list.append(index + x)
                string = Algorithm.remove_letter_from_string_by_index(string, index)
        except ValueError:
            pass
        finally:
            return occurrences_list

    def __get_right_angle_moves(self, word, pattern):
        moves = []
        letter = pattern.get_letters()
        occurrences_list = Algorithm.get_indexes_with_letter_occurrences_from_string(letter, word)
        for index in occurrences_list:
            left_space_needed = index
            right_space_needed = len(word) - index - 1
            if left_space_needed <= pattern.get_empty_cells_on_left() and right_space_needed <= pattern.get_empty_cells_on_right():
                move = Move(word, self.board_utilities, left_space_needed, pattern)
                moves.append(move)
        return moves

    def __get_bridge_moves(self, word, pattern):
        moves = []
        bridge_letters = pattern.get_letters()
        difference = pattern.get_difference_between_bridge_letters()
        first_letter_occurrences = Algorithm.get_indexes_with_letter_occurrences_from_string(bridge_letters[0], word)
        for first_letter_occurrence in first_letter_occurrences:
            try:
                if word[first_letter_occurrence + difference] != bridge_letters[1]:
                    continue
            except IndexError:
                continue
            left_space_needed = first_letter_occurrence
            right_space_needed = len(word) - (first_letter_occurrence + difference + 1)
            if left_space_needed <= pattern.get_empty_cells_on_left() and right_space_needed <= pattern.get_empty_cells_on_right():
                moves.append(Move(word, self.board_utilities, left_space_needed, pattern))
        return moves

    @staticmethod
    def remove_letters_from_string(letters, string):
        for letter in letters:
            index = string.find(letter)
            string = Algorithm.remove_letter_from_string_by_index(string, index)
        return string

    @staticmethod
    def check_if_string_contains_given_letters(letters, string):
        for letter in letters:
            index = string.index(letter)
            string = Algorithm.remove_letter_from_string_by_index(string, index)
        return string

    @staticmethod
    def convert_moves_to_json(moves):
        moves_list = [{'word': move.get_word(), 'points': move.get_points(), 'coordinates': move.get_position()} for
                      move in
                      moves]
        return {'moves': moves_list, 'quantity': len(moves_list)}

    @staticmethod
    def remove_letter_from_string_by_index(word, index):
        if index >= 0:
            return word[:index] + word[index + 1:]
        else:
            return word

    @staticmethod
    def check_if_seven_letters_move(move):
        if len(move.get_word()) - len(move.get_pattern().get_letters()) == 7:
            return True
        else:
            return False

    @staticmethod
    def check_if_word_has_pattern_letters(pattern, anagram):
        try:
            Algorithm.check_if_string_contains_given_letters(pattern.get_letters(), anagram)  # check if word has letters from pattern
        except ValueError:
            raise WordDoesNotMatchToPattern("Word does not contain pattern letters")