from __future__ import annotations

import helpers

import itertools
import collections
import re

def hasher(s):
    val = 0
    for c in s:
        val += ord(c)
        val = val * 17 % 256
    return val

def main() -> None:
    seq = helpers.read_input()[0].split(',')
    print(seq)
    for s in seq:
        print(s, hasher(s))
    print(sum(hasher(s) for s in seq))

main()
