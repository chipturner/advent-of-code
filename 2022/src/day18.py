from __future__ import annotations

import helpers

import itertools
import collections


def adjacent(c1, c2):
    deltas = sum(abs(p1 - p2) for p1, p2 in zip(c1, c2))
    return deltas == 1


def main() -> None:
    lines = helpers.read_input()
    cubes = []
    for coord in lines:
        x, y, z = [int(i) for i in coord.split(",")]
        cubes.append((x, y, z))

    surface_area = 0
    compared = set()
    for idx1 in range(len(cubes)):
        cube = cubes[idx1]
        surface_area += 6
        for idx2 in range(idx1 + 1, len(cubes)):
            other_cube = cubes[idx2]
            if adjacent(cube, other_cube):
                surface_area -= 2
    print(surface_area)


main()
