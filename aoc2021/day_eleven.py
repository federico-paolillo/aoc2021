def _find_adjacent_octopuses(y, x, octopuses_grid):
    map_max_y = len(octopuses_grid) - 1
    map_max_x = len(octopuses_grid[y]) - 1

    # Corners
    if y == 0:
        if x == 0:
            return [
                (y + 1, x),
                (y, x + 1),
                (y + 1, x + 1)
            ]
        elif x == map_max_x:
            return [
                (y + 1, x),
                (y, x - 1),
                (y + 1, x - 1)
            ]

    if y == map_max_y:
        if x == 0:
            return [
                (y - 1, x),
                (y, x + 1),
                (y - 1, x + 1)
            ]
        elif x == map_max_x:
            return [
                (y - 1, x),
                (y, x - 1),
                (y - 1, x - 1)
            ]

    # Sides
    if y == 0:
        return [
            (y, x + 1),
            (y, x - 1),
            (y + 1, x),
            (y + 1, x + 1),
            (y + 1, x - 1)
        ]
    elif y == map_max_y:
        return [
            (y, x + 1),
            (y, x - 1),
            (y - 1, x),
            (y - 1, x + 1),
            (y - 1, x - 1)
        ]

    if x == 0:
        return [
            (y, x + 1),
            (y - 1, x),
            (y + 1, x),
            (y + 1, x + 1),
            (y - 1, x + 1)
        ]
    elif x == map_max_x:
        return [
            (y, x - 1),
            (y - 1, x),
            (y + 1, x),
            (y - 1, x - 1),
            (y + 1, x - 1)
        ]

    # Point somewhere in the middle
    return [
        (y, x + 1),
        (y, x - 1),
        (y + 1, x),
        (y + 1, x - 1),
        (y + 1, x + 1),
        (y - 1, x),
        (y - 1, x - 1),
        (y - 1, x + 1)
    ]


def flash_octopuses(octopuses_grid):
    flashes = 0

    octopuses_to_flash = []
    octopuses_flashed = set()

    # Increase energy levels by one for every octopus and track which one will flash
    for y, columns in enumerate(octopuses_grid):
        for x, octopuses in enumerate(columns):
            octopuses_grid[y][x] = octopuses_grid[y][x] + 1
            if octopuses_grid[y][x] > 9:
                octopuses_to_flash.append((y, x))

    # For every flash-able octopus find any neighbours then increase their energy level
    # Then equeue any neighbour that has an energy level sufficient to flash
    while octopuses_to_flash:
        octopus_to_flash = octopuses_to_flash.pop()

        if octopus_to_flash in octopuses_flashed:
            continue

        y, x = octopus_to_flash

        octopuses_grid[y][x] = 0
        octopuses_flashed.add(octopus_to_flash)

        flashes = flashes + 1

        # Find neighbours of the flashed octopus and then flash them
        adjacent_octopuses = _find_adjacent_octopuses(y, x, octopuses_grid)

        # We take into considerations (and increase the energy level) of the octopuses that are not already enqueued and have not already flashed
        # Already flashed octopuses will not participate in further interactions for this step
        # Octopuses that are already queued do not need to be queued multiple times as we consider every single octopus only once
        for adjacent_octopus in adjacent_octopuses:
            if adjacent_octopus in octopuses_to_flash:
                continue

            if adjacent_octopus in octopuses_flashed:
                continue

            y, x = adjacent_octopus
            octopuses_grid[y][x] = octopuses_grid[y][x] + 1

            if octopuses_grid[y][x] > 9:
                octopuses_to_flash.append(adjacent_octopus)

    return flashes


def part_one(octopuses_grid):
    return sum(flash_octopuses(octopuses_grid) for _ in range(100))


def part_two(octopuses_grid):
    step = 0

    # Them nested all(all()) calls sure are ugly
    while not all(all(octopus == 0 for octopus in row) for row in octopuses_grid):
        flash_octopuses(octopuses_grid)
        step = step + 1

    return step
