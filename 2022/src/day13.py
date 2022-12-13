from __future__ import annotations

import sys

import helpers

import itertools
import collections

def compare(l1, l2, indent=0):
    print(f'{" "*indent}- Compare {l1} vs {l2}')

    if type(l1) == int and type(l2) == list:
        return compare([l1], l2, indent+1)
    if type(l2) == int and type(l1) == list:
        return compare(l1, [l2], indent+1)

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
    lines = sys.stdin.read()
    chunks = lines.strip().split('\n\n')
    print(chunks)

    proper = []
    for idx, chunk in enumerate(chunks):
        left, right = [ eval(s) for s in chunk.split('\n') ]
        print()
        print(f'== Pair {idx+1} ==')
        if compare(left, right) == -1:
            proper.append(idx+1)
    print(sum(proper))

main()
