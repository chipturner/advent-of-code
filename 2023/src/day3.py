from __future__ import annotations

import helpers

import itertools
import collections
import re
import numpy

def num_start(grid, x, y):
    ret = ''
    first = x
    if grid[x, y].isdigit():
        i = x - 1
        while i >= 0 and grid[i, y].isdigit():
            ret += grid[i, y]
            i -= 1
        first = i + 1
        i = x + 1
        ret = ret[::-1] + grid[x, y]
        while i < grid.shape[0] and grid[i, y].isdigit():
            ret += grid[i, y]
            i += 1
    return (first, ret)

def main() -> None:
    lines = helpers.read_input()
    g = numpy.array([list(l) for l in lines]).transpose()
    z = numpy.zeros(g.shape)

    sigils = set()
    seen_starts = set()
    for x in range(g.shape[0]):
        for y in range(g.shape[1]):
            if g[x, y] not in list('.1234567890'):
                for pt in helpers.neighbors8(g, x, y):
                    start_x, num = num_start(g, *pt)
                    if num != '':
                        seen_starts.add((start_x, pt[1], int(num)))

    for start in seen_starts:
        print(start)
    s = sum(v[2] for v in seen_starts)
    print(s)
                

main()
