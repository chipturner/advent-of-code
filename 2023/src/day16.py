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

def fire_beam(grid, start):
    cursors = [start]

    energized = set()

    seen_beams = set()

    while cursors:
        c, cursors = cursors[0], cursors[1:]
        if c in seen_beams:
            continue
        seen_beams.add(c)
        new_pos = c.pos + c.vec
        if new_pos.y < 0 or new_pos.x < 0 or new_pos.y >= grid.shape[0] or new_pos.x >= grid.shape[1]:
            continue
        energized.add(new_pos)
        ch = grid[new_pos.y, new_pos.x]
        splits = inout.get(ch, {})
        new_vecs = splits.get(-c.vec, [])
        if new_vecs:
            for new_vec in new_vecs:
                cursors.append(Beam(new_pos, -new_vec))
        else:
            cursors.append(Beam(new_pos, c.vec))

    return len(energized)

def main() -> None:
    grid = helpers.read_input_grid()
    print(grid)

    starts = []
    for start_x in range(grid.shape[1]):
        starts.append(Beam(Point(-1, start_x), E))
        starts.append(Beam(Point(grid.shape[1], start_x), W))
    for start_y in range(grid.shape[0]):
        starts.append(Beam(Point(start_y, -1), N))
        starts.append(Beam(Point(start_y, grid.shape[0]), S))
    for start in starts:
        print('s', start)
        print(fire_beam(grid, start))

main()
