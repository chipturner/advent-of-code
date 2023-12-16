from __future__ import annotations

import helpers

import itertools
import collections
import re
import numpy as np
from dataclasses import dataclass

Point = helpers.Point


@dataclass(frozen=True)
class Beam:
    pos: Point
    vec: Point

N, S, E, W = Point(0, 1), Point(0, -1), Point(1, 0), Point(-1, 0)

inout = {
    "-": {N: (E, W), S: (E, W)},
    "|": {E: (N, S), W: (N, S)},
    "/": {N: (W,), W: (N,), E: (S,), S: (E,)},
    "\\": {N: (E,), E: (N,), W: (S,), S: (W,)},
}


def main() -> None:
    grid = helpers.read_input_grid()
    print(grid)
    energized_grid = grid.copy()

    cursors = [Beam(Point(-1, 0), E)]

    energized = set()

    seen_beams = set()

    while cursors:
        # helpers.print_numpy_grid(energized_grid)
        # print()
        c, cursors = cursors[0], cursors[1:]
        if c in seen_beams:
            continue
        seen_beams.add(c)
        new_pos = c.pos + c.vec
        if new_pos.y < 0 or new_pos.x < 0 or new_pos.y >= grid.shape[0] or new_pos.x >= grid.shape[1]:
            continue
        energized.add(new_pos)
        energized_grid[new_pos.y, new_pos.x] = '#'
        ch = grid[new_pos.y, new_pos.x]
        splits = inout.get(ch, {})
        new_vecs = splits.get(-c.vec, [])
        if new_vecs:
            for new_vec in new_vecs:
                cursors.append(Beam(new_pos, -new_vec))
        else:
            cursors.append(Beam(new_pos, c.vec))

    print(len(energized))

main()
