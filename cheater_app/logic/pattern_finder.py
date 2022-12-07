from cheater_app.logic.structures import WordType, Orientation, Letter
from cheater_app.logic.utils import remove_duplicates_from_list
from cheater_app.logic import exceptions as exc
from cheater_app.logic.constants import BOARD_SIZE, BOARD_MAX_INDEX, BOARD_MIN_INDEX, BOARD_MIDDLE
from cheater_app.logger import logger


class Pattern:
    def __init__(self, letters=None, x=BOARD_MIDDLE, y=BOARD_MIDDLE, empty_cells_on_left=0, empty_cells_on_right=0, orientation=None, difference_between_bridge_letters=0):
        self._letters = letters if letters else []
        self._x = x
        self._y = y
        self._empty_cells_on_left = empty_cells_on_left
        self._empty_cells_on_right = empty_cells_on_right
        self._orientation = orientation
        self._difference_between_bridge_letters = difference_between_bridge_letters
        self._word_type = WordType.BRIDGE if(len(self._letters) == 2) else WordType.RIGHT_ANGLE
        self._letters_list = self._create_letters_list()

    def __str__(self):
        return f" {self._letters}, x = {self._x}, y = {self._y}, lc = {self._empty_cells_on_left}, rc = {self._empty_cells_on_right}, {self._orientation}, diff = {self._difference_between_bridge_letters}, {self._word_type}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        coordinates = self._x == other.get_x() and self._y == other.get_y()
        empty_cells = self._empty_cells_on_left == other.get_empty_cells_on_left() and self._empty_cells_on_right == other.get_empty_cells_on_right()
        letters = self._letters == other.get_letters()
        orientation = self._orientation == other.get_orientation()
        return coordinates and empty_cells and letters and orientation

    def __hash__(self):
        return hash((self._x, self._y, self._empty_cells_on_right, self._empty_cells_on_left, self._orientation, str(self._letters)))

    def _create_letters_list(self):
        if not self._letters:
            return []

        letters_list = [Letter(self._x, self._y, self._letters[0], False)]
        if self._word_type is WordType.BRIDGE:
            if self._orientation is Orientation.VERTICAL:
                letters_list.append(Letter(self._x + self._difference_between_bridge_letters, self._y, self._letters[1], False))
            elif self._orientation is Orientation.HORIZONTAL:
                letters_list.append(Letter(self._x, self._y + self._difference_between_bridge_letters, self._letters[1], False))
        return letters_list

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def get_letters_instances_list(self):
        return self._letters_list

    def get_empty_cells_on_left(self):
        return self._empty_cells_on_left

    def get_empty_cells_on_right(self):
        return self._empty_cells_on_right

    def get_difference_between_bridge_letters(self):
        return self._difference_between_bridge_letters

    def get_orientation(self):
        return self._orientation

    def get_letters(self):
        if self._word_type == WordType.BRIDGE:
            return self._letters[0], self._letters[1]
        else:
            return self._letters[0]

    def get_letters_list(self):
        return self._letters

    def get_word_type(self):
        return self._word_type


def transpose_letters_coordinates(x, y):
    return BOARD_MAX_INDEX - y, x


def untranspose_letters_coordinates(x, y):
    return y, BOARD_MAX_INDEX - x


def transpose_board(board):
    return [([board[y][BOARD_MAX_INDEX - x] for y in range(BOARD_SIZE)]) for x in range(BOARD_SIZE)]


def check_if_cell_is_empty(board, x, y):
    if x < 0 or y < 0:
        return True
    try:
        return True if board[x][y] == ' ' else False
    except IndexError:
        return True


def check_if_cell_on_the_top_is_empty(board, x, y):
    return True if check_if_cell_is_empty(board, x - 1, y) else False


def check_if_no_tiles_on_top(board, x, y):
    return True if check_if_cell_on_the_top_is_empty(board, x, y) else False


def check_if_cell_on_the_bottom_is_empty(board, x, y):
    return True if check_if_cell_is_empty(board, x + 1, y) else False


def check_if_no_tiles_on_bottom(board, x, y):
    return True if check_if_cell_on_the_bottom_is_empty(board, x, y) else False


def check_if_cell_on_the_left_is_empty(board, x, y):
    return True if check_if_cell_is_empty(board, x, y - 1) else False


def check_if_no_tiles_on_left(board, x, y):
    return True if check_if_cell_on_the_left_is_empty(board, x, y) else False


def check_if_cell_on_the_right_is_empty(board, x, y):
    return True if check_if_cell_is_empty(board, x, y + 1) else False


def check_if_no_tiles_on_right(board, x, y):
    return True if check_if_cell_on_the_right_is_empty(board, x, y) else False


def get_real_coordinates_according_to_board_orientation(orientation, x, y):
    if orientation == Orientation.HORIZONTAL:
        return x, y
    elif orientation == Orientation.VERTICAL:
        return untranspose_letters_coordinates(x, y)


