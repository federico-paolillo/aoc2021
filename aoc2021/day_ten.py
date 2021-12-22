import statistics
from dataclasses import dataclass

_PARENS = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>'
}

_MISSING_PARENS_SCORE = {
    '(': 1,
    '[': 2,
    '{': 3,
    '<': 4
}

_CORRUPT_PARENS_SCORE = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}


@dataclass
class CorruptSyntaxResult:
    wrong_token: str = None

    def score(self):
        return _CORRUPT_PARENS_SCORE.get(self.wrong_token)


@dataclass
class IncompleteSyntaxResult:
    missing_tokens: list[str] = None

    def score(self):
        total_score = 0

        for missing_token in reversed(self.missing_tokens):
            total_score = (total_score * 5) + _MISSING_PARENS_SCORE.get(missing_token)

        return total_score


@dataclass
class UnknownSyntaxResult:
    unknown_token: str = None


class CorrectSyntaxResult:
    pass


def _is_paren(char):
    return char in _PARENS.keys() or char in _PARENS.values()


def _is_open_paren(paren):
    return paren in _PARENS.keys()


def _is_closing_paren_of_paren(open_paren, closing_paren):
    return _PARENS[open_paren] == closing_paren


def check_parens(syntax_line):
    parens_stack = []

    for token in syntax_line:

        if not _is_paren(token):
            return UnknownSyntaxResult(token)

        if _is_open_paren(token):
            parens_stack.append(token)
        else:
            last_paren = parens_stack.pop()
            if not _is_closing_paren_of_paren(last_paren, token):
                return CorruptSyntaxResult(token)

    if not parens_stack:
        return CorrectSyntaxResult()

    return IncompleteSyntaxResult(parens_stack)


def part_one(syntax_lines):
    total_score = 0

    for syntax_line in syntax_lines:

        result = check_parens(syntax_line)

        if isinstance(result, CorruptSyntaxResult):
            total_score = total_score + result.score()

    return total_score


def part_two(syntax_lines):
    results = (check_parens(syntax_line) for syntax_line in syntax_lines)
    scores = sorted(result.score() for result in results if isinstance(result, IncompleteSyntaxResult))
    middle_score = scores[len(scores)//2]
    return middle_score
