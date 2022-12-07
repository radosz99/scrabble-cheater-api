import copy

from cheater_app.logic.anagram import find_anagrams
from cheater_app.logic.structures import Orientation, Move, WordType, Country
from cheater_app.logic import utils
from cheater_app.logic.pattern_finder import PatternFinder, Pattern
from cheater_app.logic import exceptions as exc
from cheater_app.logic import constants
from cheater_app.logic.board_utilities import BoardUtilities
from cheater_app.logger import logger
from cheater_app.logic.trie import check_if_contains_spanish_doubles


class Algorithm:
    def __init__(self, letters, board, country):
        self.country = country
        self.letters = self.parse_letters_string(letters)
        self.board = board
        self.patterns = self.__get_patterns()
        self.board_utilities = BoardUtilities(country)
        self.validate_letters_on_board()

    def __get_patterns(self):
        logger.info(f"Looking for patterns on board: {self.get_board_string()}")
        pattern_finder = PatternFinder()
        patterns = pattern_finder.create_patterns(self.board)
        logger.info(f"Created patterns:")
        for pattern in patterns:
            logger.info(pattern)
        return patterns

    def parse_letters_string(self, letters):
        letters = letters.lower()
        logger.debug(f"Parsing letters string - {letters}")
        letters_list = []
        skip_next = False
        for index, letter in enumerate(letters):
            if skip_next:
                skip_next = False
                continue
            if self.country == Country.ES and index < len(letters) - 1:
                letter, skip_next = check_if_contains_spanish_doubles(letters, index)
            letters_list.append(letter)
        logger.debug(f"Parsed letters string - {letters_list}")
        return letters_list

    def validate_letters_on_board(self):
        for row in self.board:
            for cell in row:
                if not self.board_utilities.check_if_letter_valid_in_country(cell) and cell != ' ':
                    raise exc.InvalidLettersOnBoardException(f"Letter '{cell}' is not supported for country {self.country.name}")

    def algorithm_engine(self, trie):
        logger.info("Starting algorithm engine")
        sorted_list_of_valid_moves = self.__get_moves(trie)
        return self.convert_moves_to_json(sorted_list_of_valid_moves)

    @utils.timing
    def __get_moves(self, trie):
        if self.__check_if_board_is_clear():
            logger.info("Board is clear, getting move from clear board")
            return self.__get_valid_moves_from_clear_board(find_anagrams(self.letters, trie))
        else:
            letters_from_board = self.__get_letters_from_board()
            letters_for_anagram = self.letters + letters_from_board
            logger.info(f"Board is not clear, looking for anagrams from player letters = {self.letters} and "
                        f"letters from board = {letters_from_board}")
            anagrams = find_anagrams(letters_for_anagram, trie)
            logger.info(f"Created {len(anagrams)} anagrams = {anagrams}")
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
            for pattern in self.patterns:
                if self.__check_if_pattern_match_to_anagram(pattern, word):
                    moves_from_word = self.__get_moves_by_word_type(pattern, word)
                    logger.debug(f"Created moves = {moves_from_word}")
                    moves.extend(moves_from_word)
        logger.info(f"Found {len(moves)} moves")
        return utils.get_sorted_list_by_attribute(moves, "_points")

    def __check_if_word_contains_only_user_letters(self, word):
        user_letters_copy = copy.copy(self.letters)
        try:
            logger.debug(f"Checking if word {word} contains only user letters = {user_letters_copy}")
            self.remove_items_from_list(word, user_letters_copy)
        except ValueError as e:
            raise exc.WordDoesNotMatchToPatternException(f"Word without pattern letters has some not-user letters - {str(e)}")

    def __check_if_pattern_match_to_anagram(self, pattern, anagram):
        anagram_copy = copy.copy(anagram)
        logger.debug(f"Checking if pattern = {pattern} match to word = {anagram}")
        try:
            word_without_pattern_letters = self.check_if_word_has_pattern_letters(pattern, anagram_copy)
            logger.debug(f"Word without letters from pattern = {word_without_pattern_letters}")
            self.__check_if_word_contains_only_user_letters(word_without_pattern_letters)
            logger.debug("Pattern has matched to anagram")
        except exc.WordDoesNotMatchToPatternException as e:
            logger.debug(f"Word {anagram} does not match to pattern - {pattern}, cause - {str(e)}")
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

        board_letters = list(right_angle_letters)
        logger.debug(f"Board letters before bridges = {board_letters}")
        for first_letter, second_letter in bridges_letters:
            if first_letter == second_letter:
                board_letters.append(first_letter)
        logger.debug(f"Board letters = {board_letters}")
        return board_letters

    def get_board_string(self):
        board_string = "\n"
        for row in self.board:
            board_string += f"{str(row)}\n"
        return board_string

    @staticmethod
    def get_indexes_of_item_in_list(item, lst):
        for index, element in enumerate(lst):
            if item == element:
                yield index

    def __get_right_angle_moves(self, word, pattern):
        moves = []
        letter = pattern.get_letters_list()[0]
        logger.debug(f"Word = {word}, letter from pattern = {letter}")
        occurrences_list = Algorithm.get_indexes_of_item_in_list(letter, word)
        for index in occurrences_list:
            logger.debug(f"Index of occurrence = {index}")
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
        first_letter_occurrences = Algorithm.get_indexes_of_item_in_list(bridge_letters[0], word)
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
    def remove_items_from_list(items, lst):
        logger.debug(f"Removing {items} from {lst}")
        for item in items:
            lst.remove(item)
        return lst

    @staticmethod
    def check_if_string_contains_given_letters(letters, string):
        for letter in letters:
            index = string.index(letter)
            string = Algorithm.remove_letter_from_string_by_index(string, index)
        return string

    @staticmethod
    def convert_moves_to_json(moves):
        moves_list = [{'word': move.get_word_string(), 'points': move.get_points(), 'coordinates': move.get_position()} for
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
            return Algorithm.remove_items_from_list(pattern.get_letters_list(), anagram)  # check if word has letters from pattern
        except ValueError:
            raise exc.WordDoesNotMatchToPatternException("Word does not contain pattern letters")