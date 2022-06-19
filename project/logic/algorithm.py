from .anagram import find_anagrams
from .structures import Orientation, Move, WordType, Country
from .pattern_finder import PatternFinder, Pattern
from .exceptions import WordDoesNotMatchToPattern
import operator
import copy


class Algorithm:
    def __init__(self, letters, board, country):
        self.letters = letters.lower()
        self.board = board
        self.patterns = self._get_patterns()
        self.country = Country[country.upper()]

    def _get_patterns(self):
        pattern_finder = PatternFinder(len(self.letters))
        patterns = pattern_finder.create_patterns(self.board)
        return patterns

    def algorithm_engine(self, trie):
        if self._check_if_board_is_clear():
            sorted_list_of_valid_moves = self._get_valid_moves_from_clear_board(find_anagrams(str(self.letters), trie))
        else:
            anagrams = find_anagrams(str(self.letters) + self._get_letters_from_board(), trie)
            sorted_list_of_valid_moves = self._get_valid_moves(anagrams)
        return self.convert_moves_to_json(sorted_list_of_valid_moves)

    def _check_if_board_is_clear(self):
        for x in range(15):
            for y in range(15):
                if self.board[x][y] != ' ':
                    return False
        return True

    def _get_move_instance_from_anagram_and_index(self, anagram, i):
        pattern = Pattern(orientation=Orientation.HORIZONTAL)
        return Move(anagram, self.country, i, pattern)

    def _get_all_possibilities_for_anagram_in_clear_board(self, anagram):
        return [self._get_move_instance_from_anagram_and_index(anagram, i) for i in range(len(anagram))]

    def _get_valid_moves_from_clear_board(self, anagrams):
        moves = []
        for anagram in anagrams:
            moves.extend(self._get_all_possibilities_for_anagram_in_clear_board(anagram))
        return sort_moves(moves)

    def _get_moves_base_on_word_type(self, pattern, anagram):
        if pattern.get_word_type() is WordType.RIGHT_ANGLE:
            return self._get_right_angle_moves(anagram, pattern)
        elif pattern.get_word_type() is WordType.BRIDGE:
            return self._get_bridge_moves(anagram, pattern)

    def _get_valid_moves(self, anagrams):
        moves = []
        for anagram in anagrams:
            for pattern in self.patterns:
                if self._check_if_pattern_match_to_anagram(pattern, anagram):
                    moves.extend(self._get_moves_base_on_word_type(pattern, anagram))
        moves = list(set(moves))
        return self.sort_moves(moves)

    def _check_if_word_without_pattern_letters_has_only_user_letters(self, pattern, word):
        try:
            word = self.remove_letters_from_string(pattern.get_letters(), word)
            self.check_if_string_contains_given_letters(letters=word, string=self.letters)
        except ValueError:
            raise WordDoesNotMatchToPattern("Word without pattern letters has some not-user letters")

    def _check_if_pattern_match_to_anagram(self, pattern, anagram):
        try:
            self.check_if_word_has_pattern_letters(pattern, anagram)
            self._check_if_word_without_pattern_letters_has_only_user_letters(pattern, anagram)
        except WordDoesNotMatchToPattern:
            return False
        else:
            return True

    def _get_letters_from_board(self):
        board_letters = ''
        bridges = {}
        for pattern in self.patterns:
            if pattern.get_word_type() == WordType.BRIDGE:
                bridges[pattern.get_letters()] = pattern.get_difference_between_bridge_letters()
            elif pattern.get_word_type() == WordType.RIGHT_ANGLE:
                board_letters += pattern.get_letters()

        letters = "".join(set(board_letters))

        for key in bridges:
            position_first, position_second = letters.find(key[0]), letters.find(key[1])
            if position_first == -1 and position_second == -1:
                letters += key[0]
                letters += key[1]
            elif position_first == position_second:
                letters += key[0]
            elif position_first == -1:
                letters += key[0]
            elif position_second == -1:
                letters += key[1]
        return letters

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


    def _get_right_angle_moves(self, word, pattern):
        if (pattern.get_x() == 6 and pattern.get_y() == 3 and word == "ananite"):
            print(f"mamy xd = {pattern}")
        moves = []
        letter = pattern.get_letters()
        occurrences_list = Algorithm.get_indexes_with_letter_occurrences_from_string(letter, word)

        for index in occurrences_list:
            left_space_needed = index
            right_space_needed = len(word) - index - 1
            if left_space_needed <= pattern.get_empty_cells_on_left() and right_space_needed <= pattern.get_empty_cells_on_right():
                move = Move(word, self.country, left_space_needed, pattern)
                moves.append(move)
        return moves

    def _get_bridge_moves(self, word, pattern):
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
                moves.append(Move(word, self.country, left_space_needed, pattern))
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

    @staticmethod
    def convert_moves_to_json(moves):
        moves_list = [{'word': move.get_word(), 'points': move.get_points(), 'coordinates': move.get_position()} for
                      move in
                      moves]
        return {'moves': moves_list, 'quantity': len(moves_list)}

    @staticmethod
    def remove_letter_from_string_by_index(word, index):
        return word[:index] + word[index + 1:]

    @staticmethod
    def check_if_seven_letters_move(move):
        if len(move.get_word()) - len(move.get_pattern().get_letters()) == 7:
            return True
        else:
            return False

    @staticmethod
    def get_sorted_list_by_attribute(list, attr):
        list.sort(key=operator.attrgetter(attr), reverse=True)
        return list

    @staticmethod
    def sort_moves(moves):
        return Algorithm.get_sorted_list_by_attribute(moves, '_points')

    @staticmethod
    def check_if_word_has_pattern_letters(pattern, anagram):
        try:
            Algorithm.check_if_string_contains_given_letters(pattern.get_letters(), anagram)  # check if word has letters from pattern
        except ValueError:
            raise WordDoesNotMatchToPattern("Word does not contain pattern letters")