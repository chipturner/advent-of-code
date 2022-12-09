from __future__ import annotations

import numpy

import helpers

import itertools
import collections

def calc_t_pos(h_pos, t_pos):
    dist = numpy.linalg.norm(h_pos - t_pos)
    print(h_pos, t_pos, dist)
    if dist < 2:
        return t_pos
    delta = numpy.sign(h_pos - t_pos)
    return t_pos + delta

def main() -> None:
    lines = helpers.read_input()
    print(lines)

    deltas = { 'U': numpy.array((0, 1)), 'D': numpy.array((0, -1)), 'L': numpy.array((-1, 0)), 'R': numpy.array((1, 0)) }

    h_pos = numpy.array((0, 0))
    t_pos = numpy.array((0, 0))
    visited = set()
    for direction, distance in [ s.split() for s in lines ]:
        for i in range(int(distance)):
            h_pos += deltas[direction]
            t_pos = calc_t_pos(h_pos, t_pos)
            print(h_pos, t_pos)
            visited.add(tuple(t_pos))
    print(len(visited))

main()
