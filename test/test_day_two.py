import unittest

from aoc2021.day_two import part_one


class DayTwoTestCase(unittest.TestCase):
    def test_day_two_part_one_solves_example_commands_correctly(self):
        commands = [
            "forward 5",
            "down 5",
            "forward 8",
            "up 3",
            "down 8",
            "forward 2"
        ]

        hposition, depth = part_one(0, 0, commands)

        self.assertEqual(hposition, 15)
        self.assertEqual(depth, 10)
