_TIMER_VALUES = 9
_SPAWN_INDEX = 8
_AFTER_BIRTH_INDEX = 6
_BIRTHING_INDEX = 0


def _shift_left(list_to_shift: list[int]) -> list[int]:
    return list_to_shift[1:] + [0]


def calculate_population(lantern_fish_population_seed: list[int], number_of_days: int) -> list[int]:
    # Each array index corresponds to the timer with the same value as the index
    # Each value at a given index is the number of fishes with that timer value
    current_population = [0] * _TIMER_VALUES

    for seed_value in lantern_fish_population_seed:
        current_population[seed_value] = current_population[seed_value] + 1

    for day in range(number_of_days):
        next_population = _shift_left(current_population)
        next_population[_AFTER_BIRTH_INDEX] = next_population[_AFTER_BIRTH_INDEX] + current_population[_BIRTHING_INDEX]
        next_population[_SPAWN_INDEX] = current_population[_BIRTHING_INDEX]
        current_population = next_population

    return sum(current_population)


def part_one(lantern_fish_population_seed: list[int]) -> list[int]:
    return calculate_population(lantern_fish_population_seed, 80)


def part_two(lantern_fish_population_seed: list[int]) -> list[int]:
    return calculate_population(lantern_fish_population_seed, 256)
