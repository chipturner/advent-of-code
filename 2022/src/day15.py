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
            print(f'{y:02d}: ', end='')
            for x in self.x_range():
                print(self.get(x, y), end="")
            print()

    def get(self, x, y):
        return self.grid.get((x, y), ".")

    def set(self, x, y, v):
        self.grid[x, y] = v

def dist(x0, y0, x1, y1):
    return abs(x0 - x1) + abs(y0 - y1)

sensor_re = re.compile(r'Sensor at x=(.*?), y=(.*?): closest beacon is at x=(.*?), y=(.*?)$')

def main() -> None:
    lines = helpers.read_input()

    g = Grid({})
    sensor_beacon = dict()
    for line in lines:
        m = sensor_re.match(line)
        s_x, s_y, b_x, b_y = [ int(v) for v in m.groups() ]
        sensor_beacon[(s_x, s_y)] = (b_x, b_y)
        g.set(s_x, s_y, 'S')
        g.set(b_x, b_y, 'B')
        d = dist(s_x, s_y, b_x, b_y) // 2 + 1
        
        g.set(s_x - d, s_y, '!')
        g.set(s_x + d, s_y, '!')
        g.set(s_x, s_y - d, '!')
        g.set(s_x, s_y + d, '!')

#    g.print_grid()

    target_y = 2000000
    count = 0
    print()
#    print('xx: ', end='')
    for x in g.x_range():
        beacon_possible = True
        pt = x, target_y
        for sensor, beacon in sensor_beacon.items():
            sensor_pt_distance = dist(*sensor, *pt)
            sensor_beacon_distance = dist(*sensor, *beacon)
#            print(pt, sensor_pt_distance, sensor_beacon_distance)
            if pt != beacon and sensor_pt_distance <= sensor_beacon_distance:
                beacon_possible = False
#        print(beacon_possible and g.get(x, target_y) or '#', end='')
        if not beacon_possible:
            count += 1
    print()
    print(count)
        

main()
