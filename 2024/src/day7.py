from __future__ import annotations

import helpers

import itertools
import collections
import re

def can_match(val, accum, args):
    if accum > val:
        return False
    if len(args) == 0:
        return val == accum
    if (can_match(val, accum + args[0], args[1:]) or
        can_match(val, accum * args[0], args[1:]) or
        can_match(val, int(str(accum) + str(args[0])), args[1:])):
        return True
    return False

def main() -> None:
    lines = helpers.read_input()
    eqs = []
    for line in lines:
        eqs.append([int(x) for x in line.replace(':', '').split(' ')])
    print(eqs)

    s = 0
    for eq in eqs:
        if can_match(eq[0], eq[1], eq[2:]):
            print('yay', eq)
            s += eq[0]
    print(s)


main()
