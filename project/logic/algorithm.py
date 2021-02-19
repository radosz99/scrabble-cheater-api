from .anagram import find_anagrams
from enum import Enum
import operator


class Algorithm:
    def __init__(self, letters, board, country):
        self.letters = [x.lower() for x in letters]
        self.board = board
        pattern_finder = PatternFinder()
        self.patterns = pattern_finder.create_patterns(board)
        self.country = country

    def algorithm_engine(self, trie):
        if(self._check_if_board_is_clear()):
            sorted_list_of_valid_moves = self._get_valid_moves_from_clear_board(find_anagrams(str(self.letters), trie))
        else:
            sorted_list_of_valid_moves = self._get_valid_moves(find_anagrams(str(self.letters) + self._get_letters_from_board(), trie))
        return self._convert_moves_to_json(sorted_list_of_valid_moves)

    def _check_if_board_is_clear(self):
        for x in range(15):
            for y in range(15):
                if(self.board[x][y] != ' '):
                    return False
        return True

    def _get_valid_moves_from_clear_board(self, anagrams):
        moves = []
        for anagram in [anagram for anagram in anagrams if len(anagram) > 1]:
            for i in range(len(anagram)):
                start_x = 7
                start_y = 7 - i
                position = self._get_position_from_coordinates_according_to_orientation(start_x, start_y, Orientation.horizontal)
                moves.append(Move(position, anagram, pattern=Pattern(x=7, y=7, orientation=Orientation.horizontal), left_space_needed=i))
        return self._sort_moves(moves)

    def _convert_moves_to_json(self, moves):
        word_list = []
        for move in moves:
            word_json = {}
            word_json['word'] = move.get_word()
            word_json['points'] = move.get_points()
            word_json['coordinate'] = move.get_position()
            word_list.append(word_json)

        words_in_json = {}
        words_in_json['words'] = word_list
        words_in_json['quantity'] = len(word_list)
        return words_in_json

    def _get_position_from_coordinates_according_to_orientation(self, start_x, start_y, orientation, empty_cells_on_left=0):
        if(orientation == Orientation.vertical):
            x = start_x - empty_cells_on_left
            y = start_y
        elif(orientation == Orientation.horizontal):
            x = start_x
            y = start_y - empty_cells_on_left
        return str(x) + str(chr(65 + y))

    def _get_valid_moves(self, anagrams):
        moves = []
        for anagram in anagrams:
            for pattern in self.patterns:
                if(self._check_if_pattern_match_to_anagram(pattern, anagram)):
                    if(pattern.get_word_type() == WordType.RIGHT_ANGLE):
                        moves.extend(self._get_right_angle_moves(anagram, pattern))
                    if(pattern.get_word_type() == WordType.BRIDGE):
                        moves.extend(self._get_bridge_moves(anagram, pattern))

        moves = list(set(moves))

        return self._sort_moves(moves)

    def _get_right_angle_moves(self, word, pattern):
        moves = []
        word_copy = word
        letter = pattern.get_letters()
        letter_occurences = word.count(letter)
        occurences_dict = {}
        for x in range(letter_occurences):
            index = word_copy.find(letter)
            word_copy = word_copy[:index] + word_copy[index + 1:]
            occurences_dict[x] = index + x

        for value in occurences_dict.values():
            left_space_needed = value
            right_space_needed = len(word) - value - 1
            if(left_space_needed <= pattern.get_empty_cells_on_left() and right_space_needed <= pattern.get_empty_cells_on_right()):
                moves.append(Move(self._get_position_from_coordinates_according_to_orientation(pattern.get_x(), pattern.get_y(), pattern.get_orientation(), left_space_needed), word, left_space_needed, pattern))
        return moves

    def _get_bridge_moves(self, word, pattern):
        moves = []
        first, second = self._get_bridge_letters_indexes_in_word(pattern.get_letters(), word)
        left_space_needed = first
        right_space_needed = len(word) - second - 1
        if(left_space_needed <= pattern.get_empty_cells_on_left() and right_space_needed <= pattern.get_empty_cells_on_right()):
            moves.append(Move(self._get_position_from_coordinates_according_to_orientation(pattern.get_x(), pattern.get_y(), pattern.get_orientation(), left_space_needed), word, left_space_needed, pattern))
        return moves

    def _sort_moves(self, moves):
        for move in moves:
            move.set_points(self._evaluate_move(move))

        moves.sort(key=operator.attrgetter("_points"))
        return moves

    def _evaluate_move(self, move):
        value = 0
        for x in range(len(move.get_word())):
            value += self._evaluate_letter_value(x, move)
        multiplier = self._calculate_overall_word_multiplier(move)

        bonus = 50 if(len(move.get_word()) - len(move.get_pattern().get_letters()) == 7) else 0
        return value * multiplier + bonus

    def _evaluate_letter_value(self, counter, move):
        if(move.get_pattern().get_orientation() == Orientation.vertical):
            start_x = move.get_pattern().get_x() - move.left_space_needed + counter
            start_y = move.get_pattern().get_y()
        elif(move.get_pattern().get_orientation() == Orientation.horizontal):
            start_x = move.get_pattern().get_x()
            start_y = move.get_pattern().get_y() - move.left_space_needed + counter

        letter_value = self._get_char_value(move.get_word()[counter])
        letter_multiplier = 1
        if(self._check_if_letter_is_newly_put(start_x, start_y, move.get_pattern())):
            letter_multiplier = self._get_field_letter_multiplier(start_x, start_y)
        return letter_multiplier * letter_value

    def _check_if_letter_is_newly_put(self, x, y, pattern):
        if(pattern.get_word_type() == WordType.RIGHT_ANGLE):
            return self._check_if_letter_is_newly_put_in_right_angle(x, y, pattern)
        elif(pattern.get_word_type() == WordType.BRIDGE):
            return self._check_if_letter_is_newly_put_in_bridge(x, y, pattern)

    def _check_if_letter_is_newly_put_in_right_angle(self, x, y, pattern):
        if(x == pattern.get_x() and y == pattern.get_y()):
            return False
        else:
            return True

    def _check_if_letter_is_newly_put_in_bridge(self, x, y, pattern):
        if(pattern.get_orientation() == Orientation.vertical):
            second_x = pattern.get_x() + pattern.get_difference_between_bridge_letters() - 1
            second_y = pattern.get_y()
        elif(pattern.get_orientation() == Orientation.horizontal):
            second_x = pattern.get_x()
            second_y = pattern.get_y() + pattern.get_difference_between_bridge_letters() - 1
        if((x == pattern.get_x() and y == pattern.get_y()) or (x == second_x and y == second_y)):
            return False
        else:
            return True

    def _get_field_letter_multiplier(self, x, y):
        if(((x == 5 or x == 9) and (y == 1 or y == 5 or y == 9 or y == 13)) or ((x == 1 or x == 13) and (y == 5 or y == 9))):
            return 3
        elif(((x == 0 or x == 7 or x == 14) and (y == 3 or y == 11)) or ((x == 3 or x == 11) and (y == 0 or y == 7 or y == 14)) or((x == 2 or x == 6 or x == 8 or x == 12) and (y == 6 or y == 8)) or((y == 2 or y == 6 or y == 8 or y == 12) and (x == 6 or x == 8))):
            return 2
        else:
            return 1

    def _calculate_overall_word_multiplier(self, move):
        multiplier = 1
        if(move.get_pattern().get_orientation() == Orientation.vertical):
            start_x = move.get_pattern().get_x() - move.left_space_needed
            start_y = move.get_pattern().get_y()
        elif(move.get_pattern().get_orientation() == Orientation.horizontal):
            start_x = move.get_pattern().get_x()
            start_y = move.get_pattern().get_y() - move.left_space_needed

        for x in range(len(move.get_word())):
            if(self._check_if_letter_is_newly_put(start_x, start_y, move.get_pattern()) or self._check_if_board_is_clear()):
                multiplier *= self._get_field_word_multiplier(start_x, start_y)
            if(move.get_pattern().get_orientation() == Orientation.vertical):
                start_x += 1
            if(move.get_pattern().get_orientation() == Orientation.horizontal):
                start_y += 1
        return multiplier

    def _get_field_word_multiplier(self, x, y):
        if(((x == 1 or x == 13) and (y == 1 or y == 13)) or ((x == 2 or x == 12) and (y == 2 or y == 12)) or ((x == 3 or x == 11) and (y == 3 or y == 11)) or ((x == 4 or x == 10) and (y == 4 or y == 10)) or (x == 7 and y == 7)):
            return 2
        elif(((x == 0 or x == 14) and (y == 0 or y == 7 or y == 14)) or (x == 7 and (y == 0 or y == 14))):
            return 3
        else:
            return 1

    def _check_if_pattern_match_to_anagram(self, pattern, anagram):
        if(self._check_if_word_contains_letters(pattern.get_letters(), anagram)):
            if(pattern.get_word_type() == WordType.BRIDGE):
                if(not self._check_if_correct_difference_in_bridge(pattern, anagram)):
                    return False
            if(self._check_if_word_contains_only_user_letters(pattern, anagram)):
                return True
            else:
                return False
        else:
            return False

    def _check_if_correct_difference_in_bridge(self, pattern, word):
        first_letter, second_letter = pattern.get_letters()[0], pattern.get_letters()[1]

        first_letter_occurences = word.count(first_letter)

        for x in range(first_letter_occurences):
            index = word.find(first_letter)
            try:
                if(word[index + pattern.get_difference_between_bridge_letters()] == second_letter):
                    return True
            except IndexError:
                pass
            word = word[:index] + word[index + 1:]

    def _check_if_word_contains_only_user_letters(self, pattern, word):
        user_letters = ''.join(self.letters)
        word = self._remove_letters_from_word(pattern.get_letters(), word)
        return self._check_if_word_contains_letters(word, user_letters)

    def _check_if_word_contains_letters(self, letters, word):
        for letter in letters:
            index = word.find(letter)
            if(index == -1):
                return False
            else:
                word = word[:index] + word[index + 1:]
        return True

    def _remove_letters_from_word(self, letters, word):
        for letter in letters:
            index = word.find(letter)
            word = word[:index] + word[index + 1:]
        return word

    def _get_bridge_letters_indexes_in_word(self, letters, word):
        first = word.find(letters[0])
        word = word[:first] + word[first + 1:]
        second = word.find(letters[1]) + 1
        return first, second

    def _get_char_value(self, char):
        if(self.country == 'pl'):
            if(char == 'a' or char == 'e' or char == 'i' or char == 'n' or char == 'o' or char == 'r' or char == 's' or char == 'w' or char == 'z'):
                return 1
            if(char == 'c' or char == 'd' or char == 'k' or char == 'l' or char == 'm' or char == 'p' or char == 't' or char == 'y'):
                return 2
            if(char == 'b' or char == 'g' or char == 'h' or char == 'j' or char == 'ł' or char == 'u'):
                return 3
            if(char == 'ą' or char == 'ę' or char == 'f' or char == 'ó' or char == 'ś' or char == 'ż'):
                return 5
            if(char == 'ć'):
                return 6
            if(char == 'ń'):
                return 7
            if(char == 'ź'):
                return 9

        if(self.country == 'gb'):
            if(char == 'a' or char == 'e' or char == 'i' or char == 'n' or char == 'o' or char == 'r' or char == 's' or char == 't' or char == 'u' or char == 'l'):
                return 1
            if(char == 'g' or char == 'd'):
                return 2
            if(char == 'b' or char == 'c' or char == 'm' or char == 'p'):
                return 3
            if(char == 'h' or char == 'v' or char == 'w' or char == 'y' or char == 'f'):
                return 4
            if(char == 'k'):
                return 5
            if(char == 'j' or char == 'x'):
                return 8
            if(char == 'q' or char == 'z'):
                return 10
        return 1

    def _get_letters_from_board(self):
        board_letters = ''
        bridges = {}
        for pattern in self.patterns:
            if(pattern.get_word_type() == WordType.BRIDGE):
                bridges[pattern.get_letters()] = pattern.get_difference_between_bridge_letters()
            elif(pattern.get_word_type() == WordType.RIGHT_ANGLE):
                board_letters += pattern.get_letters()

        letters = "".join(set(board_letters))

        for key in bridges:
            position_first, position_second = letters.find(key[0]), letters.find(key[1])
            if(position_first == -1 and position_second == -1):
                letters += key[0]
                letters += key[1]
            elif(position_first == position_second):
                letters += key[0]
            elif(position_first == -1):
                letters += key[0]
            elif(position_second == -1):
                letters += key[1]
        return letters


