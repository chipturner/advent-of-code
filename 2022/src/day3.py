import helpers

import itertools
import collections


def priority(ch):
    if "a" <= ch <= "z":
        return ord(ch) - ord("a") + 1
    else:
        return ord(ch) - ord("A") + 27


def main() -> None:
    lines = helpers.read_input()
    tot = 0
    for sack in lines:
        c1, c2 = set(sack[: len(sack) // 2]), set(sack[len(sack) // 2 :])
        v = [priority(ch) for ch in c1.intersection(c2)][0]
        tot += v
    print(tot)


main()
