def part_one(input_data):
    if len(input_data) == 0:
        return 0

    previous_input_value = input_data[0]
    total_increments = 0

    for current_input_value in input_data:
        if current_input_value > previous_input_value:
            total_increments = total_increments + 1
        previous_input_value = current_input_value

    return total_increments


def part_two(input_data):
    pass
