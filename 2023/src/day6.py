from __future__ import annotations

import helpers

import itertools
import collections
import re

def dist_traveled(held, total):
    if held >= total:
        return 0
    return held * (total - held)

def main() -> None:
    lines = helpers.read_input()
    times = int(lines[0].split(maxsplit=1)[1].replace(' ', ''))
    dists = int(lines[1].split(maxsplit=1)[1].replace(' ', ''))
    print(times,dists)
    time_dists = [ [times, dists] ]
    print(times, dists)

    tot = 1
    for t, d in time_dists:
        wins = 0
        for held in range(t):
            nd = dist_traveled(held, t)
            if d < nd:
                # print(t, d, held)
                wins += 1
        tot *= wins
    print(tot)

main()
