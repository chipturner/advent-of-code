from __future__ import annotations

import helpers

import itertools
import collections
import re


def main() -> None:
    lines = helpers.read_input()
    l, r = [], []
    for line in lines:
        vl, vr = line.split()
        l.append(int(vl))
        r.append(int(vr))
    l.sort()
    r.sort()
    p = [abs(vl - vr) for vr, vl in zip(l, r)]
    print(sum(p))

    t = 0
    for vl in l:
        s = sum([1 if vr == vl else 0 for vr in r])
        t += vl * s
    print(t)


main()
