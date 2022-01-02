import io
import os
from dataclasses import dataclass
from enum import Enum
from functools import reduce


class FoldInstructionAxis(Enum):
    X = 1
    Y = 2


@dataclass(frozen=True)
class FoldInstruction:
    axis: FoldInstructionAxis
    fold: int


def fold_coordinate(coordinate, fold):
    # How much 'up' we have to move from the fold to find the new coordinate location ?
    # We have to move up by a delta calculated by the 'distance' of the coordinate to transpose from the fold
    fold_delta = coordinate - fold
    folded_coordinate = fold - fold_delta
    return folded_coordinate


def fold_along(points, fold, get_folding_coordinate, make_new_point):
    fixed_points = (point for point in points if get_folding_coordinate(point) <= fold)
    points_to_fold = (point for point in points if get_folding_coordinate(point) > fold)

    points_left_after_folding = set(fixed_points)

    for point_to_fold in points_to_fold:
        new_coordinate = fold_coordinate(get_folding_coordinate(point_to_fold), fold)
        new_point = make_new_point(point_to_fold, new_coordinate)
        if new_point not in points_left_after_folding:
            points_left_after_folding.add(new_point)

    return list(points_left_after_folding)


def fold_along_x(points, fold):
    return fold_along(points, fold, lambda point: point[0], lambda old_point, new_coordinate: (new_coordinate, old_point[1]))


def fold_along_y(points, fold):
    return fold_along(points, fold, lambda point: point[1], lambda old_point, new_coordinate: (old_point[0], new_coordinate))


def stringify_points(points):
    xs = [point[0] for point in points]
    ys = [point[1] for point in points]

    min_x = min(xs)
    max_x = max(xs)
    max_y = max(ys)
    min_y = min(ys)

    with io.StringIO() as sb:
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                if (x, y) in points:
                    sb.write('#')
                else:
                    sb.write('.')
            # Avoids an useless newline after the final row
            if y < max_y:
                sb.write(os.linesep)
        return sb.getvalue()


def _apply_fold_instruction(fold_instruction, points):
    if fold_instruction.axis == FoldInstructionAxis.X:
        return fold_along_x(points, fold_instruction.fold)
    else:
        return fold_along_y(points, fold_instruction.fold)


def part_one(points):
    return fold_along_x(points, 655)


def part_two(points, instructions):
    return reduce(lambda points_to_fold, instruction: _apply_fold_instruction(instruction, points_to_fold), instructions, points)
