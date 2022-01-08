import unittest

from aoc2021.day_eighteen import parse_snailfish_number, SnailfishNumber


class DayEighteenTestCase(unittest.TestCase):
    def test_parse_snailfish_number_parses_simple_number(self):
        snailfish_number = parse_snailfish_number('[1, 2]')
        expected_snailfish_number = SnailfishNumber(1, 2)

        self.assertEqual(expected_snailfish_number, snailfish_number)
        self.assertEqual('[1, 2]', str(snailfish_number))
        self.assertEqual('SnailfishNumber(RegularNumber(1), RegularNumber(2))', repr(snailfish_number))

    def test_parse_snailfish_number_parses_nested_number(self):
        snailfish_number = parse_snailfish_number('[[1,2], 3]')
        expected_snailfish_number = SnailfishNumber(SnailfishNumber(1, 2), 3)

        self.assertEqual(expected_snailfish_number, snailfish_number)
        self.assertEqual('[[1, 2], 3]', str(snailfish_number))
        self.assertEqual('SnailfishNumber(SnailfishNumber(RegularNumber(1), RegularNumber(2)), RegularNumber(3))', repr(snailfish_number))

    def test_addition_sums_snailfish_numbers_correctly__add__(self):
        snailfish_number_a = SnailfishNumber(1, 2)
        snailfish_number_b = SnailfishNumber(SnailfishNumber(3, 4), 5)

        snailfish_number_sum = snailfish_number_a + snailfish_number_b

        self.assertEqual(SnailfishNumber(SnailfishNumber(1, 2), SnailfishNumber(SnailfishNumber(3, 4), 5)), snailfish_number_sum)

    def test_addition_sums_snailfish_numbers_correctly__radd__(self):
        snailfish_number_a = SnailfishNumber(SnailfishNumber(3, 4), 5)
        snailfish_number_b = SnailfishNumber(1, 2)

        snailfish_number_sum = snailfish_number_a + snailfish_number_b

        self.assertEqual(SnailfishNumber(SnailfishNumber(SnailfishNumber(3, 4), 5), SnailfishNumber(1, 2)), snailfish_number_sum)

    def test_addition_sums_snailfish_numbers_correctly__iadd__(self):
        snailfish_number_a = SnailfishNumber(1, 2)
        snailfish_number_b = SnailfishNumber(SnailfishNumber(3, 4), 5)

        snailfish_number_a += snailfish_number_b

        self.assertEqual(SnailfishNumber(SnailfishNumber(1, 2), SnailfishNumber(SnailfishNumber(3, 4), 5)), snailfish_number_a)

    def test_can_split_returns_True_for_splittable_snailfish_number(self):
        snailfish_number = SnailfishNumber(10, 2)

        self.assertTrue(snailfish_number.can_split())

    def test_can_split_returns_False_for_unsplittable_snailfish_number(self):
        snailfish_number = SnailfishNumber(1, 2)

        self.assertFalse(snailfish_number.can_split())

    def test_can_explode_returns_True_for_explodable_snailfish_number(self):
        snailfish_number = SnailfishNumber(SnailfishNumber(SnailfishNumber(SnailfishNumber(SnailfishNumber(9, 8), 1), 2), 3), 4)

        self.assertTrue(snailfish_number.can_reduce())
        self.assertTrue(snailfish_number.can_explode())

    def test_can_explode_returns_False_for_non_explodable_snailfish_number(self):
        snailfish_number = SnailfishNumber(SnailfishNumber(SnailfishNumber(1, 2), 3), 4)

        self.assertFalse(snailfish_number.can_reduce())
        self.assertFalse(snailfish_number.can_explode())

    def test_splitting_splits_snailfish_number_correctly(self):
        snailfish_number = parse_snailfish_number('[[[[0, 7], 4], [15, [0, 13]]], [1, 1]]')
        snailfish_number_after_split = parse_snailfish_number('[[[[0, 7], 4], [[7, 8], [0, [6, 7]]]], [1, 1]]')

        self.assertTrue(snailfish_number.can_split())

        snailfish_number.split()

        self.assertEqual(snailfish_number_after_split, snailfish_number)

    def test_explode_explodes_snailfish_number_correctly(self):
        snailfish_number = parse_snailfish_number('[[[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1]]')
        snailfish_number_after_explode = parse_snailfish_number('[[[[0, 7], 4], [15, [0, 13]]], [1, 1]]')

        self.assertTrue(snailfish_number.can_explode())

        snailfish_number.explode()

        self.assertEqual(snailfish_number_after_explode, snailfish_number)

    def test_reduce_reduces_snailfish_number_correctly(self):
        snailfish_number = parse_snailfish_number('[[[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1]]')
        snailfish_number_after_reduce = parse_snailfish_number('[[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]')

        snailfish_number.reduce()

        print(snailfish_number)
        print(snailfish_number_after_reduce)

        self.assertEqual(snailfish_number_after_reduce, snailfish_number)
