import functools


def _risk_level(height_value):
    return height_value + 1


def _get_adjacent_points_coordinates(y, x, height_map):
    map_max_row_index = len(height_map) - 1
    map_max_col_index = len(height_map[y]) - 1

    # Handle corners first

    if y == 0:
        if x == 0:
            return [
                (y + 1, x),
                (y, x + 1)
            ]
        elif x == map_max_col_index:
            return [
                (y + 1, x),
                (y, x - 1),
            ]

    if y == map_max_row_index:
        if x == 0:
            return [
                (y - 1, x),
                (y, x + 1)
            ]
        elif x == map_max_col_index:
            return [
                (y - 1, x),
                (y, x - 1)
            ]

    # Sides
    if y == 0:
        return [
            (y, x + 1),
            (y, x - 1),
            (y + 1, x)
        ]
    elif y == map_max_row_index:
        return [
            (y, x + 1),
            (y, x - 1),
            (y - 1, x)
        ]

    if x == 0:
        return [
            (y, x + 1),
            (y - 1, x),
            (y + 1, x)
        ]
    elif x == map_max_col_index:
        return [
            (y, x - 1),
            (y - 1, x),
            (y + 1, x)
        ]

    # Point somewhere in the middle
    return [
        (y, x + 1),
        (y, x - 1),
        (y + 1, x),
        (y - 1, x)
    ]


def _low_points_coordinates(height_map):
    low_points_coordinates = []

    for y, columns in enumerate(height_map):
        for x, heightmap_point in enumerate(columns):
            adjacent_points_coordinates = _get_adjacent_points_coordinates(y, x, height_map)
            adjacent_points = (height_map[y][x] for (y, x) in adjacent_points_coordinates)
            smallest_adjacent_point = min(adjacent_points)

            if heightmap_point < smallest_adjacent_point:
                low_point_coordinates = (y, x)
                low_points_coordinates.append(low_point_coordinates)

    return low_points_coordinates


def _is_out_of_bounds(y, x, height_map):
    if x < 0:
        return True

    if y < 0:
        return True

    map_max_row_index = len(height_map)

    if y >= map_max_row_index:
        return True

    map_max_col_index = len(height_map[y])

    if x >= map_max_col_index:
        return True

    return False


def _is_inside_basin(y, x, visited_coordinates, height_map):
    if (y, x) in visited_coordinates:
        return False

    if _is_out_of_bounds(y, x, height_map):
        return False

    if height_map[y][x] == 9:
        return False

    return True


# Span Filling flood fill, stolen from: https://en.wikipedia.org/wiki/Flood_fill#Span_Filling
def _scan_for_basin(basin_lowest_point_y, basin_lowest_point_x, height_map):
    basin_height_values = []

    coordinates_to_visit = [(basin_lowest_point_y, basin_lowest_point_x)]
    visited_coordinates = set()

    while coordinates_to_visit:
        seed_point_y, seed_point_x = coordinates_to_visit.pop()

        span_x_start = seed_point_x
        span_x_end = seed_point_x

        # Move to the left of the seed point, remember what we visit and add it to the basin coordinates
        while _is_inside_basin(seed_point_y, span_x_start - 1, visited_coordinates, height_map):
            span_x_start = span_x_start - 1
            visited_coordinates.add((seed_point_y, span_x_start))
            basin_height_values.append(height_map[seed_point_y][span_x_start])

        # Move to the right of the seed point, remember what we visit and add it to the basin coordinates
        while _is_inside_basin(seed_point_y, span_x_end, visited_coordinates, height_map):
            visited_coordinates.add((seed_point_y, span_x_end))
            basin_height_values.append(height_map[seed_point_y][span_x_end])
            span_x_end = span_x_end + 1

        # Try to scan a line of the same length below the current line
        for line_above_x in range(span_x_start, span_x_end):
            if _is_inside_basin(seed_point_y + 1, line_above_x, visited_coordinates, height_map):
                coordinates_to_visit.append((seed_point_y + 1, line_above_x))

        # Try to scan a line of the same length above the current line
        for line_below_x in range(span_x_start, span_x_end):
            if _is_inside_basin(seed_point_y - 1, line_below_x, visited_coordinates, height_map):
                coordinates_to_visit.append((seed_point_y - 1, line_below_x))

    return basin_height_values


def part_one(height_map):
    return sum(_risk_level(height_map[y][x]) for (y, x) in _low_points_coordinates(height_map))


def part_two(height_map):
    low_points_coordinates = _low_points_coordinates(height_map)
    basins = sorted([_scan_for_basin(y, x, height_map) for (y, x) in low_points_coordinates], key=len)
    largest_three_basins = basins[-3:]

    return functools.reduce(lambda basins_len_multiplied, basin: basins_len_multiplied * len(basin), largest_three_basins, 1)
