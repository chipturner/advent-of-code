from __future__ import annotations

import helpers

import itertools
import collections
import re
import numpy as np
import sys

Point = helpers.Point

offsets = {'U': Point(0, -1), 'D': Point(0, 1), 'L': Point(-1, 0), 'R': Point(1, 0)}

def main() -> None:
    lines = helpers.read_input()

    pos = Point(500, 500)
    grid = {}
    grid_colors = {}
    min_row, min_col, max_row, max_col = sys.maxsize, sys.maxsize, -1, -1
    for d, dist, color in [ re.match(r'(.) (.+) \(#(.*?)\)', line).groups() for line in lines ]:
        for _ in range(int(dist)):
            min_row = min(min_row, pos.y)
            min_col = min(min_col, pos.x)
            max_row = max(max_row, pos.y)
            max_col = max(max_col, pos.x)
            grid[pos] = '#'
            grid_colors[pos] = color
            delta = offsets[d]
            pos += delta
    helpers.print_grid(grid)
    print()

    start = Point(500, 500)
    while grid.get(start, None) == '#':
        start += Point(1, 1)
    todo = [ start ]
    grid_copy = grid.copy()
    fills = 0
    seen = set()
    while todo:
        cur = todo.pop(0)
        if cur in seen:
            continue
        seen.add(cur)
        for offset in offsets.values():
            new_pt = cur + offset
            if (min_col <= new_pt.x <= max_col) and (min_row <= new_pt.y <= max_row):
                if grid_copy.get(new_pt, None) == None:
                    todo.append(new_pt)
                    grid_copy[new_pt] = 'X'
                    fills += 1
    helpers.print_grid(grid_copy)
    print(fills)
    print(sum(1 for ch in grid_copy.values() if ch in ('X', '#')))

main()
