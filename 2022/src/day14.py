from __future__ import annotations

import helpers

from typing import Dict, Tuple
from dataclasses import dataclass


@dataclass
class Grid:
    grid: Dict[Tuple[int, int], str]
    floor: int = 0

    def __post_init__(self):
        self.floor = max(p[1] for p in self.grid) + 2

    def print_grid(self):
        x_min = sorted([p[0] for p in self.grid.keys()])[0]
        x_max = sorted([p[0] for p in self.grid.keys()])[-1] + 1
        y_min = 0
        y_max = sorted([p[1] for p in self.grid.keys()])[-1] + 2

        for y in range(y_min, y_max):
            for x in range(x_min, x_max):
                print(self.get(x, y), end="")
            print()

    def get(self, x, y):
        if y == self.floor:
            return "#"
        return self.grid.get((x, y), ".")

    def sand_lands(self):
        x, y = 500, 0
        while self.get(500, 0) != "o":
            stuck = False
            while not stuck:
                for next_pos in [(x, y + 1), (x - 1, y + 1), (x + 1, y + 1)]:
                    ch = self.get(*next_pos)
                    if ch == ".":
                        x, y = next_pos
                        break
                else:
                    stuck = True
            self.grid[x, y] = "o"
            return True


def inclusive_range(i, j):
    if i > j:
        i, j = j, i
    return list(range(i, j + 1))


def main() -> None:
    lines = helpers.read_input()
    print(lines)

    grid = dict()
    for line in lines:
        segments = [
            list(map(int, segment.split(","))) for segment in line.split(" -> ")
        ]
        print(segments)
        p1 = segments.pop(0)
        for p2 in segments:
            print(p1, p2)
            if p1[0] == p2[0]:
                for i in inclusive_range(p1[1], p2[1]):
                    grid[(p1[0], i)] = "#"
            else:
                for i in inclusive_range(p1[0], p2[0]):
                    grid[(i, p1[1])] = "#"

            p1 = p2
    grid = Grid(grid)
    grid.print_grid()
    print("go!")
    rested = 0
    while grid.sand_lands():
        rested += 1
    print(rested)


main()
