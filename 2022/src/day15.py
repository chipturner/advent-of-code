from __future__ import annotations

import helpers

import sys

import itertools
import collections

from dataclasses import dataclass

import re


@dataclass
class Grid:
    grid: Dict[Tuple[int, int], str]

    def x_range(self):
        x_min = sorted([p[0] for p in self.grid.keys()])[0]
        x_max = sorted([p[0] for p in self.grid.keys()])[-1]
        return range(x_min, x_max + 1)

    def y_range(self):
        y_min = sorted([p[1] for p in self.grid.keys()])[0]
        y_max = sorted([p[1] for p in self.grid.keys()])[-1]
        return range(y_min, y_max + 1)

    def print_grid(self):
        for y in self.y_range():
            print(f"{y:02d}: ", end="")
            for x in self.x_range():
                print(self.get(x, y), end="")
            print()

    def get(self, x, y):
        return self.grid.get((x, y), ".")

    def set(self, x, y, v):
        self.grid[x, y] = v


def dist(x0, y0, x1, y1):
    return abs(x0 - x1) + abs(y0 - y1)


def boundaries(discs):
    for (x, y), d in discs.items():
        delta = d + 1
        pt = [x - delta, y]
        while pt[0] < x:
            yield tuple(pt)
            pt[0] += 1
            pt[1] -= 1
        while pt[0] < x + delta:
            yield tuple(pt)
            pt[0] += 1
            pt[1] += 1
        while pt[0] > x:
            yield tuple(pt)
            pt[0] -= 1
            pt[1] += 1
        while pt[0] > x - delta:
            yield tuple(pt)
            pt[0] -= 1
            pt[1] -= 1


sensor_re = re.compile(
    r"Sensor at x=(.*?), y=(.*?): closest beacon is at x=(.*?), y=(.*?)$"
)


def main() -> None:
    lines = helpers.read_input()

    g = Grid({})
    sensor_beacon = dict()
    sensor_discs = dict()
    for line in lines:
        m = sensor_re.match(line)
        s_x, s_y, b_x, b_y = [int(v) for v in m.groups()]
        sensor_beacon[(s_x, s_y)] = (b_x, b_y)
        g.set(s_x, s_y, "S")
        g.set(b_x, b_y, "B")
        d = dist(s_x, s_y, b_x, b_y)
        sensor_discs[(s_x, s_y)] = d

    # g.print_grid()

    print(list(boundaries({(0, 0): 1})))

    bounds = 4000000
    for b in boundaries(sensor_discs):
        if not (0 <= b[0] <= bounds and 0 <= b[1] <= bounds):
            continue
        for (x, y), diameter in sensor_discs.items():
            if dist(x, y, *b) < diameter + 1:
                break
        else:
            print(b, b[0] * 4000000 + b[1])
            break


main()
