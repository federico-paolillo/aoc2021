import unittest

from aoc2021.day_eight import parse_scrambled_signals_file, part_one, ScrambledSignal, decode_scrambled_signal_number, part_two


class DayEightTestCase(unittest.TestCase):

    def test_part_one_solves_example_scrambled_signals_correctly(self):
        signals = parse_scrambled_signals_file('inputs/day_eight_sample_signals.txt')

        number_of_1_4_7_8_digits = part_one(signals)

        self.assertEqual(26, number_of_1_4_7_8_digits)

    def test_part_one_solves_puzzle_scrambled_signals_correctly(self):
        signals = parse_scrambled_signals_file('inputs/day_eight_puzzle_signals.txt')

        number_of_1_4_7_8_digits = part_one(signals)

        self.assertEqual(488, number_of_1_4_7_8_digits)

    def test_decode_scrambled_signal_digits_decodes_one_scrambled_signal_correctly(self):
        scrambled_signal = ScrambledSignal(
            [
                'acedgfb',
                'cdfbe',
                'gcdfa',
                'fbcad',
                'dab',
                'cefabd',
                'cdfgeb',
                'eafb',
                'cagedb',
                'ab'
            ],
            [
                'cdfeb',
                'fcadb',
                'cdfeb',
                'cdbaf'
            ]
        )

        decoded_number = decode_scrambled_signal_number(scrambled_signal)

        self.assertEqual(5353, decoded_number)

    def test_decode_scrambled_signal_digits_decodes_another_scrambled_signal_correctly(self):
        scrambled_signal = ScrambledSignal(
            [
                'fbegcd',
                'cbd',
                'adcefb',
                'dageb',
                'afcb',
                'bc',
                'aefdc',
                'ecdab',
                'fgdeca',
                'fcdbega'
            ],
            [
                'efabcd',
                'cedba',
                'gadfec',
                'cb'
            ]
        )

        decoded_number = decode_scrambled_signal_number(scrambled_signal)

        self.assertEqual(9361, decoded_number)

    def test_decode_scrambled_signal_digits_decodes_some_other_scrambled_signal_correctly(self):
        scrambled_signal = ScrambledSignal(
            [
                'bdfegc',
                'cbegaf',
                'gecbf',
                'dfcage',
                'bdacg',
                'ed',
                'bedf',
                'ced',
                'adcbefg',
                'gebcd'
            ],
            [
                'ed',
                'bcgafe',
                'cdgba',
                'cbgef'
            ]
        )

        decoded_number = decode_scrambled_signal_number(scrambled_signal)

        self.assertEqual(1625, decoded_number)

    def test_part_two_solves_sample_scrambled_signals_correctly(self):
        signals = parse_scrambled_signals_file('inputs/day_eight_sample_signals.txt')

        sum_of_all_digits = part_two(signals)

        self.assertEqual(61229, sum_of_all_digits)

    def test_part_two_solves_puzzle_scrambled_signals_correctly(self):
        signals = parse_scrambled_signals_file('inputs/day_eight_puzzle_signals.txt')

        sum_of_all_digits = part_two(signals)

        self.assertEqual(1040429, sum_of_all_digits)
