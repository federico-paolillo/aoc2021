# NOTE: We are always ALWAYS implying that any snail number is well formed, we purposefully ignore any possible error

# To find the separator index we search for the first separator that appears after all the 'left' part parenthesis have been closed
# The comma that separates left from right can only appear after the left part is completely formed and 'closed'
import math


def _find_parts_separator_index(snailfish_number_string_without_parens):
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


def _scan_up_right(node, visited):
    if node.is_root():
        return node

    # If we are stepping back in a node that we visited already we go up
    if node in visited:
        return _scan_up_right(node.parent, visited)

    visited.append(node)

    if isinstance(node, RegularNumber):
        return node

    # We try to scan right for a regular number
    return _scan_up_right(node.right, visited)


def _scan_down_left(node):
    if isinstance(node, RegularNumber):
        return node

    # We just drill down to the left
    return _scan_down_left(node.left)


def _scan_up_left(node, visited):
    if node.is_root():
        return node

    # If we are stepping back in a node that we visited already we go up
    if node in visited:
        return _scan_up_left(node.parent, visited)

    visited.append(node)

    if isinstance(node, RegularNumber):
        return node

    # We try to scan left for a regular number
    return _scan_up_left(node.left, visited)


def _scan_down_right(node):
    if isinstance(node, RegularNumber):
        return node

    # We just drill down to the right
    return _scan_down_left(node.right)


def _find_rightmost_regular_number(current_node):
    visited = [current_node]

    regular_number_or_root = _scan_up_right(current_node, visited)

    if isinstance(regular_number_or_root, RegularNumber):
        return regular_number_or_root

    # If we reached root, we scan down and left from root.right
    # But only if root.right was not already visited
    # If root.right was visited there is nothing to do but returning None
    if regular_number_or_root.right in visited:
        return None

    return _scan_down_left(regular_number_or_root.right)


def _find_leftmost_regular_number(current_node):
    visited = [current_node]

    regular_number_or_root = _scan_up_left(current_node, visited)

    if isinstance(regular_number_or_root, RegularNumber):
        return regular_number_or_root

    # If we reached root, we scan down and left from root.right
    # But only if root.right was not already visited
    # If root.right was visited there is nothing to do but returning None
    if regular_number_or_root.left in visited:
        return None

    return _scan_down_right(regular_number_or_root.left)


def _calculate_nesting(node):
    parents_count = 0
    current_parent = node.parent

    while current_parent:
        current_parent = current_parent.parent
        parents_count = parents_count + 1

    return parents_count


def parse_snailfish_number(snailfish_number_string):
    if snailfish_number_string.isnumeric():
        return RegularNumber(int(snailfish_number_string))

    # Remove one char left and right, this should strip the number parenthesis ([])
    snailfish_number_string_without_parens = snailfish_number_string[1:-1]

    # We have to find the index of the separator that divides the parts of the number
    parts_separator_comma_index = _find_parts_separator_index(snailfish_number_string_without_parens)

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

        self.left.split()
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

        self.left.explode()
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
            self.explode()
            self.split()

    def is_root(self):
        return self.parent is None

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
        if self.can_reduce():
            raise ValueError(f'{self} is not reduced')
        if other.can_reduce():
            raise ValueError(f'{other} is not reduced')
        return SnailfishNumber(self, other)

    def __iadd__(self, other):
        if not isinstance(other, SnailfishNumber):
            return NotImplemented

        # TODO: Check for reduce()

        self.left = SnailfishNumber(self.left, self.right)
        self.right = other

        return self
