from __future__ import annotations

import helpers

import itertools
import collections
import re


def main() -> None:
    grid = helpers.read_input_grid()
    print(grid)

    gdict = dict()
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            gdict[helpers.Point(row, col)] = grid[row][col]

    found = 0
    for pos, ch in gdict.items():
        if pos.x == 0 or pos.y == 0 or pos.x == len(grid) - 1 or pos.y == len(grid[0]) - 1:
            continue
        if ch == "A":
            c1, c2, c3, c4 = pos + helpers.Point(-1, -1), pos + helpers.Point(-1, 1), pos + helpers.Point(1, 1), pos + helpers.Point(1, -1)
            p1 = gdict[c1] + gdict[c3]
            p2 = gdict[c2] + gdict[c4]
            print(ch, pos, c1, c3, p1, p2)
            if sorted(p1) == sorted(p2) == list('MS'):
                print(ch, pos, p1, p2)
                found += 1
    print(found)


main()
