from __future__ import annotations

import helpers

import itertools
import collections
import re
import numpy
import sys


def dist(pt1, pt2):
    return abs(pt1[0] - pt2[0]) + abs(pt1[1] - pt2[1]), pt1, pt2


def scale_gaps(gaps, v):
    return (1000000 - 1) * sum([1 if v > g else 0 for g in gaps]) + v


def main() -> None:
    g = helpers.read_input_grid()
    print(g)
    print("\n".join("".join(r) for r in g))
    print()

    row_gaps, col_gaps = [], []

    for idx, r in enumerate(g):
        if all(ch == "." for ch in r):
            row_gaps.append(idx)
    g = g.transpose()

    for idx, r in enumerate(g):
        if all(ch == "." for ch in r):
            col_gaps.append(idx)
    g = g.transpose()

    print(row_gaps, col_gaps)

    galaxies = set()
    for pt in numpy.ndindex(g.shape):
        if g[pt] == "#":
            new_pt = (scale_gaps(row_gaps, pt[0]), scale_gaps(col_gaps, pt[1]))
            galaxies.add(new_pt)

    dists = [dist(pt1, pt2) for pt1, pt2 in itertools.combinations(galaxies, 2)]
    shortest_paths = collections.defaultdict(lambda: sys.maxsize)
    for d, pt1, pt2 in dists:
        shortest_paths[(pt1, pt2)] = min(shortest_paths[(pt1, pt2)], d)
    print(sum(shortest_paths.values()))


main()
