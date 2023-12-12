from __future__ import annotations

import helpers

import itertools
import collections
import re

def all_candidates(state):
    if '?' not in state:
        yield state
    left_right = state.split('?', maxsplit=1)
    if len(left_right) == 1:
        yield left_right[0]
        return

    left, right = left_right
    for candidate in all_candidates(right):
        yield left + '.' + candidate
        yield left + '#' + candidate

def matches(candidate, blocks):
    return blocks == [ len(v) for v in candidate.replace('.', ' ').split() ]

def main() -> None:
    s = 0
    for state, blocks in helpers.read_input_split():
        blocks = [ int(i) for i in blocks.split(',') ]
        qs = sum(ch == '?' for ch in state)
        hits = set()
        for candidate in all_candidates(state):
            if matches(candidate, blocks):
                print(f'block {candidate} matches {blocks}')
                hits.add(candidate)
        print('total', len(hits))
        s += len(hits)
    print(s)


main()
