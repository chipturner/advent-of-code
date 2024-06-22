from __future__ import annotations

import helpers

import itertools
import collections
import re
import numpy as np
import sys

Point = helpers.Point

offsets = {'3': Point(0, -1), '1': Point(0, 1), '2': Point(-1, 0), '0': Point(1, 0)}

def condense_range(r):
    assert sorted(r) == r
    ret = []
    for idx, (v0, v1) in enumerate(zip(r[:-1], r[1:])):
        ret.append((idx, idx + 1, v1 - v0))
    return ret

def range_value(r, val):
    s = 0
    for v0, v1, weight in r:
        if s <= val < s + weight:
            return v0
        s += weight
    return r[-1][1] + 1

def point_weight(r1, r2, pt):
    return range_value(r1, pt.y) * range_value(r2, pt.x)

def main() -> None:
    lines = helpers.read_input()

    first_pos = pos = Point(0, 0)
    vertices = set()
    row_pts = []
    col_pts = []
    edges = []
    for d, dist, color in [ re.match(r'(.) (.+) \(#(.*?)\)', line).groups() for line in lines ]:
        d, dist = color[-1], int(color[:-1], 16)
        next_pos = pos + offsets[d] * dist
        vertices.add(pos)
        vertices.add(next_pos)
        edges.append((pos, next_pos))
        pos = next_pos
    # edges.append((pos, first_pos))
    print('v', vertices)
    print(edges)
    row_pts = sorted(set(v.y for v in vertices))
    col_pts = sorted(set(v.x for v in vertices))
    print(row_pts, col_pts)

    row_ranges = condense_range(row_pts)
    col_ranges = condense_range(col_pts)

    new_edges = []
    for e0, e1 in edges:
        new_edges.append((Point(range_value(row_ranges, e0.x), range_value(col_ranges, e0.y)),
                          Point(range_value(row_ranges, e1.x), range_value(col_ranges, e1.y))))

    grid = {}
    for e0, e1 in new_edges:
        if e0.x == e1.x:
            if e0.y > e1.y:
                delta = (0, -1)
            else:
                delta = (0, 1)
        elif e0.y == e1.y:
            if e0.x > e1.x:
                delta = (-1, 0)
            else:
                delta = (1, 0)
        ptdelta = Point(*delta)
        pt = e0
        while pt != e1:
            grid[pt] = '#'
            pt += ptdelta
    helpers.print_grid(grid)

main()
