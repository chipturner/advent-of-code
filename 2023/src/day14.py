from __future__ import annotations

import helpers

import itertools
import collections
import re
import numpy

spins = { 'N': 0, 'W': 1, 'S': 2, 'E': 3 }

def roll(grid, d):
    for _ in range(spins[d]):
        grid = numpy.rot90(grid, k=-1)
        
    for idx, row in enumerate(grid):
        if idx == 0:
            continue
        for x_idx in range(len(grid[idx])):
            new_idx = idx
            if grid[idx, x_idx] != 'O':
                continue
            while new_idx > 0:
                if grid[new_idx - 1, x_idx] != '.':
                    break
                grid[new_idx, x_idx] = '.'
                new_idx -= 1
                grid[new_idx, x_idx] = 'O'

    for _ in range(spins[d]):
        grid = numpy.rot90(grid, k=1)

    return grid

def main() -> None:
    grid = helpers.read_input_digit_grid(str)
    grid.setflags(write=True)

    rotations = itertools.cycle('NWSE')
    previously_seen = {}
    n = 0
    while n < 1000000000:
        cur_str = grid.tobytes()
        if cur_str in previously_seen:
            period = n - previously_seen[cur_str]
            print(f'hit at {n} with period {period}')
            if n + period < 1000000000:
                n += period
                continue

        previously_seen[cur_str] = n
        for _ in range(4):
            rot = next(rotations)
            grid = roll(grid, rot)
        print(rot, n)
        n += 1
    helpers.print_numpy_grid(grid)

    t = 0
    for idx, row in enumerate(grid):
        dist = len(grid) - idx
        c = dist * sum(row == 'O')
        print(c)
        t += c
    print(t)


main()
