from __future__ import annotations

import helpers

import itertools
import collections
import re


def main() -> None:
    lines = helpers.read_input()
    s = 0
    doing = True
    for line in lines:
        vals = re.finditer(r"do\(\)|don't\(\)|mul\((\d{,3}),(\d{,3})\)", line)
        actuals = []
        for m in vals:
            print(m.group(0))
            if m.group(0) == "don't()":
                doing = False
            elif m.group(0) == "do()":
                doing = True
            if doing and m.group(0).startswith("mul"):
                actuals.append(m)
        s += sum(int(m[1]) * int(m[2]) for m in actuals)
    print(s)


main()
