from __future__ import annotations

import helpers

import itertools
import math

step_idx = {"L": 0, "R": 1}


def main() -> None:
    lines = helpers.read_input()
    steps = itertools.cycle(lines[0])
    m = {}
    for line in lines[2:]:
        m[line[0:3]] = line[7:10], line[12:15]

    c = 0
    curs = list([s for s in m if s[-1] == "A"])
    hop_counts = [0] * (len(curs))

    for idx, cur in enumerate(curs):
        c = 0
        for step in steps:
            c += 1
            curs[idx] = m[curs[idx]][step_idx[step]]
            if curs[idx][-1] == "Z":
                hop_counts[idx] = c
                break
        print(hop_counts)
    print(math.lcm(*hop_counts))


main()
