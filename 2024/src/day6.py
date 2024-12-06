from __future__ import annotations
from sys import breakpointhook

import helpers

import itertools
import collections
import re

directions = '^>v<'
next_directions = dict(itertools.pairwise(directions + '^'))
deltas = [helpers.up, helpers.right, helpers.down, helpers.left]
vel_map = dict(zip(directions, deltas))

def walk_grid(grid, guard_ch, guard_pos):
    path = [(guard_ch, guard_pos)]
    try:
        while True:
            next_pos = guard_pos + vel_map[guard_ch]
            while grid[next_pos] == '#':
                guard_ch = next_directions[guard_ch]
                next_pos = guard_pos + vel_map[guard_ch]
            guard_pos = next_pos
            path.append((guard_ch, guard_pos))
    except IndexError:
        return path

def main() -> None:
    grid = helpers.Grid.from_stdin()

    guard_ch = '^'
    for (row, col), ch in grid.items():
        if grid[(row, col)] == guard_ch:
            guard_pos = helpers.Coordinate(row, col)
            break

    grid[guard_pos] = 'X'
    path = walk_grid(grid, guard_ch, guard_pos)
    seen = set(path)
    print(len(set([d for _, d in seen])))




main()
