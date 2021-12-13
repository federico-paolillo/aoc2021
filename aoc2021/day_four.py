from typing import Tuple, Optional

_BINGO_BOARD_LINES_SEPARATOR = ' '


def _index_to_x_y(number_of_columns: int, number_of_rows: int, index: int) -> Tuple[int, int]:
    x = index % number_of_columns
    y = index // number_of_rows

    return x, y


class BingoBoard:
    def __init__(self, number_of_columns: int, number_of_rows: int, numbers: list[int]):
        self._number_of_columns = number_of_columns
        self._number_of_rows = number_of_rows
        self._numbers = numbers
        self._unmarked_numbers = list(numbers)
        self._row_completion_counters = [0] * number_of_rows
        self._column_completion_counters = [0] * number_of_columns

    def mark_number(self, number_to_mark: int):
        if number_to_mark not in self._numbers:
            return

        number_to_mark_index = self._numbers.index(number_to_mark)

        x, y = _index_to_x_y(self._number_of_columns, self._number_of_rows, number_to_mark_index)

        self._column_completion_counters[x] = self._column_completion_counters[x] + 1
        self._row_completion_counters[y] = self._row_completion_counters[y] + 1

        self._unmarked_numbers.remove(number_to_mark)

    def has_won(self) -> bool:
        any_column_complete = any(column_counter for column_counter in self._column_completion_counters if column_counter == self._number_of_columns)
        any_row_complete = any(row_counter for row_counter in self._row_completion_counters if row_counter == self._number_of_rows)

        return any_column_complete or any_row_complete

    def calculate_score(self, last_extracted_number: int) -> int:
        partial_score = 0

        for not_marked_number in self._unmarked_numbers:
            partial_score = partial_score + not_marked_number

        return partial_score * last_extracted_number


def _text_lines_to_bingo_board(number_of_columns: int, number_of_rows: int, text_lines: list[str]) -> BingoBoard:
    numbers = []

    for line in text_lines:
        raw_row_numbers = line.split(_BINGO_BOARD_LINES_SEPARATOR)
        row_numbers = [int(raw_number.strip()) for raw_number in raw_row_numbers if raw_number]
        numbers.extend(row_numbers)

    return BingoBoard(number_of_columns, number_of_rows, numbers)


def parse_bingo_boards_file(number_of_columns: int, number_of_rows: int, file_path: str):
    bingo_boards = []

    with open(file_path, mode='r') as bingo_boards_file:
        bingo_board_text_lines = []

        for bingo_board_line in bingo_boards_file:
            clean_bingo_board_line = bingo_board_line.strip()

            if clean_bingo_board_line:  # Bingo Boards are separated by empty lines
                bingo_board_text_lines.append(clean_bingo_board_line)
            else:
                bingo_board = _text_lines_to_bingo_board(number_of_columns, number_of_rows, bingo_board_text_lines)
                bingo_boards.append(bingo_board)
                bingo_board_text_lines = []

        # Let's check for any leftovers lines
        if bingo_board_text_lines:
            bingo_board = _text_lines_to_bingo_board(number_of_columns, number_of_rows, bingo_board_text_lines)
            bingo_boards.append(bingo_board)

    return bingo_boards


def find_first_winning_board(numbers_to_draw: list[int], bingo_boards: list[BingoBoard]) -> Optional[BingoBoard]:
    for number_drawn in numbers_to_draw:
        for bingo_board in bingo_boards:
            bingo_board.mark_number(number_drawn)
            if bingo_board.has_won():
                return number_drawn, bingo_board

    return None, None
