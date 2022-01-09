import unittest

from aoc2021.day_eighteen import parse_snailfish_number, SnailfishNumber, RegularNumber


class DayEighteenTestCase(unittest.TestCase):
    def test_cannot_create_snailfish_number_without_left(self):
        try:
            SnailfishNumber(None, 2)
        except ValueError:
            pass
        else:
            self.fail()

    def test_cannot_create_snailfish_number_without_right(self):
        try:
            SnailfishNumber(2, None)
        except ValueError:
            pass
        else:
            self.fail()

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

    def test_parse_snailfish_number_throws_for_invalid_numbers(self):
        try:
            parse_snailfish_number('[1 2]')
        except ValueError:
            pass
        else:
            self.fail()

    def test_addition_sums_snailfish_numbers_correctly__add__(self):
        snailfish_number_a = SnailfishNumber(1, 2)
        snailfish_number_b = SnailfishNumber(SnailfishNumber(3, 4), 5)

        snailfish_number_sum = snailfish_number_a + snailfish_number_b

        self.assertEqual(SnailfishNumber(SnailfishNumber(1, 2), SnailfishNumber(SnailfishNumber(3, 4), 5)), snailfish_number_sum)

    def test_addition_sums_snailfish_numbers_correctly__iadd__(self):
        snailfish_number_a = SnailfishNumber(1, 2)
        snailfish_number_b = SnailfishNumber(SnailfishNumber(3, 4), 5)

        snailfish_number_a += snailfish_number_b

        self.assertEqual(SnailfishNumber(SnailfishNumber(1, 2), SnailfishNumber(SnailfishNumber(3, 4), 5)), snailfish_number_a)

    def test_addition_does_not_work_if_operand_is_not_snailfish_number__add__(self):
        pass

    def test_addition_does_not_work_if_operand_is_not_snailfish_number__iadd__(self):
        pass

    def test_addition_sums_regular_number_correctly__add__(self):
        regular_number_a = RegularNumber(1)
        regular_number_b = RegularNumber(2)

        regular_number = regular_number_a + regular_number_b

        self.assertEqual(RegularNumber(3), regular_number)

    def test_addition_sums_regular_number_correctly__iadd__(self):
        regular_number_a = RegularNumber(1)
        regular_number_b = RegularNumber(2)

        regular_number_a += regular_number_b

        self.assertEqual(RegularNumber(3), regular_number_a)

    def test_addition_does_not_work_if_operand_is_not_regular_number__add__(self):
        try:
            RegularNumber(1) + 3
        except TypeError:
            pass
        else:
            self.fail()

    def test_addition_does_not_work_if_operand_is_not_regular_number__iadd__(self):
        regular_number = RegularNumber(1)
        try:
            regular_number += 3
        except TypeError:
            pass
        else:
            self.fail()

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

    def test_splitting_does_not_split_root_regular_number(self):
        regular_number = RegularNumber(15)
        regular_number_expected = RegularNumber(15)

        self.assertTrue(regular_number.can_split())

        regular_number.split()

        self.assertEqual(regular_number_expected, regular_number)

    def test_explode_explodes_snailfish_number_correctly(self):
        snailfish_number = parse_snailfish_number('[[[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1]]')
        snailfish_number_after_explode = parse_snailfish_number('[[[[0, 7], 4], [15, [0, 13]]], [1, 1]]')

        self.assertTrue(snailfish_number.can_explode())

        snailfish_number.explode()

        self.assertEqual(snailfish_number_after_explode, snailfish_number)

    def test_explode_has_precedence_over_splitting(self):
        snailfish_number = parse_snailfish_number('[[[[[[1, 2], 10], 1], 1], 1], 1]')
        snailfish_number_expected = parse_snailfish_number('[[[[[[1, 2], 10], 1], 1], 1], 1]')

        self.assertTrue(snailfish_number.can_split())
        self.assertTrue(snailfish_number.can_explode())

        snailfish_number.split()

        self.assertEqual(snailfish_number_expected, snailfish_number)

    def test_reduce_reduces_snailfish_number_correctly(self):
        snailfish_number = parse_snailfish_number('[[[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1]]')
        snailfish_number_after_reduce = parse_snailfish_number('[[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]')

        snailfish_number.reduce()

        self.assertEqual(snailfish_number_after_reduce, snailfish_number)

    def test_snailfish_number_will_not_replace_something_that_is_not_directly_its_child(self):
        snailfish_number = SnailfishNumber(1, 2)
        other_unrelated_snailfish_number = SnailfishNumber(3, 4)
        snailfish_number_expected = SnailfishNumber(1, 2)

        snailfish_number.replace(other_unrelated_snailfish_number, RegularNumber(1))

        self.assertEqual(snailfish_number_expected, snailfish_number)
