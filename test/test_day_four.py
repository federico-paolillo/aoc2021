import unittest

from aoc2021.day_four import BingoBoard


class DayFourTestCase(unittest.TestCase):
    def test_BingoBoard_has_won_condition(self):
        numbers_to_draw = [7, 4, 9, 5, 11, 17, 23, 2, 0, 14, 21, 24, 10, 16, 13, 6, 15, 25, 12, 22, 18, 20, 8, 19, 3, 26, 1]

        bingo_board_numbers = [
            14, 21, 17, 24, 4,
            10, 16, 15, 9, 19,
            18, 8, 23, 26, 20,
            22, 11, 13, 6, 5,
            2, 0, 12, 3, 7
        ]

        bingo_board = BingoBoard(5, 5, bingo_board_numbers)

        for number_drawn in numbers_to_draw:
            bingo_board.mark_drawn_number(number_drawn)
            if bingo_board.has_won():
                break
        else:
            self.fail('Bingo board did not win')
