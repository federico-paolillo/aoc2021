import math
from typing import Tuple


def _get_bit_at_index(zero_based_bit_index: int, number: int) -> int:
    bit_mask = 2 ** zero_based_bit_index

    if number & bit_mask == bit_mask:
        return 1

    return 0


def _find_most_common_bit(zero_based_bit_index: int, numbers: list[int]) -> int:
    number_of_one_bits_at_index = 0
    number_of_zero_bits_at_index = 0

    for number in numbers:
        number_bit_value_at_index = _get_bit_at_index(zero_based_bit_index, number)
        if number_bit_value_at_index == 0:
            number_of_zero_bits_at_index = number_of_zero_bits_at_index + 1
        else:
            number_of_one_bits_at_index = number_of_one_bits_at_index + 1

    one_bits_are_most_common = number_of_one_bits_at_index > number_of_zero_bits_at_index

    if one_bits_are_most_common:
        return 1

    return 0


def part_one(diagnostic_readings: list[int]) -> Tuple[int, int]:
    largest_diagnostic_reading = max(diagnostic_readings, default=0)

    if largest_diagnostic_reading == 0:
        return 0, 0

    max_number_of_bits = math.trunc(math.log2(largest_diagnostic_reading)) + 1  # Largest number has the longest number of significant bits

    gamma_rate_calculated = 0
    epsilon_rate_calculated = 0

    for bit_index in range(max_number_of_bits):

        most_common_bit = _find_most_common_bit(bit_index, diagnostic_readings)

        bit_mask_for_index = 2 ** bit_index

        # Only 1 bits are meaningful, we turn on the bit at the current bit_index for gamma_rate if 1 bits are the most common
        # On the other end, if 0 bits are most common we turn on the bit at the current bit_index for epsilon_rate
        # Because we have only two possible values, we can assume that if 0 bits are the most common then 1 bits are less common

        if most_common_bit == 1:
            gamma_rate_calculated = gamma_rate_calculated | bit_mask_for_index
        else:
            epsilon_rate_calculated = epsilon_rate_calculated | bit_mask_for_index

    return gamma_rate_calculated, epsilon_rate_calculated
