import helpers

import itertools
import collections

def parse_assignment(a):
    return list(map(int, a.split('-')))

def contains(l1, l2):
    if l1[0] >= l2[0] and l1[1] <= l2[1]:
        return True
    if l2[0] >= l1[0] and l2[1] <= l1[1]:
        return True
    return False

def overlap(l1, l2):
    if l1[0] <= l2[0] <= l1[1]:
        return True
    if l2[0] <= l1[0] <= l2[1]:
        return True
    return False

def main() -> None:
    lines = helpers.read_input()
    for assignments in lines:
        a1, a2 = map(parse_assignment, assignments.split(','))
        print(a1, a2, overlap(a1, a2))

main()
