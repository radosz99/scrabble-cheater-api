from .structures import WordType, Orientation, Letter
from .exceptions import NoMatchingRightAngle
import copy


class Pattern:
    def __init__(self, letters="", x=7, y=7, empty_cells_on_left=0, empty_cells_on_right=0, orientation=None, difference_between_bridge_letters=0):
        self._letters = str(letters)
        self._x = x
        self._y = y
        self._empty_cells_on_left = empty_cells_on_left
        self._empty_cells_on_right = empty_cells_on_right
        self._orientation = orientation
        self._difference_between_bridge_letters = difference_between_bridge_letters
        self._word_type = WordType.BRIDGE if(len(letters) == 2) else WordType.RIGHT_ANGLE
        self._letters_list = self._create_letters_list()

    def __str__(self):
        return f" {self._letters}, x = {self._x}, y = {self._y}, lc = {self._empty_cells_on_left}, rc = {self._empty_cells_on_right}, {self._orientation}, diff = {self._difference_between_bridge_letters}, {self._word_type}"

    def __eq__(self, other):
        coordinates = self._x == other.get_x() and self._y == other.get_y()
        empty_cells = self._empty_cells_on_left == other.get_empty_cells_on_left() and self._empty_cells_on_right == other.get_empty_cells_on_right()
        letters = self._letters = other.get_letters()
        orientation = self._orientation == other.get_orientation()
        return coordinates and empty_cells and letters and orientation

    def __hash__(self):
        return hash((self._x, self._y, self._empty_cells_on_right, self._empty_cells_on_left, self._orientation, self._letters))

    def _create_letters_list(self):
        if self._letters == "":
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

    def get_letters_list(self):
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
        return self._letters

    def get_word_type(self):
        return self._word_type


def _transpose_letters_coordinates(x, y):
    return 14 - y, x


def _untranspose_letters_coordinates(x, y):
    return y, 14 - x


def _transpose_board(board):
    return [([board[y][14 - x] for y in range(15)]) for x in range(15)]


def _check_if_cell_is_empty(board, x, y):
    try:
        return True if board[x][y] == ' ' else False
    except IndexError:
        return True


def _check_if_cell_on_the_top_is_empty(board, x, y):
    return True if _check_if_cell_is_empty(board, x - 1, y) else False


def _check_if_no_tiles_on_top(board, x, y):
    return True if _check_if_cell_on_the_top_is_empty(board, x, y) else False


def _check_if_cell_on_the_bottom_is_empty(board, x, y):
    return True if _check_if_cell_is_empty(board, x + 1, y) else False


def _check_if_no_tiles_on_bottom(board, x, y):
    return True if _check_if_cell_on_the_bottom_is_empty(board, x, y) else False


def _check_if_cell_on_the_left_is_empty(board, x, y):
    return True if _check_if_cell_is_empty(board, x, y - 1) else False


def _check_if_no_tiles_on_left(board, x, y):
    return True if _check_if_cell_on_the_left_is_empty(board, x, y) else False


def _check_if_cell_on_the_right_is_empty(board, x, y):
    return True if _check_if_cell_is_empty(board, x, y + 1) else False


def _check_if_no_tiles_on_right(board, x, y):
    return True if _check_if_cell_on_the_right_is_empty(board, x, y) else False


def _get_coordinates_according_to_board_orientation(orientation, x, y):
    if orientation == Orientation.HORIZONTAL:
        return x, y
    elif orientation == Orientation.VERTICAL:
        return y, 14 - x  # they have been transposed earlier


def _check_if_cell_has_got_no_vertical_neighbors(board, x, y):
    return _check_if_no_tiles_on_top(board, x, y) and _check_if_no_tiles_on_bottom(board, x, y)


def _check_if_cell_has_got_no_horizontal_neighbors(board, x, y):
    return _check_if_no_tiles_on_left(board, x, y) and _check_if_no_tiles_on_right(board, x, y)


def _check_if_right_cell_is_available(board, x, y):
    if y == 14:
        return False
    return _check_if_cell_has_got_no_vertical_neighbors(board, x, y + 1) and _check_if_no_tiles_on_right(board, x, y + 1)


def _check_if_left_cell_is_available(board, x, y):
    if y == 0:
        return False
    return _check_if_cell_has_got_no_vertical_neighbors(board, x, y - 1) and _check_if_no_tiles_on_left(board, x, y - 1)


def _get_empty_cells_on_the_right(x, y, board):
    empty_cells_on_right = 0
    while _check_if_right_cell_is_available(board, x, y + empty_cells_on_right):
        empty_cells_on_right += 1
    return empty_cells_on_right if empty_cells_on_right < 7 else 7


def _get_empty_cells_on_the_left(x, y, board):
    empty_cells_on_left = 0
    while _check_if_left_cell_is_available(board, x, y - empty_cells_on_left):
        empty_cells_on_left += 1
    return empty_cells_on_left if empty_cells_on_left < 7 else 7


