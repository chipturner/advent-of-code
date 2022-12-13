from __future__ import annotations

import sys


import itertools
import functools


def compare(l1, l2, indent=0):
    print(f'{" "*indent}- Compare {l1} vs {l2}')

    if type(l1) == int and type(l2) == list:
        return compare([l1], l2, indent + 1)
    if type(l2) == int and type(l1) == list:
        return compare(l1, [l2], indent + 1)

    if type(l1) == int and type(l2) == int:
        if l1 < l2:
            return -1
        elif l1 == l2:
            return 0
        else:
            return 1

    for l, r in itertools.zip_longest(l1, l2):
        if l is None:
            return -1
        if r is None:
            return 1
        if (v := compare(l, r)) != 0:
            return v

    return 0


def main() -> None:
    lines = ("[[2]]\n[[6]]\n" + sys.stdin.read().replace("\n\n", "\n").strip()).split()
    entries = [eval(s) for s in lines]
    print(entries)

    entries.sort(key=functools.cmp_to_key(compare))
    ret = 1
    for idx, v in enumerate(entries):
        if v == [[2]] or v == [[6]]:
            ret *= idx + 1
    print(ret)


main()
