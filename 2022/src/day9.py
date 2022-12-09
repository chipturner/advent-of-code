from __future__ import annotations

import numpy

import helpers

import itertools
import collections


def calc_t_pos(h_pos, t_pos):
    dist = numpy.linalg.norm(h_pos - t_pos)
    if dist < 2:
        return t_pos
    delta = numpy.sign(h_pos - t_pos)
    return t_pos + delta


def main() -> None:
    lines = helpers.read_input()
    print(lines)

    deltas = {
        "U": numpy.array((0, 1)),
        "D": numpy.array((0, -1)),
        "L": numpy.array((-1, 0)),
        "R": numpy.array((1, 0)),
    }

    origin = numpy.array((0, 0))
    origin.flags["WRITEABLE"] = False
    positions = [origin]

    tail_9_visited = set()
    for direction, distance in [s.split() for s in lines]:
        for i in range(int(distance)):
            if len(positions) < 10:
                positions.append(origin)
            positions[0] = positions[0] + deltas[direction]
            for idx in range(1, len(positions)):
                positions[idx] = calc_t_pos(positions[idx - 1], positions[idx])
            if len(positions) == 10:
                tail_9_visited.add(tuple(positions[-1]))
    print(len(tail_9_visited))


main()
