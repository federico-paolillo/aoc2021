def part_one(measurements):
    previous_measurement = None
    total_increments = 0

    for measurement in measurements:
        if previous_measurement:
            if measurement > previous_measurement:
                total_increments = total_increments + 1
        previous_measurement = measurement

    return total_increments


def part_two(measurements):
    sliding_windows = (measurements[index:index + 3] for index, _ in enumerate(measurements))
    sliding_windows_totals = (sum(sliding_window) for sliding_window in sliding_windows if len(sliding_window) == 3)

    return part_one(sliding_windows_totals)