class PatternFinder:
    def __init__(self):
        self._user_letters_quantity = 7
        self.patterns = []

    def create_patterns(self, board):
        self._create_right_angle_patterns(board)
        self._create_bridge_patterns(board)
        return self.patterns

    def _create_right_angle_patterns(self, board):
        self._create_right_angle_patterns_for_orientation(board, Orientation.horizontal)
        self._create_right_angle_patterns_for_orientation(self._transpose_board(board), Orientation.vertical)

    def _create_bridge_patterns(self, board):
        self._create_bridge_patterns_for_orientation(board, Orientation.horizontal)
        self._create_bridge_patterns_for_orientation(self._transpose_board(board), Orientation.vertical)

    def _create_bridge_patterns_for_orientation(self, board, orientation):
        for pattern in self.patterns:
            if(pattern.get_orientation() != orientation):
                continue
            if(orientation == Orientation.horizontal):
                x, y = pattern.get_x(), pattern.get_y()
            elif(orientation == Orientation.vertical):
                x, y = self._transpose_letters_coordinates(pattern.get_x(), pattern.get_y())

            y_coord = self._get_nearest_left_cell(x, y, board)
            if(y_coord >= 0):
                difference = y - y_coord
                if(self._check_if_not_adjacent_to_left(board, x, y_coord) and difference <= 8):
                    bridge = board[x][y_coord] + board[x][y]
                    letters_to_put_not_between = self._user_letters_quantity - (difference - 1)
                    max_cells_on_left = min(self._get_empty_cells_on_the_left(x, y_coord, board), letters_to_put_not_between)
                    max_cells_on_right = min(self._get_empty_cells_on_the_right(x, y, board), letters_to_put_not_between)

                    for i in range(max_cells_on_left + 1):
                        index_right = min(letters_to_put_not_between - i, max_cells_on_right)
                        if(orientation == Orientation.horizontal):
                            self.patterns.append(Pattern(bridge, x, y_coord, i, index_right, orientation, difference))
                        elif(orientation == Orientation.vertical):
                            x_bridge, y_bridge = self._untranspose_letters_coordinates(x, y_coord)
                            self.patterns.append(Pattern(bridge, x_bridge, y_bridge, i, index_right, orientation, difference))

    def _get_nearest_left_cell(self, x, y, board):
        counter = 0
        while(True):
            index = y - counter - 1
            if(index == 0):
                return -1
            if(board[x][index] == ' '):
                counter += 1
                if(not self._check_if_cell_has_got_no_vertical_neighbors(board, x, y - counter)):
                    return -1
            else:
                return index

    def _transpose_letters_coordinates(self, x, y):
        help_x = x
        x = 14 - y
        y = help_x
        return x, y

    def _untranspose_letters_coordinates(self, x, y):
        help_y = y
        y = 14 - x
        x = help_y
        return x, y

    def _create_right_angle_patterns_for_orientation(self, board, orientation):
        for x in range(15):
            for y in range(15):
                self._create_all_letter_right_angle_patterns(board, x, y, orientation)

    def _create_all_letter_right_angle_patterns(self, board, x, y, node_orient):
        if(self._check_if_cell_can_be_right_angle_pattern(board, x, y)):
            empty_cells_on_left = self._get_empty_cells_on_the_left(x, y, board)
            empty_cells_on_right = self._get_empty_cells_on_the_right(x, y, board)

            if(empty_cells_on_right != 0 or empty_cells_on_left != 0):
                self._make_right_angle_patterns(empty_cells_on_left, empty_cells_on_right, node_orient, board, x, y)

    def _check_if_cell_can_be_right_angle_pattern(self, board, x, y):
        return self._check_if_cell_has_got_no_horizontal_neighbors(board, x, y) and self._check_if_cell_is_occupied(board, x, y)

    def _check_if_cell_is_occupied(self, board, x, y):
        return False if board[x][y] == ' ' else True

    def _check_if_cell_has_got_no_horizontal_neighbors(self, board, x, y):
        return self._check_if_not_adjacent_to_left(board, x, y) and self._check_if_not_adjacent_to_right(board, x, y)

    def _transpose_board(self, board):
        return [([board[y][14 - x] for y in range(15)]) for x in range(15)]

    def _get_empty_cells_on_the_left(self, x, y, board):
        empty_cells_on_left = 0
        while(self._check_if_left_cell_is_available(board, x, y - empty_cells_on_left)):
            empty_cells_on_left += 1
        return empty_cells_on_left if empty_cells_on_left < 7 else 7

    def _check_if_left_cell_is_available(self, board, x, y):
        if(y == 0):
            return False

        return self._check_if_cell_has_got_no_vertical_neighbors(board, x, y - 1) and self._check_if_not_adjacent_to_left(board, x, y - 1)

    def _check_if_cell_has_got_no_vertical_neighbors(self, board, x, y):
        return self._check_if_not_adjacent_to_top(board, x, y) and self._check_if_not_adjacent_to_bottom(board, x, y)

    def _check_if_not_adjacent_to_top(self, board, x, y):
        if(self._check_if_cell_is_in_top_row(x)):
            return True
        elif(self._check_if_cell_on_the_top_is_empty(board, x, y)):
            return True
        else:
            return False

    def _check_if_cell_on_the_top_is_empty(self, board, x, y):
        if(board[x - 1][y] == ' '):
            return True
        else:
            return False

    def _check_if_cell_is_in_top_row(self, x):
        if(x == 0):
            return True
        else:
            return False

    def _check_if_not_adjacent_to_bottom(self, board, x, y):
        if(self._check_if_cell_is_in_bottom_row(x)):
            return True
        elif(self._check_if_cell_on_the_bottom_is_empty(board, x, y)):
            return True
        else:
            return False

    def _check_if_cell_on_the_bottom_is_empty(self, board, x, y):
        if(board[x + 1][y] == ' '):
            return True
        else:
            return False

    def _check_if_cell_is_in_bottom_row(self, x):
        if(x == 14):
            return True
        else:
            return False

    def _check_if_not_adjacent_to_left(self, board, x, y):
        if(self._check_if_cell_is_in_left_column(y)):
            return True
        elif(self._check_if_cell_on_the_left_is_empty(board, x, y)):
            return True
        else:
            return False

    def _check_if_cell_is_in_left_column(self, y):
        if(y == 0):
            return True
        else:
            return False

    def _check_if_cell_on_the_left_is_empty(self, board, x, y):
        if(board[x][y - 1] == ' '):
            return True
        else:
            return False

    def _check_if_not_adjacent_to_right(self, board, x, y):
        if(self._check_if_cell_is_in_right_column(y)):
            return True
        elif(self._check_if_cell_on_the_right_is_empty(board, x, y)):
            return True
        else:
            return False

    def _check_if_cell_is_in_right_column(self, y):
        if(y == 14):
            return True
        else:
            return False

    def _check_if_cell_on_the_right_is_empty(self, board, x, y):
        if(board[x][y + 1] == ' '):
            return True
        else:
            return False

    def _check_if_right_cell_is_available(self, board, x, y):
        if(y == 14):
            return False
        top_not_adjacent = self._check_if_not_adjacent_to_top(board, x, y + 1)
        bottom_not_adjacent = self._check_if_not_adjacent_to_bottom(board, x, y + 1)
        right_not_adjacent = self._check_if_not_adjacent_to_right(board, x, y + 1)
        return top_not_adjacent and bottom_not_adjacent and right_not_adjacent

    def _get_empty_cells_on_the_right(self, x, y, board):
        empty_cells_on_right = 0
        while(self._check_if_right_cell_is_available(board, x, y + empty_cells_on_right)):
            empty_cells_on_right += 1
        return empty_cells_on_right if empty_cells_on_right < 7 else 7

    def _get_coordinates_according_to_board_orientation(self, orientation, x, y):
        if(orientation == Orientation.horizontal):
            return x, y
        elif(orientation == Orientation.vertical):
            return y, 14 - x

    def _make_right_angle_patterns(self, empty_left, empty_right, orientation, board, x, y):
        pattern_board = []
        empty_left = 7 if empty_left > 7 else empty_left
        for i in range(empty_left + 1):
            free_cells_on_right = empty_right if (i + empty_right <= 7) else 7 - i
            real_x, real_y = self._get_coordinates_according_to_board_orientation(orientation, x, y)
            self.patterns.append(Pattern(board[x][y].lower(), real_x, real_y, i, free_cells_on_right, orientation))
        return pattern_board


