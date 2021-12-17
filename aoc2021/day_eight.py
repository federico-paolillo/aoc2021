from dataclasses import field, dataclass

_SCRAMBLED_SIGNAL_FILE_LINE_PATTERN_AND_DIGITS_SEPARATOR = '|'
_SCRAMBLED_SIGNAL_FILE_VALUES_SEPARATOR = " "


@dataclass
class ScrambledSignal:
    patterns: list[str] = field(default_factory=list)
    digits: list[str] = field(default_factory=list)


def parse_scrambled_signals_file(file_path: str) -> list[ScrambledSignal]:
    scrambled_signals = []

    with open(file_path, 'r') as scrambled_signals_file:
        for line in scrambled_signals_file:
            raw_patterns_sequences, raw_digits_sequences = line.split(_SCRAMBLED_SIGNAL_FILE_LINE_PATTERN_AND_DIGITS_SEPARATOR)

            raw_patterns = raw_patterns_sequences.split(_SCRAMBLED_SIGNAL_FILE_VALUES_SEPARATOR)
            raw_digits = raw_digits_sequences.split(_SCRAMBLED_SIGNAL_FILE_VALUES_SEPARATOR)

            patterns = [raw_pattern.strip() for raw_pattern in raw_patterns]
            digits = [raw_digit.strip() for raw_digit in raw_digits]

            scrambled_signal = ScrambledSignal(patterns, digits)

            scrambled_signals.append(scrambled_signal)

    return scrambled_signals


def part_one(scrambled_signals: list[ScrambledSignal]):
    number_of_1_4_7_8_digits = 0

    for scrambled_signal in scrambled_signals:
        number_of_1_4_7_8_digits = number_of_1_4_7_8_digits + sum(1 for digit in scrambled_signal.digits if len(digit) in [2, 3, 4, 7])

    return number_of_1_4_7_8_digits
