import unittest

from aoc2021.day_four import BingoBoard, parse_bingo_boards_file, find_first_winning_board


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
            bingo_board.mark_number(number_drawn)
            if bingo_board.has_won():
                break
        else:
            self.fail('Bingo board did not win')

    def test_BingoBoard_solves_example_boards_correctly(self):
        numbers_to_draw = [7, 4, 9, 5, 11, 17, 23, 2, 0, 14, 21, 24, 10, 16, 13, 6, 15, 25, 12, 22, 18, 20, 8, 19, 3, 26, 1]

        bingo_boards = parse_bingo_boards_file(5, 5, 'day_four_sample_boards.txt')

        winning_number_drawn, winning_bingo_board = find_first_winning_board(numbers_to_draw, bingo_boards)

        self.assertEqual(winning_bingo_board, bingo_boards[2])
        self.assertEqual(winning_number_drawn, 24)
        self.assertEqual(winning_bingo_board.calculate_score(winning_number_drawn), 4512)

    def test_BingoBoard_solves_puzzle_boards_correctly(self):
        numbers_to_draw = [
            38, 54, 68, 93, 72, 12, 33, 8, 98, 88, 21, 91, 53, 61, 26, 36, 18, 80, 73, 47, 3, 5, 55, 92, 67, 52, 25, 40, 56, 95, 9, 62, 30, 31, 85,
            65, 14, 2, 78, 75, 15, 39, 87, 27, 58, 42, 60, 32, 41, 83, 51, 77, 10, 66, 70, 4, 37, 6, 89, 23, 16, 49, 48, 63, 94, 97, 86, 64, 74, 82,
            7, 0, 11, 71, 44, 43, 50, 69, 45, 81, 20, 28, 46, 79, 90, 34, 35, 96, 99, 59, 1, 76, 22, 24, 17, 57, 13, 19, 84, 29
        ]

        bingo_boards = parse_bingo_boards_file(5, 5, 'day_four_puzzle_boards.txt')

        winning_number_drawn, winning_bingo_board = find_first_winning_board(numbers_to_draw, bingo_boards)

        self.assertEqual(winning_bingo_board.calculate_score(winning_number_drawn), 58838)
