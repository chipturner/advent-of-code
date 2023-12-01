from __future__ import annotations

import helpers

import itertools
import collections


def main() -> None:
    lines = helpers.read_input()
    vals = []
    for line in lines:
        digits = list(filter(lambda c: c.isdigit(), line))
        val = digits[0] + digits[-1]
        vals.append(int(val))
    print(sum(vals))


main()
