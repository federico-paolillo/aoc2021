import itertools
import math


class Line:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def discrete_points(self):
        delta_x = self.x2 - self.x1
        delta_y = self.y2 - self.y1

        # If delta is greater than 0 we have to count forward from the starting point, because the end number is greater that then start number
        # In the other case we count backwards because the start number is greater than the end number

        x_step = 1 if delta_x > 0 else -1
        y_step = 1 if delta_y > 0 else -1

        # range() excludes the end number, we have to count up to the end +/- 1 to include the end number

        x_coordinates = range(self.x1, self.x2 + x_step, x_step)
        y_coordinates = range(self.y1, self.y2 + y_step, y_step)

        # We might run out of coordinates on a particular axis before the other axis
        # When we reach the end of an axis we have to stick the points coordinates to the final coordinate for that axis
        # To find which axis will run out first we look at the absolute delta, bigger delta means longer sequences
        # This happens for vertical and horizontal lines and 'skewed' lines
        # A 'skewed' line is a line that cannot be represented with only integer points because some of its points pass through more than one point
        # That means that a 'skewed' lines is not a 45 degrees line.
        # For example (2,6) - (4,3) cannot have all its point represented with a step of 1, 1 points.

        pinned_coordinate = self.x2 if abs(delta_y) > abs(delta_x) else self.y2
        line_points = list(itertools.zip_longest(x_coordinates, y_coordinates, fillvalue=pinned_coordinate))

        return line_points

    def is_horizontal(self):
        return self.y1 == self.y2

    def is_vertical(self):
        return self.x1 == self.x2

    def is_diagonal(self):
        return not self.is_horizontal() and not self.is_vertical()

    def angle(self):
        delta_x = self.x2 - self.x1
        delta_y = self.y2 - self.y1

        # We are on screen coordinates not cartesian coordinates, so the way is positive below 0,0 that's why we invert the arguments to atan2
        # We don't care about positive or negative degrees we just want to know the absolute angle, that's why we abs()

        line_angle = abs(math.degrees(math.atan2(delta_y, delta_x)))

        return line_angle

    def __str__(self):
        return f'({self.x1},{self.y1}) -> ({self.x2},{self.y2})'


def _parse_line(raw_line) -> Line:
    raw_start_part, raw_end_part = raw_line.split('->')

    raw_start_coordinates = [coordinate.strip() for coordinate in raw_start_part.split(',')]
    raw_end_coordinates = [coordinate.strip() for coordinate in raw_end_part.split(',')]

    coordinates = [int(coordinate) for coordinate in raw_start_coordinates + raw_end_coordinates]

    return Line(*coordinates)


def _calculate_points_overlaps(lines, no_diagonals=False):
    points_overlaps_map = {}

    if no_diagonals:
        lines = (line for line in lines if not line.is_diagonal())

    for line in lines:
        for point in line.discrete_points():
            if point in points_overlaps_map:
                points_overlaps_map[point] = points_overlaps_map[point] + 1
            else:
                points_overlaps_map[point] = 1

    return points_overlaps_map


def parse_lines_file(file_path: str):
    lines = []

    with open(file_path, 'r') as lines_file:
        for raw_line in lines_file:
            line = _parse_line(raw_line)
            lines.append(line)

    return lines


def part_one(lines) -> int:
    points_overlaps_map = _calculate_points_overlaps(lines, no_diagonals=True)

    number_of_overlaps = sum(1 for times_seen in points_overlaps_map.values() if times_seen >= 2)

    return number_of_overlaps


def part_two(lines) -> int:
    points_overlaps_map = _calculate_points_overlaps(lines, no_diagonals=False)

    number_of_overlaps = sum(1 for times_seen in points_overlaps_map.values() if times_seen >= 2)

    return number_of_overlaps
