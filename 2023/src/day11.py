from __future__ import annotations

import helpers

import itertools
import collections
import re
import numpy
import sys

def dist(pt1, pt2):
    return abs(pt1[0] - pt2[0]) + abs(pt1[1] - pt2[1]), pt1, pt2

def main() -> None:
    g = helpers.read_input_digit_grid(str)
    print(g)
    print('\n'.join(''.join(r) for r in g))
    print()

    new = []
    for r in g:
        if all(ch == '.' for ch in r):
            new.append(['.'] * len(r))
        new.append(r)
    g = numpy.array(new)
    g = g.transpose()

    new = []
    for r in g:
        if all(ch == '.' for ch in r):
            new.append(['.'] * len(r))
        new.append(r)
    g = numpy.array(new)
    g = g.transpose()

    print('\n'.join(''.join(r) for r in g))

    galaxies = set()
    for pt in numpy.ndindex(g.shape):
        if g[pt] == '#':
            galaxies.add(pt)

    dists = [ dist(pt1, pt2) for pt1, pt2 in  itertools.combinations(galaxies, 2) ]
    shortest_paths = collections.defaultdict(lambda: sys.maxsize)
    for d, pt1, pt2 in dists:
        shortest_paths[(pt1, pt2)] = min(shortest_paths[(pt1, pt2)], d)
    print(shortest_paths)
    print(sum(shortest_paths.values()))

main()
