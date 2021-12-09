from typing import Iterable, Optional

_SLIDING_WINDOW_SIZE = 3


def part_one(measurements: Iterable[int]) -> int:
    previous_measurement: Optional[int] = None
    total_increments = 0

    for measurement in measurements:
        if previous_measurement:
            if measurement > previous_measurement:
                total_increments = total_increments + 1
        previous_measurement = measurement

    return total_increments


def part_two(measurements: list[int]) -> int:
    sliding_windows = (measurements[index:index + _SLIDING_WINDOW_SIZE] for index, _ in enumerate(measurements))
    sliding_windows_totals = (sum(sliding_window) for sliding_window in sliding_windows if
                              len(sliding_window) == _SLIDING_WINDOW_SIZE)

    return part_one(sliding_windows_totals)
