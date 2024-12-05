from __future__ import annotations

import helpers

import itertools
import collections
import re

import fileinput

def main() -> None:
    rules, pages = '\n'.join(helpers.read_input()).split('\n\n')
    rules = rules.split('\n')
    pages = pages.split('\n')
    ordering = collections.defaultdict(set)
    for l in rules:
        left, right = l.split('|')
        ordering[left].add(right)

    goods = []
    for l in pages:
        print('check', l)
        seq = l.split(',')
        bad = False
        for idx, ch1 in enumerate(seq):
            for ch2 in seq[idx+1:]:
                if ch2 not in ordering[ch1]:
                    print(' bad', ch1, ch2)
                    bad = True
                    break
        if bad:
            print('bad:', l)
        else:
            print('good:', l)
            goods.append(seq)

    print(sum(int(v[len(v) // 2]) for v in goods))

main()