def check_if_cell_has_got_no_vertical_neighbors(board, x, y):
    return check_if_no_tiles_on_top(board, x, y) and check_if_no_tiles_on_bottom(board, x, y)


def check_if_cell_has_got_no_horizontal_neighbors(board, x, y):
    return check_if_no_tiles_on_left(board, x, y) and check_if_no_tiles_on_right(board, x, y)


def check_if_right_cell_is_available(board, x, y):
    if y == BOARD_MAX_INDEX:
        return False
    return check_if_cell_has_got_no_vertical_neighbors(board, x, y + 1) and check_if_no_tiles_on_right(board, x, y + 1)


def check_if_left_cell_is_available(board, x, y):
    if y == BOARD_MIN_INDEX:
        return False
    return check_if_cell_has_got_no_vertical_neighbors(board, x, y - 1) and check_if_no_tiles_on_left(board, x, y - 1)


def get_empty_cells_on_the_right(x, y, board):
    empty_cells_on_right = 0
    while check_if_right_cell_is_available(board, x, y + empty_cells_on_right):
        empty_cells_on_right += 1
    return empty_cells_on_right


def get_empty_cells_on_the_left(x, y, board):
    empty_cells_on_left = 0
    while check_if_left_cell_is_available(board, x, y - empty_cells_on_left):
        empty_cells_on_left += 1
    return empty_cells_on_left


def get_empty_cells_on_both_sides(x, y, board):
    return get_empty_cells_on_the_left(x, y, board), get_empty_cells_on_the_right(x, y, board)


def check_if_cell_can_be_right_angle_pattern(board, x, y):
    if check_if_cell_is_empty(board, x, y):
        raise exc.NotRightAnglePatternException(f"can't be right angle pattern because it's empty")
    if not check_if_cell_has_got_no_horizontal_neighbors(board, x, y):
        raise exc.NotRightAnglePatternException(f"can't be right angle pattern because it has neighbors in given orientation")
    empty_cells_on_left, empty_cells_on_right = get_empty_cells_on_both_sides(x, y, board)
    logger.debug(f"Empty cells on left = {empty_cells_on_left}, on right = {empty_cells_on_right}")
    if empty_cells_on_left == 0 and empty_cells_on_right == 0:
        raise exc.NotRightAnglePatternException(f"can't be right angle pattern because none of the cells on both sides is accessible")


def check_if_cell_can_be_part_of_bridge_pattern(board, x, y, y_pattern):
    if not check_if_cell_is_empty(board, x, y - 1):
        raise exc.NotPartOfBridgePatternException(f" can't be part of the bridge because it has neighbor")
    for i in range(y + 1, y_pattern):
        if not check_if_cell_has_got_no_vertical_neighbors(board, x, i):
            raise exc.NotPartOfBridgePatternException(f"can't be part of the bridge because there are some not empty cells between")


def get_coordinates_from_pattern_with_optional_transposition(pattern):
    if pattern.get_orientation() == Orientation.HORIZONTAL:
        return pattern.get_x(), pattern.get_y()
    elif pattern.get_orientation() == Orientation.VERTICAL:
        return transpose_letters_coordinates(pattern.get_x(), pattern.get_y())


def get_amount_of_available_cells_outside_the_bridge(x, y, y_coord, board):
    return get_empty_cells_on_the_left(x, y_coord, board), get_empty_cells_on_the_right(x, y, board)


