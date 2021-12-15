import itertools
from typing import Tuple, Iterable

_BINGO_BOARD_LINES_SEPARATOR = ' '


def _ichunk(iterable_to_chunk, chunk_size):
    iterator_to_chunk = iter(iterable_to_chunk)

    while True:
        chunk = itertools.islice(iterator_to_chunk, chunk_size)

        try:
            first_element = next(chunk)
        except StopIteration:
            break

        yield itertools.chain([first_element], chunk)


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
        self._rows_completion = [0] * number_of_rows
        self._columns_completion = [0] * number_of_columns

    def mark_number(self, number_to_mark: int):
        if number_to_mark not in self._numbers:
            return

        number_to_mark_index = self._numbers.index(number_to_mark)

        column, row = _index_to_x_y(self._number_of_columns, self._number_of_rows, number_to_mark_index)

        self._columns_completion[column] = self._columns_completion[column] + 1
        self._rows_completion[row] = self._rows_completion[row] + 1

        self._unmarked_numbers.remove(number_to_mark)

    def has_won(self) -> bool:
        any_column_complete = any(column_counter for column_counter in self._columns_completion if column_counter == self._number_of_columns)
        any_row_complete = any(row_counter for row_counter in self._rows_completion if row_counter == self._number_of_rows)

        return any_column_complete or any_row_complete

    def calculate_score(self, last_extracted_number: int) -> int:
        partial_score = 0

        for unmarked_number in self._unmarked_numbers:
            partial_score = partial_score + unmarked_number

        return partial_score * last_extracted_number


def _parse_bingo_boards_lines_chunk(number_of_columns: int, number_of_rows: int, bingo_board_lines_chunk: Iterable[str]) -> BingoBoard:
    numbers = []

    for bingo_board_line in bingo_board_lines_chunk:
        raw_row_numbers = (raw_row_number.strip() for raw_row_number in bingo_board_line.split(_BINGO_BOARD_LINES_SEPARATOR))
        row_numbers = [int(raw_row_number) for raw_row_number in raw_row_numbers if raw_row_number]
        numbers.extend(row_numbers)

    return BingoBoard(number_of_columns, number_of_rows, numbers)


def parse_bingo_boards_file(number_of_columns: int, number_of_rows: int, file_path: str) -> list[BingoBoard]:
    bingo_boards = []

    with open(file_path, mode='r') as bingo_boards_file:
        bingo_boards_file_stripped_lines = (line.strip() for line in bingo_boards_file)
        bingo_boards_file_lines_with_content = (line for line in bingo_boards_file_stripped_lines if line)
        bingo_boards_file_line_chunks = _ichunk(bingo_boards_file_lines_with_content, number_of_rows)

        # Each chunk represents a Bingo Board and is made of number_of_rows text lines
        for bingo_board_lines_chunk in bingo_boards_file_line_chunks:
            if not bingo_board_lines_chunk:  # We ran out of chunks with content, so we assume we are at end of file
                break

            bingo_board = _parse_bingo_boards_lines_chunk(number_of_columns, number_of_rows, bingo_board_lines_chunk)
            bingo_boards.append(bingo_board)

    return bingo_boards


def part_one(numbers_to_draw: list[int], bingo_boards: list[BingoBoard]) -> int:
    for number_drawn in numbers_to_draw:
        for bingo_board in bingo_boards:
            bingo_board.mark_number(number_drawn)
            if bingo_board.has_won():
                return bingo_board.calculate_score(number_drawn)

    return 0


def part_two(numbers_to_draw: list[int], bingo_boards: list[BingoBoard]) -> int:
    bingo_boards_that_won = []

    for number_drawn in numbers_to_draw:
        for bingo_board in bingo_boards:
            if bingo_board in bingo_boards_that_won:
                continue
            bingo_board.mark_number(number_drawn)
            if bingo_board.has_won():
                bingo_boards_that_won.append(bingo_board)
                if len(bingo_boards_that_won) == len(bingo_boards):
                    return bingo_board.calculate_score(number_drawn)

    return 0
