import math
from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class _BitDistribution:
    most_common_bit: int
    least_common_bit: int


def _bit_mask(zero_based_bit_index: int) -> int:
    return 2 ** zero_based_bit_index


def _bits_count(number: int) -> int:
    if not number:
        return 1

    return math.trunc(math.log2(number)) + 1


def _get_bit_at_index(zero_based_bit_index: int, number: int) -> int:
    bit_mask = _bit_mask(zero_based_bit_index)

    if number & bit_mask == bit_mask:
        return 1

    return 0


def _get_bit_distribution(zero_based_bit_index: int, numbers: list[int]) -> _BitDistribution:
    number_of_one_bits_at_index = 0
    number_of_zero_bits_at_index = 0

    for number in numbers:
        number_bit_value_at_index = _get_bit_at_index(zero_based_bit_index, number)

        if number_bit_value_at_index == 0:
            number_of_zero_bits_at_index = number_of_zero_bits_at_index + 1
        else:
            number_of_one_bits_at_index = number_of_one_bits_at_index + 1

    one_bits_are_most_common = number_of_one_bits_at_index > number_of_zero_bits_at_index
    zero_bits_are_most_common = number_of_zero_bits_at_index > number_of_one_bits_at_index
    same_amount_of_one_and_zeroes = number_of_one_bits_at_index == number_of_zero_bits_at_index

    most_common_bit = 1 if same_amount_of_one_and_zeroes else 1 if one_bits_are_most_common else 0
    least_common_bit = 0 if same_amount_of_one_and_zeroes else 1 if zero_bits_are_most_common else 0

    return _BitDistribution(most_common_bit, least_common_bit)


def part_one(diagnostic_readings: list[int]) -> Tuple[int, int]:
    largest_diagnostic_reading = max(diagnostic_readings, default=0)

    if not largest_diagnostic_reading:
        return 0, 0

    max_number_of_bits = _bits_count(largest_diagnostic_reading)

    gamma_rate_calculated = 0
    epsilon_rate_calculated = 0

    for bit_index in range(max_number_of_bits):
        bit_distribution = _get_bit_distribution(bit_index, diagnostic_readings)
        bit_mask_for_index = _bit_mask(bit_index)

        # Only 1 bits are meaningful, we turn on the bit at the current bit_index for gamma_rate if 1 bits are the most common
        # On the other end, if 0 bits are most common we turn on the bit at the current bit_index for epsilon_rate
        # Because we have only two possible values, we can assume that if 0 bits are the most common then 1 bits are less common

        if bit_distribution.most_common_bit == 1:
            gamma_rate_calculated = gamma_rate_calculated | bit_mask_for_index
        elif bit_distribution.least_common_bit == 1:
            epsilon_rate_calculated = epsilon_rate_calculated | bit_mask_for_index

    return gamma_rate_calculated, epsilon_rate_calculated


def _find_diagnostic_rating(diagnostic_readings: list[int], distribution_bit_selector) -> int:
    largest_diagnostic_reading = max(diagnostic_readings, default=0)

    if not largest_diagnostic_reading:
        return 0

    max_number_of_bits = _bits_count(largest_diagnostic_reading)

    remaining_readings = list(diagnostic_readings)

    # For this search it is paramount that we start from the most significant bit, hence the reversed() call

    for bit_index in reversed(range(max_number_of_bits)):
        bit_distribution = _get_bit_distribution(bit_index, remaining_readings)
        remaining_readings = [reading for reading in remaining_readings if
                              _get_bit_at_index(bit_index, reading) == distribution_bit_selector(bit_distribution)]

        if len(remaining_readings) == 1:
            return remaining_readings[0]

        if len(remaining_readings) == 0:
            return 0

    return 0


def _find_oxygen_generator_rating(diagnostic_readings: list[int]) -> int:
    return _find_diagnostic_rating(diagnostic_readings, lambda distribution: distribution.most_common_bit)


def _find_co2_scrubber_rating(diagnostic_readings: list[int]) -> int:
    return _find_diagnostic_rating(diagnostic_readings, lambda distribution: distribution.least_common_bit)


def part_two(diagnostic_readings: list[int]) -> Tuple[int, int]:
    oxygen_generator_rating = _find_oxygen_generator_rating(diagnostic_readings)
    co2_scrubber_rating = _find_co2_scrubber_rating(diagnostic_readings)

    return oxygen_generator_rating, co2_scrubber_rating
