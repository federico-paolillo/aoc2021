# NOTE: We are always ALWAYS implying that any snail number is well formed, we purposefully ignore any possible error

# To find the separator index we search for the first separator that appears after all the 'left' part parenthesis have been closed
# The comma that separates left from right can only appear after the left part is completely formed and 'closed'
import copy
import itertools
import math


def _scan_up_right_for_ancestor(node, visited=None):
    if not node:
        return None

    if not visited:
        # Initial call, we are not interested in anything on the right of the current node only up
        visited = [node, node.right]
    else:
        visited.append(node)

    if any(visited_node is node.right for visited_node in visited):
        return _scan_up_right_for_ancestor(node.parent, visited)

    return node


def _scan_down_left_for_regular_number(node):
    if isinstance(node, RegularNumber):
        return node

    return _scan_down_left_for_regular_number(node.left)


def _scan_up_left_for_ancestor(node, visited=None):
    if not node:
        return None

    if not visited:
        # Initial call, we are not interested in anything on the left of the current node only up
        visited = [node, node.left]
    else:
        visited.append(node)

    if any(visited_node is node.left for visited_node in visited):
        return _scan_up_left_for_ancestor(node.parent, visited)

    return node


def _scan_down_right_for_regular_number(node):
    if isinstance(node, RegularNumber):
        return node

    return _scan_down_right_for_regular_number(node.right)


def _find_rightmost_regular_number(current_node):
    # Given that we are in a tree and there are always leafs that are Regular Numbers
    # If we are on the left of our parent the rightmost number has to be on the left of our parent right
    # If we are on the right we have to find the first ancestor that has our node on the left
    # Once we found that ancestor, the rightmost number will be on the left of the ancestor right

    if current_node is current_node.parent.left:
        return _scan_down_left_for_regular_number(current_node.parent.right)

    ancestor = _scan_up_right_for_ancestor(current_node)

    if ancestor:
        return _scan_down_left_for_regular_number(ancestor.right)

    return None


def _find_leftmost_regular_number(current_node):
    # Given that we are in a tree and there are always leafs that are Regular Numbers
    # If we are on the right of our parent the leftmost number has to be on the right of our parent left
    # If we are on the left we have to find the first ancestor that has our node on the right
    # Once we found that ancestor, the leftmost number will be on the right of the ancestor left

    if current_node is current_node.parent.right:
        return _scan_down_right_for_regular_number(current_node.parent.left)

    ancestor = _scan_up_left_for_ancestor(current_node)

    if ancestor:
        return _scan_down_right_for_regular_number(ancestor.left)

    return None


def _calculate_nesting(node):
    parents_count = 0
    current_parent = node.parent

    while current_parent:
        current_parent = current_parent.parent
        parents_count = parents_count + 1

    return parents_count


def _find_pair_separator_index(snailfish_number_string_without_parens):
    parens_stack = []

    for index, char in enumerate(snailfish_number_string_without_parens):
        if char == '[':
            parens_stack.append(char)
        elif char == ']':
            parens_stack.pop()
        elif char == ',':
            if not parens_stack:
                return index

    return None


def parse_snailfish_number(snailfish_number_string):
    if snailfish_number_string.isnumeric():
        return RegularNumber(int(snailfish_number_string))

    # Remove one char left and right, this should strip the number parenthesis ([])
    snailfish_number_string_without_parens = snailfish_number_string[1:-1]

    # We have to find the index of the separator that divides the parts of the number
    parts_separator_comma_index = _find_pair_separator_index(snailfish_number_string_without_parens)

    if not parts_separator_comma_index:
        raise ValueError(f'Value {snailfish_number_string} is not a valid snailfish number')

    left_part_string = snailfish_number_string_without_parens[:parts_separator_comma_index].strip()
    right_part_string = snailfish_number_string_without_parens[parts_separator_comma_index + 1:].strip()

    left_part = parse_snailfish_number(left_part_string)
    right_part = parse_snailfish_number(right_part_string)

    return SnailfishNumber(left_part, right_part)


class RegularNumber:
    def __init__(self, value):
        self.value = value
        self._parent = None

    @property
    def parent(self):
        return self._parent

    def can_split(self):
        return self.value >= 10

    def can_explode(self):
        return False

    def split(self):
        if not self.can_split():
            return

        if self.is_root():
            return

        floor = math.floor(self.value / 2)
        ceil = math.ceil(self.value / 2)

        self.parent.replace(self, SnailfishNumber(floor, ceil))

    def explode(self):
        pass

    def is_root(self):
        return self.parent is None

    def magnitude(self):
        return self.value

    def __repr__(self):
        return f'RegularNumber({repr(self.value)})'

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        if not isinstance(other, RegularNumber):
            return False

        return self.value == other.value

    def __add__(self, other):
        if not isinstance(other, RegularNumber):
            return NotImplemented

        return RegularNumber(self.value + other.value)

    def __iadd__(self, other):
        if not isinstance(other, RegularNumber):
            return NotImplemented

        self.value = self.value + other.value

        return self


