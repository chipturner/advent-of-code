from __future__ import annotations
from sys import breakpointhook

import helpers

import itertools
import collections
import re
import copy

directions = '^>v<'
next_directions = dict(itertools.pairwise(directions + '^'))
deltas = [helpers.up, helpers.right, helpers.down, helpers.left]
vel_map = dict(zip(directions, deltas))

def walk_grid(grid, guard_ch, guard_pos):
    path = [(guard_ch, guard_pos)]
    seen = set(path)
    try:
        while True:
            next_pos = guard_pos + vel_map[guard_ch]
            while grid[next_pos] == '#':
                guard_ch = next_directions[guard_ch]
                next_pos = guard_pos + vel_map[guard_ch]
            guard_pos = next_pos
            if (guard_ch, guard_pos) in seen:
                return None
            path.append((guard_ch, guard_pos))
            seen.add((guard_ch, guard_pos))
    except IndexError:
        return path

def main() -> None:
    grid = helpers.Grid.from_stdin()

    guard_ch = '^'
    for (row, col), ch in grid.items():
        if grid[(row, col)] == guard_ch:
            guard_pos = helpers.Coordinate(row, col)
            break

    first_guard_ch, first_guard_pos = guard_ch, guard_pos
    grid[guard_pos] = 'X'
    path = walk_grid(grid, guard_ch, guard_pos)
    seen = set(path)
    print(len(set([d for _, d in seen])))

    loop_makers = set()
    for idx, (guard_ch, guard_pos) in enumerate(path[:-1]):
        next_guard_ch, next_guard_pos = path[idx+1]
        new_grid = copy.deepcopy(grid)
        new_grid[next_guard_pos] = '#'
        new_path = walk_grid(new_grid, first_guard_ch, first_guard_pos)
        if not new_path:
            print('yay', idx, next_guard_pos)
            loop_makers.add(next_guard_pos)
    print('loops', len(loop_makers))

main()
