from __future__ import annotations

import helpers

import itertools
import collections
import re


def main() -> None:
    lines = helpers.read_input()
    print(lines)
    cards = []
    for line in lines:
        m = re.match(r'Card +(\d+): +(.*) +\| +(.*) *$', line)
        card, winners, mine = m.groups()
        cards.append((set(winners.strip().split()), set(mine.strip().split())))
    score = 0
    for w, m in cards:
        if not w.intersection(m):
            continue
        s = 2 ** (len(m.intersection(w)) - 1)
        print(len(m.intersection(w)), s, m.intersection(w), w, m)
        score += s
    print(score)


main()
