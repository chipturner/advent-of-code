from __future__ import annotations

import helpers

import itertools
import collections
import re


def main() -> None:
    grid = helpers.Grid.from_stdin()
    print(grid)

    found = 0
    for (row, col), ch in grid.items():
        if row == 0 or col == 0 or row == grid.nrows - 1 or col == grid.ncols - 1:
            continue
        if ch == "A":
            pos = helpers.Coordinate(row, col)
            up_left, up_right, down_left, down_right = [
                pos + x
                for x in (
                    helpers.up_left,
                    helpers.up_right,
                    helpers.down_left,
                    helpers.down_right,
                )
            ]
            p1 = grid[up_left] + grid[down_right]
            p2 = grid[up_right] + grid[down_left]
            print(ch, up_left, down_right, p1, p2)
            if sorted(p1) == sorted(p2) == list("MS"):
                print(ch, pos, p1, p2)
                found += 1
    print(found)


main()
