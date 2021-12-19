import statistics


def part_one(crabs):
    crab_median = statistics.median(sorted(crabs))
    fuel_consumptions = (abs(crab_position - crab_median) for crab_position in crabs)
    return sum(fuel_consumptions)
