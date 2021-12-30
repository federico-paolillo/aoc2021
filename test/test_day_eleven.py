import unittest

from aoc2021.day_eleven import part_one, flash_octopuses, part_two


class DayElevenTestCase(unittest.TestCase):
    def test_part_one_solves_simple_octopuses_grid_correctly(self):
        octopuses_grid = [
            [1, 1, 1, 1, 1],
            [1, 9, 9, 9, 1],
            [1, 9, 1, 9, 1],
            [1, 9, 9, 9, 1],
            [1, 1, 1, 1, 1]
        ]

        flash_octopuses(octopuses_grid)

        expected_octopuses_grid_after_step_1 = [
            [3, 4, 5, 4, 3],
            [4, 0, 0, 0, 4],
            [5, 0, 0, 0, 5],
            [4, 0, 0, 0, 4],
            [3, 4, 5, 4, 3]
        ]

        self.assertEqual(expected_octopuses_grid_after_step_1, octopuses_grid)

        flash_octopuses(octopuses_grid)

        expected_octopuses_grid_after_step_2 = [
            [4, 5, 6, 5, 4],
            [5, 1, 1, 1, 5],
            [6, 1, 1, 1, 6],
            [5, 1, 1, 1, 5],
            [4, 5, 6, 5, 4]
        ]

        self.assertEqual(expected_octopuses_grid_after_step_2, octopuses_grid)

    def test_part_one_solves_example_octopuses_grid_correctly(self):
        octopuses_grid = [
            [5, 4, 8, 3, 1, 4, 3, 2, 2, 3],
            [2, 7, 4, 5, 8, 5, 4, 7, 1, 1],
            [5, 2, 6, 4, 5, 5, 6, 1, 7, 3],
            [6, 1, 4, 1, 3, 3, 6, 1, 4, 6],
            [6, 3, 5, 7, 3, 8, 5, 4, 7, 8],
            [4, 1, 6, 7, 5, 2, 4, 6, 4, 5],
            [2, 1, 7, 6, 8, 4, 1, 7, 2, 1],
            [6, 8, 8, 2, 8, 8, 1, 1, 3, 4],
            [4, 8, 4, 6, 8, 4, 8, 5, 5, 4],
            [5, 2, 8, 3, 7, 5, 1, 5, 2, 6],
        ]

        total_flashes = part_one(octopuses_grid)

        self.assertEqual(1656, total_flashes)

    def test_part_one_solves_puzzle_octopuses_grid_correctly(self):
        # Puzzle data is here because flash_octopuses changes data in place
        puzzle_octopuses = [
            [4, 5, 7, 5, 3, 5, 5, 6, 2, 3],
            [3, 3, 2, 5, 5, 7, 8, 4, 2, 6],
            [7, 8, 8, 5, 1, 6, 5, 5, 7, 6],
            [4, 8, 7, 1, 4, 5, 5, 6, 5, 8],
            [3, 7, 2, 2, 5, 4, 5, 3, 1, 2],
            [8, 3, 6, 2, 6, 6, 3, 8, 3, 2],
            [5, 5, 6, 2, 7, 4, 3, 3, 2, 4],
            [4, 1, 6, 5, 7, 7, 6, 4, 1, 2],
            [1, 8, 1, 7, 8, 1, 3, 6, 7, 5],
            [4, 2, 5, 5, 5, 2, 4, 6, 3, 2]
        ]

        total_flashes = part_one(puzzle_octopuses)

        self.assertEqual(1642, total_flashes)

    def test_part_two_solves_puzzle_octopuses_grid_correctly(self):
        # Puzzle data is here because flash_octopuses changes data in place
        puzzle_octopuses = [
            [4, 5, 7, 5, 3, 5, 5, 6, 2, 3],
            [3, 3, 2, 5, 5, 7, 8, 4, 2, 6],
            [7, 8, 8, 5, 1, 6, 5, 5, 7, 6],
            [4, 8, 7, 1, 4, 5, 5, 6, 5, 8],
            [3, 7, 2, 2, 5, 4, 5, 3, 1, 2],
            [8, 3, 6, 2, 6, 6, 3, 8, 3, 2],
            [5, 5, 6, 2, 7, 4, 3, 3, 2, 4],
            [4, 1, 6, 5, 7, 7, 6, 4, 1, 2],
            [1, 8, 1, 7, 8, 1, 3, 6, 7, 5],
            [4, 2, 5, 5, 5, 2, 4, 6, 3, 2]
        ]

        total_flashes = part_two(puzzle_octopuses)

        self.assertEqual(320, total_flashes)