class SnailfishNumber:
    def __init__(self, left, right):
        if left is None:
            raise ValueError('A SnailfishNumber must always have a left')

        if right is None:
            raise ValueError('A SnailfishNumber must always have a right')

        self.left = left
        self.right = right

        self._parent = None

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, value):
        self._left = RegularNumber(value) if isinstance(value, int) else value
        self.left._parent = self

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, value):
        self._right = RegularNumber(value) if isinstance(value, int) else value
        self.right._parent = self

    # self.parent can be manipulated and assigned only through SnailNumber methods to avoid inconsistencies
    # e.g.: How do you know if you are the left or right of your parent
    # e.g.: What if you have a parent but your parent does not have you ?
    # By design a SnailNumber is never nested until...it is nested somewhere
    @property
    def parent(self):
        return self._parent

    def can_reduce(self):
        return self.can_split() or self.can_explode()

    def can_split(self):
        return self.left.can_split() or self.right.can_split()

    def can_explode(self):
        if self.is_explodable():
            return True

        return self.left.can_explode() or self.right.can_explode()

    def is_explodable(self):
        is_nested_in_more_than_four_pairs = _calculate_nesting(self) >= 4

        left_is_regular_number = isinstance(self.left, RegularNumber)
        right_is_regular_number = isinstance(self.right, RegularNumber)

        return is_nested_in_more_than_four_pairs and (right_is_regular_number and left_is_regular_number)

    def split(self):
        if not self.can_split():
            return

        # Explode has precedence on split()
        if self.can_explode():
            return

        if self.left.can_split():
            self.left.split()
        elif self.right.can_split():
            self.right.split()

    def explode(self):
        if not self.can_explode():
            return

        if self.is_explodable():
            rightmost_regular_number = _find_rightmost_regular_number(self)

            if rightmost_regular_number:
                rightmost_regular_number += self.right

            leftmost_regular_number = _find_leftmost_regular_number(self)

            if leftmost_regular_number:
                leftmost_regular_number += self.left

            self.parent.replace(self, RegularNumber(0))
        elif self.left.can_explode():
            self.left.explode()
        elif self.right.can_explode():
            self.right.explode()

    def replace(self, node, replacement_node):
        if node.parent is not self:
            return

        if self.left is node:
            self.left = replacement_node

        if self.right is node:
            self.right = replacement_node

        node._parent = None

    def reduce(self):
        while self.can_reduce():
            if self.can_explode():
                self.explode()
            else:
                self.split()

    def is_root(self):
        return self.parent is None

    def magnitude(self):
        return (3 * self.left.magnitude()) + (2 * self.right.magnitude())

    def __str__(self):
        return f'[{self.left}, {self.right}]'

    def __repr__(self):
        return f'SnailfishNumber({repr(self.left)}, {repr(self.right)})'

    def __eq__(self, other):
        if not isinstance(other, SnailfishNumber):
            return False

        return other.left == self.left and other.right == self.right

    def __add__(self, other):
        if not isinstance(other, SnailfishNumber):
            return NotImplemented

        snailfish_number_sum = SnailfishNumber(self, other)

        return snailfish_number_sum

    def __iadd__(self, other):
        if not isinstance(other, SnailfishNumber):
            return NotImplemented

        self.left = SnailfishNumber(self.left, self.right)
        self.right = other

        return self


def sum_snailfish_numbers(snailfish_numbers):
    total = None

    for snailfish_number in snailfish_numbers:
        if not total:
            total = snailfish_number
        else:
            total = total + snailfish_number
            total.reduce()

    return total


def part_one(raw_snailfish_numbers):
    snailfish_numbers = map(parse_snailfish_number, raw_snailfish_numbers)

    total = sum_snailfish_numbers(snailfish_numbers)

    return total.magnitude()


def part_two(raw_snailfish_numbers):
    snailfish_numbers = map(parse_snailfish_number, raw_snailfish_numbers)

    snailfish_numbers_permutations = itertools.permutations(snailfish_numbers, 2)

    # Snailfish Numbers are mutable, so we need to clone the permutations, otherwise we make a mess
    snailfish_numbers_permutation_copies = (copy.deepcopy(permutation) for permutation in snailfish_numbers_permutations)

    snailfish_numbers_sums = (sum_snailfish_numbers(permutation) for permutation in snailfish_numbers_permutation_copies)

    max_magnitude = max(map(lambda number: number.magnitude(), snailfish_numbers_sums))

    return max_magnitude
