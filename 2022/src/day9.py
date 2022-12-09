from __future__ import annotations

import helpers
from helpers import Point

import itertools
import collections


def calc_t_pos(h_pos: Point, t_pos: Point) -> Point:
    dist = (h_pos - t_pos).magnitude()
    if dist < 2:
        return t_pos
    delta = (h_pos - t_pos).sign()
    return t_pos + delta


def main() -> None:
    lines = helpers.read_input()
    print(lines)

    deltas = {
        "U": Point(0, 1),
        "D": Point(0, -1),
        "L": Point(-1, 0),
        "R": Point(1, 0),
    }

    origin = Point(0, 0)
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
                tail_9_visited.add(positions[-1])
    print(len(tail_9_visited))


main()
