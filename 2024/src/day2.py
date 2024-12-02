from __future__ import annotations

import helpers

import itertools
import collections
import re

def sign(n):
    if n < 0:
        return -1
    else:
        return 1


def main() -> None:
    lines = [list(map(int, l.split())) for l in helpers.read_input()]
    print(lines)

    c = 0
    for big_s in lines:
        for removed in range(len(big_s)):
            s = big_s[:removed] + big_s[removed+1:]
            deltas = [d[0] - d[1] for d in zip(s[:-1], s[1:])]
            safe = all(sign(deltas[0]) == sign(p) and 0 < abs(p) <= 3 for p in deltas)
            if safe:
                break
        print(safe)
        c += safe
    print(c)


main()
