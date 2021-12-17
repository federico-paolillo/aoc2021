import unittest

from aoc2021.day_eight import parse_scrambled_signals_file, part_one


class DayEightTestCase(unittest.TestCase):
    def test_part_one_solves_example_scrambled_signals_correctly(self):
        signals = parse_scrambled_signals_file('inputs/day_eight_sample_signals.txt')

        number_of_1_4_7_8_digits = part_one(signals)

        self.assertEqual(26, number_of_1_4_7_8_digits)

    def test_part_one_solves_puzzle_scrambled_signals_correctly(self):
        signals = parse_scrambled_signals_file('inputs/day_eight_puzzle_signals.txt')

        number_of_1_4_7_8_digits = part_one(signals)

        self.assertEqual(488, number_of_1_4_7_8_digits)
