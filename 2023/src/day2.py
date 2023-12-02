from __future__ import annotations

import helpers

import itertools
import collections

color = collections.namedtuple('color', ['red', 'green', 'blue'], defaults=(0,0,0))

def compare(a, b):
    return a.red <= b.red and a.green <= b.green and a.blue <= b.blue

def main() -> None:
    lines = helpers.read_input()
    bag = color(red=12, green=13, blue=14)
    s = 0
    for line in lines:
        _, day, x = line.split(maxsplit=2)
        x = x.replace(',', '').split('; ')
        nope = False
        print(day)
        for r in x:
            elems = r.split()
            elems = color(**dict([ r[::-1] for r in zip(map(int, elems[::2]), elems[1::2]) ]))
            print('test', elems, bag, compare(elems, bag))
            if not compare(elems, bag):
                nope = True
                print('nope', day)
                break
        if not nope:
            s += int(day[:-1])
    print(s)

main()
