# NOTE: We are always ALWAYS implying that any snail number is well formed, we purposefully ignore any possible error

def find_rightmost_node(current_node, visited=None):
    if not current_node:
        return None

    if not visited:
        visited = [current_node]

    if current_node in visited:
        return find_rightmost_node(current_node.parent, visited)

    if isinstance(current_node.right, int):
        return current_node

    visited.append(current_node)

    return find_rightmost_node(current_node.right, visited)


class SnailfishNumber:
    def __init__(self, left, right):
        if left is None:
            raise ValueError('A SnailfishNumber must always have a left')

        self.left = left

        if right is None:
            raise ValueError('A SnailfishNumber must always have a right')

        self.right = right

        self._parent = None

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, value):
        self._left = value
        if isinstance(self.left, SnailfishNumber):
            self.left._parent = self

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, value):
        self._right = value
        if isinstance(self.right, SnailfishNumber):
            self.right._parent = self

    # self.parent can be manipulated and assigned only through SnailNumber methods to avoid inconsistencies
    # e.g.: How do you know if you are the left or right of your parent
    # e.g.: What if you have a parent but your parent does not have you ?
    # By design a SnailNumber is never nested until...it is nested somewhere
    @property
    def parent(self):
        return self._parent

    def is_reduced(self):
        if self.can_split():
            return False

        if self.can_explode():
            return False

        if isinstance(self.left, SnailfishNumber):
            if not self.left.is_reduced():
                return False

        if isinstance(self.right, SnailfishNumber):
            if not self.right.is_reduced():
                return False

        return True

    def can_split(self):
        if isinstance(self.left, int):
            can_split_left = self.left >= 10
        else:
            can_split_left = self.left.can_split()

        if isinstance(self.right, int):
            can_split_right = self.right >= 10
        else:
            can_split_right = self.right.can_split()

        return can_split_left or can_split_right

    def can_explode(self):
        # If we have at least 4 parents it means we are 4 parenthesis deep
        current_parent = self._parent
        parents_count = 0

        while current_parent:
            current_parent = current_parent.parent
            parents_count = parents_count + 1

            if parents_count >= 4:
                return True

        return False

    def __str__(self):
        return f'[{self.left}, {self.right}]'

    def __repr__(self):
        return f'SnailfishNumber({repr(self.left)}, {repr(self.right)})'

    # No __hash__, this class is mutable
    def __eq__(self, other):
        if not isinstance(other, SnailfishNumber):
            return False
        return other.left == self.left and other.right == self.right

    def __add__(self, other):
        if not isinstance(other, SnailfishNumber):
            return NotImplemented
        if not self.is_reduced():
            raise ValueError(f'{self} is not reduced')
        if not other.is_reduced():
            raise ValueError(f'{other} is not reduced')
        return SnailfishNumber(self, other)

    def __radd__(self, other):
        return self + other

    def __iadd__(self, other):
        self.left = SnailfishNumber(self.left, self.right)
        self.right = other
        return self


# To find the separator index we search for the first separator that appears after all the 'left' part parenthesis have been closed
# The comma that separates left from right can only appear after the left part is completely formed and 'closed'
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


def parse_snailfish_number(snailfish_number_string):
    # Remove one char left and right, this should strip the number parenthesis ([])
    snailfish_number_string_without_parens = snailfish_number_string[1:-1]

    # We have to find the index of the separator that divides the parts of the number
    parts_separator_comma_index = _find_parts_separator_index(snailfish_number_string_without_parens)

    if not parts_separator_comma_index:
        raise ValueError(f'Value {snailfish_number_string} is not a valid snailfish number')

    left_part_string = snailfish_number_string_without_parens[:parts_separator_comma_index].strip()
    right_part_string = snailfish_number_string_without_parens[parts_separator_comma_index + 1:].strip()

    if left_part_string.isnumeric():
        left_part = int(left_part_string)
    else:
        left_part = parse_snailfish_number(left_part_string)

    if right_part_string.isnumeric():
        right_part = int(right_part_string)
    else:
        right_part = parse_snailfish_number(right_part_string)

    return SnailfishNumber(left_part, right_part)
