from __future__ import annotations

import helpers

import itertools
import collections
import re

def check_n(grid, path, seq):
    row, col = path[-1]
    if seq[0] != grid[row][col]:
        return 0
    if len(seq) == 1:
        print(path)
        return 1
    ret = 0
    for n in helpers.neighbors8(grid, row, col):
        ret += check_n(grid, path + [(n[0], n[1])], seq[1:])
    return ret


def main() -> None:
    lines = helpers.read_input_grid()
    print(lines)

    found = 0
    for row in range(len(lines)):
        for col in range(len(lines[0])):
            t = check_n(lines, [(row, col)], 'XMAS')
            if t > 0:
                print('found', row, col, t)
            found += t
    print(found)

main()
