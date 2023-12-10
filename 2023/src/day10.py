from __future__ import annotations

import helpers

import itertools
import collections
import re
import numpy as np
import sys

steps = {
    '|': (np.array((-1,0)), np.array((1, 0))),
    '-': (np.array((0, 1)), np.array((0, -1))),
    'L': (np.array((-1,0)), np.array((0, 1))),
    'J': (np.array((-1,0)), np.array((0, -1))),
    '7': (np.array((1,0)), np.array((0, -1))),
    'F': (np.array((1,0)), np.array((0, 1))),
    'S': (),
}

def main() -> None:
    g = helpers.read_input_digit_grid(str)
    for y in range(len(g)):
        for x in range(len(g[0])):
            if g[(y, x)] == 'S':
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

    print(max(v for v in seen_dist.values() if v != sys.maxsize))

main()
