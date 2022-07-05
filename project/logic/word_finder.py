from .structures import Orientation
from .pattern_finder import check_if_cell_has_got_no_vertical_neighbors, check_if_cell_has_got_no_horizontal_neighbors
from .exceptions import IncorrectMove


def get_updated_board_after_move(board, move):
    board = update_board(board, move)
    for letter in [letter for letter in move.get_letters_list() if letter.is_user_letter()]:
        if move.get_orientation() == Orientation.VERTICAL:
            if not check_if_cell_has_got_no_horizontal_neighbors(board, letter.get_x(), letter.get_y()):
                raise IncorrectMove(f"ERROR - {move}, {move.get_pattern()}")
        elif move.get_orientation() == Orientation.HORIZONTAL:
            if not check_if_cell_has_got_no_vertical_neighbors(board, letter.get_x(), letter.get_y()):
                raise IncorrectMove(f"ERROR - {move}, {move.get_pattern()}")
    return board


def update_board(board, move):
    for letter in move.get_letters_list():
        board[letter.get_x()][letter.get_y()] = letter.get_char()
    return board
