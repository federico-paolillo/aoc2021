import functools


# Remember: all the points have their coordinates flipped, so expect y,x and not x,y
# This is to remind me that we have a matrix that is an array of array where each array is a row


def _risk_level(height_value):
    return height_value + 1


def _get_adjacent_points(y, x, height_map):
    map_max_y = len(height_map) - 1
    map_max_x = len(height_map[y]) - 1

    # Corners
    if y == 0:
        if x == 0:
            return [
                (y + 1, x),
                (y, x + 1)
            ]
        elif x == map_max_x:
            return [
                (y + 1, x),
                (y, x - 1),
            ]

    if y == map_max_y:
        if x == 0:
            return [
                (y - 1, x),
                (y, x + 1)
            ]
        elif x == map_max_x:
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
    elif y == map_max_y:
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
    elif x == map_max_x:
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


def _low_points(height_map):
    low_points = []

    for y, columns in enumerate(height_map):
        for x, point_height in enumerate(columns):
            adjacent_points = _get_adjacent_points(y, x, height_map)

            adjacent_points_heights = (height_map[y][x] for (y, x) in adjacent_points)

            smallest_adjacent_point_height = min(adjacent_points_heights)

            if point_height < smallest_adjacent_point_height:
                low_points.append((y, x))

    return low_points


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


def _is_inside_basin(y, x, visited_points, height_map):
    if (y, x) in visited_points:
        return False

    if _is_out_of_bounds(y, x, height_map):
        return False

    if height_map[y][x] == 9:
        return False

    return True


# Span Filling flood fill, stolen from: https://en.wikipedia.org/wiki/Flood_fill#Span_Filling
def _scan_for_basin(basin_lowest_point_y, basin_lowest_point_x, height_map):
    basin_points = []

    coordinates_to_visit = [(basin_lowest_point_y, basin_lowest_point_x)]
    visited_coordinates = set()

    while coordinates_to_visit:
        seed_point_y, seed_point_x = coordinates_to_visit.pop()

        span_x_start = seed_point_x
        span_x_end = seed_point_x

        # Scan a line to the left of the seed point, remember what we visit and add it to the basin coordinates
        while _is_inside_basin(seed_point_y, span_x_start - 1, visited_coordinates, height_map):
            span_x_start = span_x_start - 1
            visited_coordinates.add((seed_point_y, span_x_start))
            basin_points.append((seed_point_y, span_x_start))

        # Scan a line to right of the seed point, remember what we visit and add it to the basin coordinates
        while _is_inside_basin(seed_point_y, span_x_end, visited_coordinates, height_map):
            visited_coordinates.add((seed_point_y, span_x_end))
            basin_points.append((seed_point_y, span_x_end))
            span_x_end = span_x_end + 1

        # Once we finish scanning left and right we are left with a start and end of a line

        # Try to scan the same line below the current line
        for line_above_x in range(span_x_start, span_x_end):
            if _is_inside_basin(seed_point_y + 1, line_above_x, visited_coordinates, height_map):
                coordinates_to_visit.append((seed_point_y + 1, line_above_x))

        # Try to scan the same line above the current line
        for line_below_x in range(span_x_start, span_x_end):
            if _is_inside_basin(seed_point_y - 1, line_below_x, visited_coordinates, height_map):
                coordinates_to_visit.append((seed_point_y - 1, line_below_x))

    return basin_points


def part_one(height_map):
    return sum(_risk_level(height_map[y][x]) for (y, x) in _low_points(height_map))


def part_two(height_map):
    low_points = _low_points(height_map)

    basins_by_size = sorted([_scan_for_basin(y, x, height_map) for (y, x) in low_points], key=len)

    largest_three_basins = basins_by_size[-3:]

    return functools.reduce(lambda basins_size_multiplied, basin: basins_size_multiplied * len(basin), largest_three_basins, 1)
