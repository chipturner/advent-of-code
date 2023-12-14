from __future__ import annotations

import helpers

import itertools
import collections
import re
import numpy as np
import sys

steps = {
    "|": (np.array((-1, 0)), np.array((1, 0))),
    "-": (np.array((0, 1)), np.array((0, -1))),
    "L": (np.array((-1, 0)), np.array((0, 1))),
    "J": (np.array((-1, 0)), np.array((0, -1))),
    "7": (np.array((1, 0)), np.array((0, -1))),
    "F": (np.array((1, 0)), np.array((0, 1))),
    "S": (),
}

fills = {
    "|": [(1, 0), (1, 1), (1, 2)],
    "-": [(0, 1), (1, 1), (2, 1)],
    "F": [(2, 1), (1, 1), (1, 2)],
    "J": [(0, 1), (1, 1), (1, 0)],
    "7": [(0, 1), (1, 1), (1, 2)],
    "L": [(1, 0), (1, 1), (2, 1)],
    "S": [],
    ".": [],
}


def main() -> None:
    g = helpers.read_input_digit_grid(str)
    for y in range(len(g)):
        for x in range(len(g[0])):
            if g[(y, x)] == "S":
                start = (y, x)
                break

    seen_dist = collections.defaultdict(lambda: sys.maxsize)

    todo = []
    for pt in helpers.neighbors(g, int(start[0]), int(start[1])):
        pt = np.array(pt)
        ch = g[tuple(pt)][0]
        if ch not in steps:
            continue
        for hop in steps[ch]:
            if np.array_equal(pt + hop, start):
                todo.append(tuple(pt))
                seen_dist[tuple(pt)] = 1
    seen_dist[start] = 0

    visited = set()
    while todo:
        n = todo.pop(0)
        if n in visited:
            continue
        ch = g[tuple(n)][0]
        for hop in steps[ch]:
            pt = tuple(n + hop)
            seen_dist[pt] = min(seen_dist[n] + 1, seen_dist[pt])
            todo.append(pt)
        visited.add(n)

    g.setflags(write=True)

    print(max(v for v in seen_dist.values() if v != sys.maxsize))

    big_g = np.full((3 * g.shape[0], 3 * g.shape[1]), ".")

    for y in range(len(g)):
        for x in range(len(g[0])):
            if seen_dist[y, x] == sys.maxsize:
                g[y, x] = "."
            fill_spots = fills[g[(y, x)]]
            for xd, yd in fill_spots:
                big_g[(3 * y + yd, 3 * x + xd)] = "#"
    big_g[3 * start[0] + 1, 3 * start[1] + 1] = "#"

    big_g[3 * start[0] + 2, 3 * start[1] + 1] = big_g[
        3 * start[0] + 3, 3 * start[1] + 1
    ]
    big_g[3 * start[0] + 0, 3 * start[1] + 1] = big_g[
        3 * start[0] - 1, 3 * start[1] + 1
    ]

    big_g[3 * start[0] + 1, 3 * start[1] + 2] = big_g[
        3 * start[0] + 1, 3 * start[1] + 3
    ]
    big_g[3 * start[0] + 1, 3 * start[1] + 0] = big_g[
        3 * start[0] + 1, 3 * start[1] - 1
    ]

    for r in g:
        print("".join(r))
    for r in big_g:
        print("".join(r))

    todo = [(0, 0)]
    while todo:
        cur = todo.pop(0)
        for neigh in helpers.neighbors(big_g, cur[0], cur[1]):
            if big_g[neigh] == ".":
                todo.append(neigh)
                big_g[neigh] = " "
    for r in big_g:
        print("".join(r))

    c = 0
    for y in range(len(g)):
        for x in range(len(g[0])):
            if big_g[3 * y + 1, 3 * x + 1] == "." and g[y, x] == ".":
                c += 1
                g[y, x] = "#"
    print(c)
    for r in g:
        print("".join(r))


main()
