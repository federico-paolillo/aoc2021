import math
import statistics


# This is intuitively easy, the easiest place to reach for any crab is right in the center so we can use the median to compute that
# The median only works if the data set is sorted

def part_one(crabs):
    crab_median = statistics.median(sorted(crabs))
    fuel_consumptions = (abs(crab_position - crab_median) for crab_position in crabs)
    return sum(fuel_consumptions)


# Crabs on part two move with the triangular numbers formula, and that's easy enough

def _triangular_number(number):
    return int((number * (number + 1)) / 2)


# I've pulled this out of my ass but some guy proved that the optimal position is within 1/2 of the mean
# Because we are using only integers we can check the ceil and the floor of the mean which is equivalent to check 1/2 around the mean
# I have no fucking clue, but the intuition still stands.

def part_two(crabs):
    crab_mean = statistics.mean(crabs)

    lower_bound = math.floor(crab_mean)
    upper_bound = math.ceil(crab_mean)

    fuel_consumption_at_lower_bound = sum(_triangular_number(abs(crab_position - lower_bound)) for crab_position in crabs)
    fuel_consumption_at_upper_bound = sum(_triangular_number(abs(crab_position - upper_bound)) for crab_position in crabs)

    return min(fuel_consumption_at_lower_bound, fuel_consumption_at_upper_bound)
