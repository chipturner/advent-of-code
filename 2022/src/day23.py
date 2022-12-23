from __future__ import annotations

import helpers
from helpers import Point

import itertools
import collections


check_sets = [
    (Point(0, -1), Point(1, -1), Point(-1, -1)),
    (Point(0, 1), Point(1, 1), Point(-1, 1)),
    (Point(-1, 0), Point(-1, -1), Point(-1, 1)),
    (Point(1, 0), Point(1, -1), Point(1, 1)),
]


def has_neighbor_elf(grid, pt):
    i, j = pt.x, pt.y
    for pos in (
        (i, j + 1),
        (i, j - 1),
        (i + 1, j),
        (i - 1, j),
        (i + 1, j + 1),
        (i - 1, j - 1),
        (i + 1, j - 1),
        (i - 1, j + 1),
    ):
        if Point(*pos) in grid:
            return True
    return False


def main() -> None:
    global check_sets
    lines = helpers.read_input()
    grid = {}
    for row_num, line in enumerate(lines):
        grid.update(
            {
                Point(col_num, row_num): line[col_num]
                for col_num in range(len(line))
                if line[col_num] == "#"
            }
        )

    round = 1
    while round <= 10:
        print()
        print("round", round)
        helpers.print_grid(grid)
        print()
        proposals = collections.defaultdict(list)
        for pt, val in grid.items():
            if not has_neighbor_elf(grid, pt):
                continue

            for check_set in check_sets:
                for check in check_set:
                    if pt + check in grid:
                        break
                else:
                    proposals[pt + check_set[0]].append(pt)
                    break

        removes = set()
        moves = dict()
        for pt, proposers in proposals.items():
            if len(proposers) == 1:
                proposer = proposers[0]
                removes.add(proposer)
                moves[pt] = "#"

        c = grid.copy()
        c.update(moves)

        for remove in removes:
            del c[remove]

        grid = c

        check_sets = check_sets[1:] + [check_sets[0]]
        round += 1

    width = max(pt.x for pt in grid) - min(pt.x for pt in grid)
    height = max(pt.y for pt in grid) - min(pt.y for pt in grid)
    print((1 + height) * (1 + width) - len(grid))


main()
