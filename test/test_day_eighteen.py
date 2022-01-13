import unittest

from aoc2021.day_eighteen import parse_snailfish_number, SnailfishNumber, RegularNumber


class DayEighteenTestCase(unittest.TestCase):
    def test_cannot_create_snailfish_number_without_left(self):
        self.assertRaises(ValueError, lambda: SnailfishNumber(None, 2))

    def test_cannot_create_snailfish_number_without_right(self):
        self.assertRaises(ValueError, lambda: SnailfishNumber(2, None))

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
        self.assertRaises(ValueError, lambda: parse_snailfish_number('[1 x]'))

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
        self.assertRaises(TypeError, lambda: SnailfishNumber(1, 2) + 3)

    def test_addition_does_not_work_if_operand_is_not_snailfish_number__iadd__(self):
        def inplace_addition():
            snailfish_number = SnailfishNumber(1, 2)
            snailfish_number += 3

        self.assertRaises(TypeError, inplace_addition)

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
        self.assertRaises(TypeError, lambda: RegularNumber(1) + 3)

    def test_addition_does_not_work_if_operand_is_not_regular_number__iadd__(self):
        def inplace_addition():
            regular_number = RegularNumber(1)
            regular_number += 3

        self.assertRaises(TypeError, inplace_addition)

    def test_equality_returns_True_for_equal_snailfish_numbers(self):
        snailfish_number_a = SnailfishNumber(1, 2)
        snailfish_number_b = SnailfishNumber(1, 2)

        self.assertTrue(snailfish_number_a == snailfish_number_b)

    def test_equality_returns_False_for_non_equal_snailfish_numbers(self):
        snailfish_number_a = SnailfishNumber(1, 2)
        snailfish_number_b = SnailfishNumber(3, 4)

        self.assertFalse(snailfish_number_a == snailfish_number_b)

    def test_equality_returns_False_when_comparing_snailfish_number_to_something_else(self):
        snailfish_number_a = SnailfishNumber(1, 2)
        something_else = 'blahblah'

        self.assertFalse(snailfish_number_a == something_else)

    def test_equality_returns_True_for_equal_regular_numbers(self):
        regular_number_a = RegularNumber(1)
        regular_number_b = RegularNumber(1)

        self.assertTrue(regular_number_a == regular_number_b)

    def test_equality_returns_False_for_non_equal_regular_numbers(self):
        regular_number_a = RegularNumber(1)
        regular_number_b = RegularNumber(2)

        self.assertFalse(regular_number_a == regular_number_b)

    def test_equality_returns_False_when_comparing_regular_number_to_something_else(self):
        regular_number = RegularNumber(1)
        something_else = 'blahblah'

        self.assertFalse(regular_number == something_else)

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
        snailfish_number_after_first_split = parse_snailfish_number('[[[[0, 7], 4], [[7, 8], [0, 13]]], [1, 1]]')
        snailfish_number_after_second_split = parse_snailfish_number('[[[[0, 7], 4], [[7, 8], [0, [6, 7]]]], [1, 1]]')

        self.assertTrue(snailfish_number.can_split())

        snailfish_number.split()

        self.assertEqual(snailfish_number_after_first_split, snailfish_number)

        snailfish_number.split()

        self.assertEqual(snailfish_number_after_second_split, snailfish_number)

    def test_splitting_does_not_split_root_regular_number(self):
        regular_number = RegularNumber(15)
        regular_number_expected = RegularNumber(15)

        self.assertTrue(regular_number.can_split())

        regular_number.split()

        self.assertEqual(regular_number_expected, regular_number)

    def test_explode_explodes_snailfish_number_correctly(self):
        snailfish_number = parse_snailfish_number('[[[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1]]')
        snailfish_number_after_first_explode = parse_snailfish_number('[[[[0, 7], 4], [7, [[8, 4], 9]]], [1, 1]]')
        snailfish_number_after_second_explode = parse_snailfish_number('[[[[0, 7], 4], [15, [0, 13]]], [1, 1]]')

        self.assertTrue(snailfish_number.can_explode())

        snailfish_number.explode()

        self.assertEqual(snailfish_number_after_first_explode, snailfish_number)

        snailfish_number.explode()

        self.assertEqual(snailfish_number_after_second_explode, snailfish_number)

    def test_explode_has_precedence_over_splitting(self):
        snailfish_number = parse_snailfish_number('[[[[[[1, 2], 10], 1], 1], 1], 1]')
        snailfish_number_expected = parse_snailfish_number('[[[[[[1, 2], 10], 1], 1], 1], 1]')

        self.assertTrue(snailfish_number.can_split())
        self.assertTrue(snailfish_number.can_explode())

        snailfish_number.split()

        self.assertEqual(snailfish_number_expected, snailfish_number)

    def test_reduce_reduces_snailfish_number_correctly(self):
        test_cases = [
            ('[[[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1]]', '[[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]'),
            ('[1, [[[[1, 2], 1], 1], 1]]', '[2, [[[0, 3], 1], 1]]'),
            ('[[1, [1, [1, [1, 2]]]], 1]', '[[1, [1, [2, 0]]], 3]'),
            ('[1, [1, [1, [1, [1, 1]]]]]', '[1, [1, [1, [2, 0]]]]'),
            ('[[1, 1], [[[[1, 1], 1], 1], 1]]', '[[1, 2], [[[0, 2], 1], 1]]'),
            ('[[3, [2, [1, [7 ,3]]]], [6, [5, [4, [3, 2]]]]]', '[[3, [2, [8, 0]]], [9, [5, [7, 0]]]]')
        ]

        for test_case in test_cases:
            with self.subTest('Reduce snailfish number', number=test_case[0]):
                snailfish_number = parse_snailfish_number(test_case[0])
                snailfish_number_after_reduce_expected = parse_snailfish_number(test_case[1])

                snailfish_number.reduce()

                self.assertEqual(snailfish_number_after_reduce_expected, snailfish_number)

    def test_snailfish_number_will_not_replace_something_that_is_not_directly_its_child(self):
        snailfish_number = SnailfishNumber(1, 2)
        other_unrelated_snailfish_number = SnailfishNumber(3, 4)
        snailfish_number_expected = SnailfishNumber(1, 2)

        snailfish_number.replace(other_unrelated_snailfish_number, RegularNumber(1))

        self.assertEqual(snailfish_number_expected, snailfish_number)

    def test_snailfish_number_reduction_steps_apply_to_one_snailfish_number_per_call(self):
        snailfish_number_a = parse_snailfish_number('[[[[4,3],4],4],[7,[[8,4],9]]]')
        snailfish_number_b = parse_snailfish_number('[1, 1]')

        snailfish_number_total = snailfish_number_a + snailfish_number_b

        self.assertEqual(parse_snailfish_number('[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]'), snailfish_number_total)

        snailfish_number_total.explode()

        self.assertEqual(parse_snailfish_number('[[[[0,7],4],[7,[[8,4],9]]],[1,1]]'), snailfish_number_total)

        snailfish_number_total.explode()

        self.assertEqual(parse_snailfish_number('[[[[0,7],4],[15,[0,13]]],[1,1]]'), snailfish_number_total)

        snailfish_number_total.split()

        self.assertEqual(parse_snailfish_number('[[[[0,7],4],[[7,8],[0,13]]],[1,1]]'), snailfish_number_total)

        snailfish_number_total.split()

        self.assertEqual(parse_snailfish_number('[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]'), snailfish_number_total)

        snailfish_number_total.explode()

        self.assertEqual(parse_snailfish_number('[[[[0,7],4],[[7,8],[6,0]]],[8,1]]'), snailfish_number_total)

        self.assertFalse(snailfish_number_total.can_reduce())

    def test_snailfish_number_continuous_sums_are_correct(self):
        snailfish_number_a = parse_snailfish_number('[1, 1]')
        snailfish_number_b = parse_snailfish_number('[2, 2]')
        snailfish_number_c = parse_snailfish_number('[3, 3]')
        snailfish_number_d = parse_snailfish_number('[4, 4]')
        snailfish_number_e = parse_snailfish_number('[5, 5]')

        snailfish_number_expected = parse_snailfish_number('[[[[3,0],[5,3]],[4,4]],[5,5]]')

        snailfish_sum = snailfish_number_a + snailfish_number_b + snailfish_number_c + snailfish_number_d + snailfish_number_e

        snailfish_sum.reduce()

        self.assertEqual(snailfish_number_expected, snailfish_sum)

    def test_snailfish_number_continuous_sums_are_correct_2(self):
        snailfish_number_a = parse_snailfish_number('[1, 1]')
        snailfish_number_b = parse_snailfish_number('[2, 2]')
        snailfish_number_c = parse_snailfish_number('[3, 3]')
        snailfish_number_d = parse_snailfish_number('[4, 4]')
        snailfish_number_e = parse_snailfish_number('[5, 5]')
        snailfish_number_f = parse_snailfish_number('[6, 6]')

        snailfish_number_expected = parse_snailfish_number('[[[[5,0],[7,4]],[5,5]],[6,6]]')

        snailfish_sum = snailfish_number_a + snailfish_number_b + snailfish_number_c + snailfish_number_d + snailfish_number_e + snailfish_number_f

        snailfish_sum.reduce()

        self.assertEqual(snailfish_number_expected, snailfish_sum)