class PatternFinder:
    def __init__(self):
        self.patterns = []

    def create_patterns(self, board):
        self._create_right_angle_patterns(board)
        self._create_bridge_patterns(board)
        self.patterns = remove_duplicates_from_list(self.patterns)
        return self.patterns

    def _create_right_angle_patterns(self, board):
        self._create_right_angle_patterns_for_orientation(board, Orientation.HORIZONTAL)
        self._create_right_angle_patterns_for_orientation(transpose_board(board), Orientation.VERTICAL)

    def _create_bridge_patterns(self, board):
        self._create_bridge_patterns_for_orientation(board, Orientation.HORIZONTAL)
        self._create_bridge_patterns_for_orientation(transpose_board(board), Orientation.VERTICAL)

    @staticmethod
    def flip_board_horizontally(board):
        flipped_board = []
        for line in board:
            flipped_board.append(line[::-1])
        return flipped_board

    @staticmethod
    def _get_bridge_pattern_from_pattern_and_nearest_suitable_cell_on_right(board, pattern, y_nearest):
        return PatternFinder._get_bridge_pattern_from_pattern_and_nearest_suitable_cell_on_left(board, pattern, y_nearest, True)

    @staticmethod
    def _get_bridge_pattern_from_pattern_and_nearest_suitable_cell_on_left(board, pattern, y_nearest, reversed=False):
        x, y = get_coordinates_from_pattern_with_optional_transposition(pattern)
        if reversed:
            y, y_nearest = y_nearest, y
        orientation = pattern.get_orientation()
        difference = y - y_nearest
        bridge_letters = [board[x][y_nearest].lower(), board[x][y].lower()]
        cells_on_left, cells_on_right = get_amount_of_available_cells_outside_the_bridge(x, y, y_nearest, board)
        real_x, real_y = get_real_coordinates_according_to_board_orientation(orientation, x, y_nearest)
        return Pattern(bridge_letters, real_x, real_y, cells_on_left, cells_on_right, orientation, difference)

    def _create_bridge_patterns_for_orientation(self, board, orientation):
        for pattern in self.patterns:
            if pattern.get_orientation() != orientation or pattern.get_word_type() is WordType.BRIDGE:
                continue
            logger.debug(f"Looking for nearest matching cell for pattern = {pattern}")
            try:

                y_nearest = PatternFinder._get_nearest_cell_index_on_left(pattern, board)
                logger.debug(f"Nearest cell index on left = {y_nearest}")
                new_pattern = PatternFinder._get_bridge_pattern_from_pattern_and_nearest_suitable_cell_on_left(board, pattern, y_nearest)
                logger.debug(f"New bridge pattern = {new_pattern}")
                self.patterns.append(new_pattern)
            except exc.NoMatchingRightAngleException as e:
                logger.debug(e)

            try:
                y_nearest = PatternFinder._get_nearest_cell_index_on_right(pattern, board)
                logger.debug(f"Nearest cell index on right = {y_nearest}")
                new_pattern = PatternFinder._get_bridge_pattern_from_pattern_and_nearest_suitable_cell_on_right(board, pattern, y_nearest)
                logger.debug(f"New bridge pattern = {new_pattern}")
                self.patterns.append(new_pattern)
            except exc.NoMatchingRightAngleException as e:
                logger.debug(e)

    @staticmethod
    def _get_nearest_cell_index_on_right(pattern, board):
        return BOARD_MAX_INDEX - PatternFinder._get_nearest_cell_index_on_left(pattern, PatternFinder.flip_board_horizontally(board), reversed=True)

    @staticmethod
    def _get_nearest_cell_index_on_left( pattern, board, reversed=False):
        side = "left" if not reversed else "right"
        orientation = pattern.get_orientation()
        x, y = get_coordinates_from_pattern_with_optional_transposition(pattern)
        if reversed:
            y = BOARD_MAX_INDEX - y

        for index in range(2, y + 1):
            real_x, real_y = get_real_coordinates_according_to_board_orientation(orientation, x, y - index)
            if check_if_cell_is_empty(board, x, y - index):
                continue
            try:
                check_if_cell_can_be_part_of_bridge_pattern(board, x, y - index, y)
            except exc.NotPartOfBridgePatternException as e:
                logger.debug(f"Cell with letter \"{board[x][y - index]}\" with coordinates ({real_x}, {real_y}) and "
                             f"{orientation}, can not be a part of bridge pattern, details = {str(e)}")
                raise exc.NoMatchingRightAngleException("There is no accessible right angles on {side}")
            else:
                logger.debug(f"Matching cell on {side} has been found with letter \"{board[x][y - index]}\" on "
                             f"coordinates ({x}, {y - index}), should reverse y = {reversed}")
                return y - index
        raise exc.NoMatchingRightAngleException(f"There is no accessible right angles on {side}, only empty cells")

    def _create_right_angle_patterns_for_orientation(self, board, orientation):
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                try:
                    self._create_right_angle_pattern(board, x, y, orientation)
                except exc.NotRightAnglePatternException as e:
                    logger.debug(e)

    def _create_right_angle_pattern(self, board, x, y, node_orient):
        real_x, real_y = get_real_coordinates_according_to_board_orientation(node_orient, x, y)
        logger.debug(f"Checking if letter \"{board[x][y]}\" on coordinates ({real_x}, {real_y}) can be right angle pattern")
        try:
            check_if_cell_can_be_right_angle_pattern(board, x, y)
        except exc.NotRightAnglePatternException as e:
            logger.debug(f"Cell with coordinates ({real_x}, {real_y}) and {node_orient} {e} ")
        else:
            self._make_right_angle_pattern(node_orient, board, x, y)

    def _make_right_angle_pattern(self, orientation, board, x, y):
        empty_cells_on_left, empty_cells_on_right = get_empty_cells_on_both_sides(x, y, board)
        real_x, real_y = get_real_coordinates_according_to_board_orientation(orientation, x, y)
        pattern = Pattern([board[x][y].lower()], real_x, real_y, empty_cells_on_left, empty_cells_on_right, orientation)
        logger.debug(f"New right angle pattern - {pattern}")
        self.patterns.append(pattern)

