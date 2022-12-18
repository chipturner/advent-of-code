from __future__ import annotations

import helpers


def adjacent(c1, c2):
    deltas = sum(abs(p1 - p2) for p1, p2 in zip(c1, c2))
    return deltas == 1


def neighbors(cube):
    for delta_idx in range(3):
        if cube[delta_idx] <= 20:
            new_cube = list(cube)
            new_cube[delta_idx] += 1
            yield tuple(new_cube)
        if cube[delta_idx] >= 1:
            new_cube = list(cube)
            new_cube[delta_idx] -= 1
            yield tuple(new_cube)


def main() -> None:
    lines = helpers.read_input()
    all_cubes = set()
    for coord in lines:
        x, y, z = [int(i) for i in coord.split(",")]
        all_cubes.add((x, y, z))

    outside_coords = set()
    queue = [(1, 1, 1)]
    seen = set()
    while queue:
        coord = queue.pop(0)
        if coord in seen:
            continue
        seen.add(coord)
        outside_coords.add(coord)
        for neighbor in neighbors(coord):
            if neighbor not in all_cubes:
                queue.append(neighbor)
    print(outside_coords)

    for x in range(22):
        for y in range(22):
            for z in range(22):
                maybe_plug = (x, y, z)
                if maybe_plug not in outside_coords:
                    print("plugging", maybe_plug)
                    all_cubes.add(maybe_plug)

    surface_area = 0
    cubes = list(all_cubes)
    for idx1 in range(len(cubes)):
        cube = cubes[idx1]
        surface_area += 6
        for idx2 in range(idx1 + 1, len(cubes)):
            other_cube = cubes[idx2]
            if adjacent(cube, other_cube):
                surface_area -= 2
    print(surface_area)


main()
