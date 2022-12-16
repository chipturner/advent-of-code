from __future__ import annotations

import helpers

import re


def dist(x0, y0, x1, y1):
    return abs(x0 - x1) + abs(y0 - y1)


def boundaries(discs):
    for (x, y), d in discs.items():
        delta = d + 1
        pt = helpers.Point(x - delta, y)
        while pt.x < x:
            yield pt
            pt += helpers.Point(1, -1)
        while pt.x < x + delta:
            yield pt
            pt += helpers.Point(1, 1)
        while pt.x > x:
            yield pt
            pt += helpers.Point(-1, 1)
        while pt.x > x - delta:
            yield pt
            pt += helpers.Point(-1, -1)


sensor_re = re.compile(
    r"Sensor at x=(.*?), y=(.*?): closest beacon is at x=(.*?), y=(.*?)$"
)


def main() -> None:
    lines = helpers.read_input()

    sensor_beacon = dict()
    sensor_discs = dict()
    for line in lines:
        m = sensor_re.match(line)
        s_x, s_y, b_x, b_y = [int(v) for v in m.groups()]
        sensor_beacon[(s_x, s_y)] = (b_x, b_y)
        d = dist(s_x, s_y, b_x, b_y)
        sensor_discs[(s_x, s_y)] = d

    print(list(boundaries({(0, 0): 1})))

    bounds = 4000000
    for b in boundaries(sensor_discs):
        if not (0 <= b.x <= bounds and 0 <= b.y <= bounds):
            continue
        for (x, y), diameter in sensor_discs.items():
            if dist(x, y, b.x, b.y) < diameter + 1:
                break
        else:
            print(b, b.x * 4000000 + b.y)
            break


main()
