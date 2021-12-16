import unittest

from aoc2021.day_six import part_one, calculate_population, part_two

_PUZZLE_LANTERN_FISH_TIMERS = [
    5, 1, 4, 1, 5, 1, 1, 5, 4, 4, 4, 4, 5, 1, 2, 2, 1, 3, 4, 1, 1, 5, 1, 5, 2, 2, 2, 2, 1, 4, 2, 4, 3, 3, 3, 3, 1, 1, 1, 4, 3, 4, 3, 1, 2, 1, 5, 1, 1,
    4, 3, 3, 1, 5, 3, 4, 1, 1, 3, 5, 2, 4, 1, 5, 3, 3, 5, 4, 2, 2, 3, 2, 1, 1, 4, 1, 2, 4, 4, 2, 1, 4, 3, 3, 4, 4, 5, 3, 4, 5, 1, 1, 3, 2, 5, 1, 5, 1,
    1, 5, 2, 1, 1, 4, 3, 2, 5, 2, 1, 1, 4, 1, 5, 5, 3, 4, 1, 5, 4, 5, 3, 1, 1, 1, 4, 5, 3, 1, 1, 1, 5, 3, 3, 5, 1, 4, 1, 1, 3, 2, 4, 1, 3, 1, 4, 5, 5,
    1, 4, 4, 4, 2, 2, 5, 5, 5, 5, 5, 1, 2, 3, 1, 1, 2, 2, 2, 2, 4, 4, 1, 5, 4, 5, 2, 1, 2, 5, 4, 4, 3, 2, 1, 5, 1, 4, 5, 1, 4, 3, 4, 1, 3, 1, 5, 5, 3,
    1, 1, 5, 1, 1, 1, 2, 1, 2, 2, 1, 4, 3, 2, 4, 4, 4, 3, 1, 1, 1, 5, 5, 5, 3, 2, 5, 2, 1, 1, 5, 4, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 4, 2, 1, 3, 4, 2, 3,
    1, 2, 2, 3, 3, 4, 3, 5, 4, 1, 3, 1, 1, 1, 2, 5, 2, 4, 5, 2, 3, 3, 2, 1, 2, 1, 1, 2, 5, 3, 1, 5, 2, 2, 5, 1, 3, 3, 2, 5, 1, 3, 1, 1, 3, 1, 1, 2, 2,
    2, 3, 1, 1, 4, 2
]


class DaySixTestCase(unittest.TestCase):
    def test_calculate_population_calculates_example_population_correctly(self):
        lantern_fish_initial_timers = [3, 4, 3, 1, 2]

        population_count_after_18_days = calculate_population(lantern_fish_initial_timers, 18)
        population_count_after_80_days = calculate_population(lantern_fish_initial_timers, 80)
        population_count_after_256_days = calculate_population(lantern_fish_initial_timers, 256)

        self.assertEqual(26, population_count_after_18_days)
        self.assertEqual(5934, population_count_after_80_days)
        self.assertEqual(26984457539, population_count_after_256_days)

    def test_day_six_part_one_solves_puzzle_timers_correctly(self):
        population_count_part_one = part_one(_PUZZLE_LANTERN_FISH_TIMERS)

        self.assertEqual(355386, population_count_part_one)

    def test_day_six_part_two_solves_puzzle_timers_correctly(self):
        population_count_part_two = part_two(_PUZZLE_LANTERN_FISH_TIMERS)

        self.assertEqual(1613415325809, population_count_part_two)
