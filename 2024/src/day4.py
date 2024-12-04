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
            gdict[(row, col)] = grid[row][col]

    found = 0
    for pos, ch in gdict.items():
        if ch == "X":
            for npos in helpers.neighbors8(grid, *pos):
                if gdict[npos] == "M":
                    p1 = helpers.Point(*pos)
                    p2 = helpers.Point(*npos)
                    delta = p2 - p1
                    if (
                        gdict.get((p2 + delta).tuple()) == "A"
                        and gdict.get((p2 + delta + delta).tuple()) == "S"
                    ):
                        found += 1
    print(found)


main()
