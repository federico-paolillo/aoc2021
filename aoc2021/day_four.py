from typing import Tuple


def _index_to_x_y(horizontal_size: int, vertical_size: int, index: int) -> Tuple[int, int]:
    x = index % horizontal_size
    y = index // vertical_size

    return x, y


class BingoBoard:
    def __init__(self, board_horizontal_size: int, board_vertical_size: int, board_numbers: list[int]):
        self._board_horizontal_size = board_horizontal_size
        self._board_vertical_size = board_vertical_size
        self._board_numbers = board_numbers
        self._not_marked_board_numbers = list(board_numbers)
        self._rows_win_counter = [0] * board_vertical_size
        self._columns_win_counter = [0] * board_horizontal_size

    def mark_drawn_number(self, drawn_number: int):
        if drawn_number not in self._board_numbers:
            return

        extracted_number_index = self._board_numbers.index(drawn_number)

        x, y = _index_to_x_y(self._board_horizontal_size, self._board_vertical_size, extracted_number_index)

        self._rows_win_counter[y] = self._rows_win_counter[y] + 1
        self._columns_win_counter[x] = self._columns_win_counter[x] + 1

        self._not_marked_board_numbers.remove(drawn_number)

    def has_won(self) -> bool:
        any_row_complete = any(counter for counter in self._rows_win_counter if counter == self._board_vertical_size)
        any_column_complete = any(counter for counter in self._columns_win_counter if counter == self._board_horizontal_size)

        return any_column_complete or any_row_complete

    def calculate_score(self, last_extracted_number: int) -> int:
        partial_score = 0

        for not_marked_number in self._not_marked_board_numbers:
            partial_score = partial_score + not_marked_number

        return partial_score * last_extracted_number
