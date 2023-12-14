from __future__ import annotations

import helpers

import itertools
import collections
import re


def main() -> None:
    grid = helpers.read_input_digit_grid(str)
    print(grid)
    grid.setflags(write=True)
    helpers.print_numpy_grid(grid)
    print()

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

    helpers.print_numpy_grid(grid)
    t = 0
    for idx, row in enumerate(grid):
        dist = len(grid) - idx
        c = dist * sum(row == 'O')
        print(c)
        t += c
    print(t)


main()
