from __future__ import annotations

import helpers
from functools import cmp_to_key
import itertools
import collections
import re

import fileinput

def is_ordered(seq, ordering):
    for idx, ch1 in enumerate(seq):
        for ch2 in seq[idx+1:]:
            if ch2 not in ordering[ch1]:
                print(' bad', ch1, ch2)
                return False
    return True

def page_sorter(ordering, a, b):
    if b in ordering[a]:
        return -1
    elif a in ordering[b]:
        return 1
    return 0

def main() -> None:
    rules, pages = '\n'.join(helpers.read_input()).split('\n\n')
    rules = rules.split('\n')
    pages = pages.split('\n')
    ordering = collections.defaultdict(set)
    for l in rules:
        left, right = l.split('|')
        ordering[left].add(right)

    goods = []
    bads = []
    for l in pages:
        print('check', l)
        seq = l.split(',')
        if is_ordered(seq, ordering):
            print('good:', l)
            goods.append(seq)
        else:
            print('bad:', l)
            bads.append(seq)

    print(sum(int(v[len(v) // 2]) for v in goods))
    fixed = []
    for bad in bads:
        f = sorted(bad, key=cmp_to_key(lambda a, b: page_sorter(ordering, a, b)))
        fixed.append(f)
    print(sum(int(v[len(v) // 2]) for v in fixed))
    

main()
