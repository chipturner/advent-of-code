from __future__ import annotations

import helpers

import itertools
import collections
import re

step_idx = {"L": 0, "R": 1}


def main() -> None:
    lines = helpers.read_input()
    steps = itertools.cycle(lines[0])
    m = {}
    for line in lines[2:]:
        m[line[0:3]] = line[7:10], line[12:15]

    c = 0
    cur = "AAA"
    for step in steps:
        c += 1
        print(cur, c, step)
        idx = step_idx[step]
        cur = m[cur][idx]
        if cur == "ZZZ":
            break
    print(c)


main()
