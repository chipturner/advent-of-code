from __future__ import annotations

import helpers

import itertools
import collections
import re
import numpy as np
import sys
from dataclasses import dataclass
from typing import Tuple

def inside(grid, pt):
    return 0 <= pt[0] < grid.shape[0] and 0 <= pt[1] < grid.shape[1]

NORTH, EAST, WEST, SOUTH, NONE = (-1, 0), (0, 1), (1, 0), (0, -1), (0, 0)
NEXT_DIRS = { NORTH: (EAST, WEST), SOUTH: (EAST, WEST), EAST: (NORTH, SOUTH), WEST: (NORTH, SOUTH), NONE: (NORTH, SOUTH, EAST, WEST) }

def visit(grid, loc, last_direction, edges):
    next_dirs = NEXT_DIRS[last_direction]
    for delta in (1, 2, 3):
        for d in next_dirs:
            next_loc = tuple(np.add(loc, numpy.array(d) * delta))
            if not inside(grid, next_loc):
                continue
            
            edges[loc].add(next_loc)
            visit(grid, next_loc, d, edges)


def main() -> None:
    grid = helpers.read_input_digit_grid()
    print(grid)

    todo = [ start ]
    while todo:
        cur = todo.pop(0)
        if cur in nodes:
            continue
        nodes.add(cur)
        for row, col in helpers.neighbors(grid, cur.row, cur.col):
            for delta in (-3, -2, -1, 1, 2, 3):
                if inside(grid, (row, col + delta)):
                    next_node = MovementCell(row, col + delta, LEFTRIGHT)
                if inside(grid, (row + delta, col)):
                    next_node = MovementCell(row + delta, col, UPDOWN)

    best_heats = collections.defaultdict(lambda: sys.maxsize)
    todo = [ (start, 0) ]
    seen = set()
    while todo:
        cur, heat = todo.pop(0)
        for neigh in edges[cur]:
            if grid[neigh.row, neigh.col] + heat >= best_heats[neigh]:
                continue
            best_heats[neigh] = grid[neigh.row, neigh.col] + heat
            todo.append((neigh, grid[neigh.row, neigh.col] + heat))
    print(best_heats)

    best_candidate = None
    for cand in best_heats:
        if (cand.row, cand.col) == (12, 12):
            best_candidate = best_heats[cand]
            print(cand, best_candidate)
    print_grid = np.full(grid.shape, '.')
    print(edges[(11, 12)])
    dfdf()
    while (best_candidate.row, best_candidate.col) != (0, 0):
        print_grid[cur] = '#'
        cur = prev_steps[cur]
    print_grid[0, 0] = '#'
    helpers.print_numpy_grid(grid)
    print()
    helpers.print_numpy_grid(print_grid)
main()
