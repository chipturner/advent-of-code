from __future__ import annotations

import helpers

import itertools
import collections
import re
import fileinput
import sys
import numpy

def get_row_sym(g):
    for y in range(1, g.shape[0]):
        r1, r2 = y - 1, y
        different = False
        while r1 >= 0 and r2 < g.shape[0]:
            if not numpy.array_equal(g[r1], g[r2]):
                different = True
                break
            r1 -= 1
            r2 += 1
        if not different:
            print('row sym at', y)
            return y
    return 0

def pretty(g):
    return '\n'.join(''.join(c for c in r) for r in g)

def main() -> None:
    chunks = open(sys.argv[1], 'r').read().split('\n\n')

    grids = []
    for chunk in chunks:
        g = numpy.array([list(c) for c in chunk.strip().split('\n')], dtype=numpy.str_)
        grids.append(g)

    val = 0
    for g in grids:
        print('grid')
        print(pretty(g))
        val += 100 * get_row_sym(g)
        g = numpy.transpose(g)
        print()
        print('tgrid')
        print(pretty(g))
        val += get_row_sym(g)
    print(val)



main()