def _check_if_cell_can_be_right_angle_pattern(board, x, y):
    return _check_if_cell_has_got_no_horizontal_neighbors(board, x, y) and not _check_if_cell_is_empty(board, x, y)


def _get_nearest_right_angle_on_left(x, y, board):
    cell_index = -1
    for index in range(y - 1):
        if not _check_if_cell_can_be_right_angle_pattern(board, x, index):
            continue
        if not _check_if_cell_has_got_no_vertical_neighbors(board, x, index + 1):
            continue
        cell_index = index
    if 8 >= cell_index > 0:
        return cell_index
    else:
        raise NoMatchingRightAngle("There is no accessible right angles on left")


def _get_coordinates_from_pattern(pattern):
    if pattern.get_orientation() == Orientation.HORIZONTAL:
        return pattern.get_x(), pattern.get_y()
    elif pattern.get_orientation() == Orientation.VERTICAL:
        return _transpose_letters_coordinates(pattern.get_x(), pattern.get_y())


def _get_coordinates_base_on_orientation(orientation, x, y):
    if orientation == Orientation.HORIZONTAL:
        return x, y
    elif orientation == Orientation.VERTICAL:
        return _untranspose_letters_coordinates(x, y)


class PatternFinder:
    def __init__(self, user_letters_quantity):
        self._user_letters_quantity = user_letters_quantity
        self.patterns = []

    def create_patterns(self, board):
        self._create_right_angle_patterns(board)
        self._create_bridge_patterns(board)
        patterns = copy.deepcopy(self.patterns)
        print(f"Number of patterns =  {len(patterns)}")
        patterns = list(set(patterns))
        # for pattern in patterns:
        #     print(pattern)
        print(f"Number of patterns =  {len(patterns)}")
        return patterns

    def _create_right_angle_patterns(self, board):
        self._create_right_angle_patterns_for_orientation(board, Orientation.HORIZONTAL)
        self._create_right_angle_patterns_for_orientation(_transpose_board(board), Orientation.VERTICAL)

    def _create_bridge_patterns(self, board):
        self._create_bridge_patterns_for_orientation(board, Orientation.HORIZONTAL)
        self._create_bridge_patterns_for_orientation(_transpose_board(board), Orientation.VERTICAL)

    def get_amount_of_available_cells_outside_the_bridge(self, difference, x, y, y_coord, board):
        cells_between_the_bridge = difference - 1
        letters_to_put_outside_bridge = self._user_letters_quantity - cells_between_the_bridge
        available_cells_on_left = min(_get_empty_cells_on_the_left(x, y_coord, board), letters_to_put_outside_bridge)
        available_cells_on_right = min(_get_empty_cells_on_the_right(x, y, board), letters_to_put_outside_bridge)
        return available_cells_on_left, available_cells_on_right

    def _create_bridge_patterns_for_orientation(self, board, orientation):
        for pattern in self.patterns:
            if pattern.get_orientation() != orientation:
                continue
            if pattern.get_word_type() is WordType.BRIDGE:
                continue
            x, y = _get_coordinates_from_pattern(pattern)
            try:
                y_nearest = _get_nearest_right_angle_on_left(x, y, board)
            except NoMatchingRightAngle:
                continue

            difference = y - y_nearest
            bridge_letters = board[x][y_nearest] + board[x][y]
            cells_on_left, cells_on_right = self.get_amount_of_available_cells_outside_the_bridge(difference, x, y, y_nearest, board)
            for i in range(cells_on_left + 1):
                max_user_tiles_on_right = self._user_letters_quantity - i - (difference - 1)
                index_right = min(max_user_tiles_on_right, cells_on_right)
                x_coord, y = _get_coordinates_base_on_orientation(orientation, x, y_nearest)
                new_pattern = Pattern(bridge_letters, x_coord, y, i, index_right, orientation, difference)
                self.patterns.append(new_pattern)

    def _create_right_angle_patterns_for_orientation(self, board, orientation):
        for x in range(15):
            for y in range(15):
                self._create_all_letter_right_angle_patterns(board, x, y, orientation)

    def _create_all_letter_right_angle_patterns(self, board, x, y, node_orient):
        if _check_if_cell_can_be_right_angle_pattern(board, x, y):
            self._make_right_angle_patterns(node_orient, board, x, y)

    def _make_right_angle_patterns(self, orientation, board, x, y):
        empty_cells_on_left = _get_empty_cells_on_the_left(x, y, board)
        empty_cells_on_right = _get_empty_cells_on_the_right(x, y, board)
        for i in range(empty_cells_on_left + 1):
            free_cells_on_right = empty_cells_on_right if (i + empty_cells_on_right <= 7) else 7 - i
            real_x, real_y = _get_coordinates_according_to_board_orientation(orientation, x, y)
            pattern = Pattern(board[x][y].lower(), real_x, real_y, i, free_cells_on_right, orientation)
            self.patterns.append(pattern)