class Orientation(Enum):
    horizontal = 1
    vertical = 2


class WordType(Enum):
    RIGHT_ANGLE = 1
    BRIDGE = 2


class Pattern():
    def __init__(self, letters="", x=0, y=0, empty_cells_on_left=0, empty_cells_on_right=0, orientation=None, difference_between_bridge_letters=0, word_type=WordType.RIGHT_ANGLE):
        self._letters = str(letters)
        self._x = x
        self._y = y
        self._empty_cells_on_left = empty_cells_on_left
        self._empty_cells_on_right = empty_cells_on_right
        self._orientation = orientation
        self._difference_between_bridge_letters = difference_between_bridge_letters
        self._word_type = WordType.BRIDGE if(len(letters) == 2) else WordType.RIGHT_ANGLE

    def __str__(self):
        return(f" {self._letters}, x = {self._x}, y = {self._y}, lc = {self._empty_cells_on_left}, rc = {self._empty_cells_on_right}, {self._orientation}, diff = {self._difference_between_bridge_letters}, {self._word_type}")

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def get_empty_cells_on_left(self):
        return self._empty_cells_on_left

    def get_empty_cells_on_right(self):
        return self._empty_cells_on_right

    def get_difference_between_bridge_letters(self):
        return self._difference_between_bridge_letters

    def get_orientation(self):
        return self._orientation

    def get_letters(self):
        return self._letters

    def get_word_type(self):
        return self._word_type


class Move():
    def __init__(self, position, word, left_space_needed=0, pattern=None):
        self._position = position
        self._pattern = pattern
        self._word = word
        self._points = 0
        self.left_space_needed = left_space_needed

    def __str__(self):
        return(f" {self._position}, word = {self._word}, points = {self._points}")

    def __hash__(self):
        return hash(('position', self._position, 'word', self._word))

    def __eq__(self, other):
        return self._position == other._position and self._word == other._word

    def set_points(self, points):
        self._points = points

    def get_pattern(self):
        return self._pattern

    def get_position(self):
        return self._position

    def get_points(self):
        return self._points

    def get_word(self):
        return self._word
