from dataclasses import field, dataclass

_SCRAMBLED_SIGNAL_FILE_LINE_PATTERN_AND_DIGITS_SEPARATOR = '|'
_SCRAMBLED_SIGNAL_FILE_VALUES_SEPARATOR = " "


@dataclass
class ScrambledSignal:
    patterns: list[str] = field(default_factory=list)
    digits: list[str] = field(default_factory=list)


def _sort_string(string_to_sort):
    return ''.join(sorted(string_to_sort))


def _find_decoding_map(scrambled_signal):
    patterns_left_to_decode = list(scrambled_signal.patterns)

    number_1_pattern = next(pattern for pattern in patterns_left_to_decode if len(pattern) == 2)

    patterns_left_to_decode.remove(number_1_pattern)

    number_4_pattern = next(pattern for pattern in patterns_left_to_decode if len(pattern) == 4)
    number_4_segments = set(number_4_pattern)

    patterns_left_to_decode.remove(number_4_pattern)

    number_7_pattern = next(pattern for pattern in patterns_left_to_decode if len(pattern) == 3)
    number_7_segments = set(number_7_pattern)

    patterns_left_to_decode.remove(number_7_pattern)

    number_8_pattern = next(pattern for pattern in patterns_left_to_decode if len(pattern) == 7)
    number_8_segments = set(number_8_pattern)

    patterns_left_to_decode.remove(number_8_pattern)

    # 3 can only be made with the same segments as 7 plus two extra segments
    number_3_pattern = next(pattern for pattern in patterns_left_to_decode if len(set(pattern) - number_7_segments) == 2)
    number_3_segments = set(number_3_pattern)

    patterns_left_to_decode.remove(number_3_pattern)

    # 9 can only be made if it is using the same segments as 3 and 4
    number_3_and_4_segments = number_3_segments | number_4_segments
    number_9_pattern = next(pattern for pattern in patterns_left_to_decode if set(pattern) == number_3_and_4_segments)
    number_9_segments = set(number_9_pattern)

    patterns_left_to_decode.remove(number_9_pattern)

    # 6 is the only number with 6 segments that does not have one segment that 7 has, so the difference of 7 and 6 has to be 1 set of just one segment
    # The other number with 6 segments is 0, which has all the segments of 7
    number_6_pattern = next(pattern for pattern in patterns_left_to_decode if len(pattern) == 6 and len(number_7_segments - set(pattern)) == 1)

    patterns_left_to_decode.remove(number_6_pattern)

    # 0 is the only number with 6 segments that is not the number 6. At this point it should be the only number left with 6 segments
    number_0_pattern = next(pattern for pattern in patterns_left_to_decode if len(pattern) == 6)

    patterns_left_to_decode.remove(number_0_pattern)

    # 5 is like 9 except for one segment
    number_5_pattern = next(pattern for pattern in patterns_left_to_decode if len(number_9_segments - set(pattern)) == 1)

    patterns_left_to_decode.remove(number_5_pattern)

    # 2 is the only number left
    number_2_pattern = patterns_left_to_decode[0]

    # Segments are sorted to make it possible to match a digit that might have the same segments but scrambled in a different order

    return {
        _sort_string(number_0_pattern): '0',
        _sort_string(number_1_pattern): '1',
        _sort_string(number_2_pattern): '2',
        _sort_string(number_3_pattern): '3',
        _sort_string(number_4_pattern): '4',
        _sort_string(number_5_pattern): '5',
        _sort_string(number_6_pattern): '6',
        _sort_string(number_7_pattern): '7',
        _sort_string(number_8_pattern): '8',
        _sort_string(number_9_pattern): '9'
    }


def decode_scrambled_signal_number(scrambled_signal):
    decoding_map = _find_decoding_map(scrambled_signal)

    decoded_digits = []

    for encoded_digit in scrambled_signal.digits:
        sorted_encoded_digit = _sort_string(encoded_digit)
        if sorted_encoded_digit in decoding_map:
            decoded_digits.append(decoding_map[sorted_encoded_digit])

    decoded_number_string = ''.join(decoded_digits)

    return int(decoded_number_string)


def parse_scrambled_signals_file(file_path: str) -> list[ScrambledSignal]:
    scrambled_signals = []

    with open(file_path, 'r') as scrambled_signals_file:
        for line in scrambled_signals_file:
            raw_patterns_sequences, raw_digits_sequences = line.split(_SCRAMBLED_SIGNAL_FILE_LINE_PATTERN_AND_DIGITS_SEPARATOR)

            raw_patterns = [raw_pattern for raw_pattern in raw_patterns_sequences.split(_SCRAMBLED_SIGNAL_FILE_VALUES_SEPARATOR) if raw_pattern]
            raw_digits = [raw_digit for raw_digit in raw_digits_sequences.split(_SCRAMBLED_SIGNAL_FILE_VALUES_SEPARATOR) if raw_digit]

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


def part_two(scrambled_signals: list[ScrambledSignal]):
    sum_of_all_digits = 0

    for scrambled_signal in scrambled_signals:
        number_decoded = decode_scrambled_signal_number(scrambled_signal)
        sum_of_all_digits = sum_of_all_digits + number_decoded

    return sum_of_all_digits
