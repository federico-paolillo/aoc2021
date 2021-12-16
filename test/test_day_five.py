import unittest

from aoc2021.day_five import Line, part_one, parse_lines_file, part_two


class DayFiveTestCase(unittest.TestCase):
    def test_Line_discrete_points_returns_the_correct_line_points_for_a_diagonal_line(self):
        expected_points = [(2, 6), (3, 5), (4, 4), (5, 3)]
        line = Line(2, 6, 5, 3)

        line_points = line.discrete_points()

        self.assertEqual(expected_points, line_points)
        self.assertTrue(line.is_diagonal())
        self.assertFalse(line.is_horizontal())
        self.assertFalse(line.is_vertical())

    def test_Line_discrete_points_returns_the_correct_line_points_for_a_horizontal_line(self):
        expected_points = [(9, 4), (8, 4), (7, 4), (6, 4), (5, 4), (4, 4), (3, 4)]
        line = Line(9, 4, 3, 4)

        line_points = line.discrete_points()

        self.assertEqual(expected_points, line_points)
        self.assertFalse(line.is_diagonal())
        self.assertTrue(line.is_horizontal())
        self.assertFalse(line.is_vertical())

    def test_Line_discrete_points_returns_the_correct_line_points_for_a_vertical_line(self):
        expected_points = [(6, 6), (6, 7), (6, 8)]
        line = Line(6, 6, 6, 8)

        line_points = line.discrete_points()

        self.assertEqual(expected_points, line_points)
        self.assertFalse(line.is_diagonal())
        self.assertFalse(line.is_horizontal())
        self.assertTrue(line.is_vertical())

    def test_Line_angle_returns_correct_angle_for_45_degrees_line(self):
        line = Line(2, 6, 5, 3)

        self.assertEqual(line.angle(), 45)

    def test_day_five_part_one_solves_small_example_lines_correctly(self):
        lines = [
            Line(0, 9, 5, 9),
            Line(0, 9, 2, 9)
        ]

        number_of_overlaps = part_one(lines)

        self.assertEqual(number_of_overlaps, 3)

    def test_day_five_part_one_solves_example_lines_correctly(self):
        lines = parse_lines_file('inputs/day_five_sample_lines.txt')

        number_of_overlaps = part_one(lines)

        self.assertEqual(number_of_overlaps, 5)

    def test_day_five_part_one_solves_puzzle_lines_correctly(self):
        lines = parse_lines_file('inputs/day_five_puzzle_lines.txt')

        number_of_overlaps = part_one(lines)

        self.assertEqual(number_of_overlaps, 7297)

    def test_day_five_part_two_solves_puzzle_lines_correctly(self):
        lines = parse_lines_file('inputs/day_five_puzzle_lines.txt')

        number_of_overlaps = part_two(lines)

        self.assertEqual(number_of_overlaps, 21038)
