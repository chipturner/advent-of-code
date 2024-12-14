from __future__ import annotations

import helpers

import itertools
import collections
import re

from dataclasses import dataclass

@dataclass
class Robot:
    x: int
    y: int
    vx: int
    vy: int


def quadrant(robot, wide, tall):
    if robot.x == wide // 2:
        return None
    if robot.y == tall // 2:
        return None

    if robot.x < wide // 2 and robot.y < tall // 2:
        return 1
    if robot.x > wide // 2 and robot.y < tall // 2:
        return 2
    if robot.x < wide // 2 and robot.y > tall // 2:
        return 3
    if robot.x > wide // 2 and robot.y > tall // 2:
        return 4


def main() -> None:
    lines = helpers.read_input()

    robots = []
    for line in lines:
        robots.append(Robot(*[int(v) for v in re.findall(r'[-0-9]+', line)]))
    print(robots)

    if len(lines) < 100:
        wide, tall = 11, 7
    else:
        wide, tall = 101, 103

    grid_bots = collections.defaultdict(int)
    for r in robots:
        r.x = (r.x + 100 * r.vx) % wide
        r.y = (r.y + 100 * r.vy) % tall
        q = quadrant(r, wide, tall)
        if q is not None:
            print('assign', r.x, r.y, q)
            grid_bots[q] += 1
        else:
            print('discard', r.x, r.y)
    print(grid_bots)

    g = helpers.Grid.from_empty(tall, wide, '.')
    for idx, robot in enumerate(robots):
        g[(robot.y, robot.x)] = 'R'
    g.print()

    v = 1
    for q, n in grid_bots.items():
        v *= n
    print(v)
        

main()
