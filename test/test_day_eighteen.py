import unittest

from aoc2021.day_eighteen import parse_snailfish_number, SnailfishNumber, find_rightmost_node


class DayEighteenTestCase(unittest.TestCase):
    def test_parse_snailfish_number_parses_simple_number(self):
        snailfish_number = parse_snailfish_number('[1, 2]')
        expected_snailfish_number = SnailfishNumber(1, 2)

        self.assertEqual(expected_snailfish_number, snailfish_number)
        self.assertEqual('[1, 2]', str(snailfish_number))
        self.assertEqual('SnailfishNumber(1, 2)', repr(snailfish_number))

    def test_parse_snailfish_number_parses_nested_number(self):
        snailfish_number = parse_snailfish_number('[[1,2], 3]')
        expected_snailfish_number = SnailfishNumber(SnailfishNumber(1, 2), 3)

        self.assertEqual(expected_snailfish_number, snailfish_number)
        self.assertEqual('[[1, 2], 3]', str(snailfish_number))
        self.assertEqual('SnailfishNumber(SnailfishNumber(1, 2), 3)', repr(snailfish_number))

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
        explodable_snailfish_number = SnailfishNumber(9, 8)
        container_snailfish_number = SnailfishNumber(SnailfishNumber(SnailfishNumber(SnailfishNumber(explodable_snailfish_number, 1), 2), 3), 4)

        self.assertFalse(container_snailfish_number.is_reduced())
        self.assertTrue(explodable_snailfish_number.can_explode())

    def test_can_explode_returns_False_for_non_explodable_snailfish_number(self):
        non_explodable_snailfish_number = SnailfishNumber(9, 8)
        container_snailfish_number = SnailfishNumber(SnailfishNumber(SnailfishNumber(non_explodable_snailfish_number, 1), 2), 3)

        self.assertTrue(container_snailfish_number.is_reduced())
        self.assertFalse(non_explodable_snailfish_number.can_explode())

    def test_rightmost_node(self):
        # snailfish_number = '[1, [[[[1, 2], 3], 4], 5]]'
        # expected_number = '[2, [[[0, 5], 4], 5]]'
        snailfish_number_source_node = SnailfishNumber(0, 5)
        expected_rightmost_snailfish_number = SnailfishNumber(snailfish_number_source_node, 4)
        snailfish_number = SnailfishNumber(2, SnailfishNumber(expected_rightmost_snailfish_number, 5))
        rightmost_snailfish_number = find_rightmost_node(snailfish_number_source_node)

        self.assertIs(expected_rightmost_snailfish_number, rightmost_snailfish_number)
