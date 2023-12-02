from __future__ import annotations

import helpers

import itertools
import collections

color = collections.namedtuple("color", ["red", "green", "blue"], defaults=(0, 0, 0))


def compare(a, b):
    return a.red <= b.red and a.green <= b.green and a.blue <= b.blue


def main() -> None:
    lines = helpers.read_input()
    s = 0
    for line in lines:
        _, day, x = line.split(maxsplit=2)
        x = x.replace(",", "").split("; ")
        nope = False
        bag = color()
        for r in x:
            elems = r.split()
            elems = color(
                **dict([r[::-1] for r in zip(map(int, elems[::2]), elems[1::2])])
            )
            bag = color(
                red=max(elems.red, bag.red),
                green=max(elems.green, bag.green),
                blue=max(elems.blue, bag.blue),
            )
        s += bag.red * bag.blue * bag.green

    print(s)


main()
