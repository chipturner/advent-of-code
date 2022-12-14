from __future__ import annotations

import helpers

import itertools
import collections

def inclusive_range(i, j):
    if i > j:
        i, j = j, i
    return list(range(i, j+1))

def print_grid(grid):
    x_min = sorted([ p[0] for p in grid.keys() ])[0] - 1
    x_max = sorted([ p[0] for p in grid.keys() ])[-1] + 1
    y_min = 0
    y_max = sorted([ p[1] for p in grid.keys() ])[-1] + 1

    for y in range(y_min, y_max):
        for x in range(x_min, x_max):
            if (x, y) in grid:
                print(grid[(x, y)], end='')
        print()

def plump_grid(grid):
    x_min = sorted([ p[0] for p in grid.keys() ])[0]
    x_max = sorted([ p[0] for p in grid.keys() ])[-1] + 1
    y_min = 0
    y_max = sorted([ p[1] for p in grid.keys() ])[-1] + 1

    for y in range(y_min, y_max):
        for x in range(x_min, x_max):
            if (x, y) not in grid:
                grid[(x, y)] = '.'

def sand_lands(grid):
    x, y = 500, 0
    while True:
        stuck = False
        voided = False
        while not stuck and not voided:
            for next_pos in [ (x, y + 1), (x - 1, y + 1), (x + 1, y + 1) ]:
                ch = grid.get(next_pos)
                if ch == '.':
                    x, y = next_pos
                    break
                elif ch is None:
                    voided = True
                    break
            else:
                stuck = True
        if voided:
            return False
        else:
            grid[x, y] = 'o'
            return True
            
                

def main() -> None:
    lines = helpers.read_input()
    print(lines)

    grid = dict()
    for line in lines:
        segments = [ list(map(int, segment.split(','))) for segment in line.split(' -> ') ]
        print(segments)
        p1 = segments.pop(0)
        for p2 in segments:
            print(p1, p2)
            if p1[0] == p2[0]:
                for i in inclusive_range(p1[1], p2[1]):
                    grid[(p1[0], i)] = '#'
            else:
                for i in inclusive_range(p1[0], p2[0]):
                    grid[(i, p1[1])] = '#'
                    
            p1 = p2
    plump_grid(grid)
    print_grid(grid)
    print()
    rested = 0
    while sand_lands(grid):
        print_grid(grid)
        print()
        rested += 1
    print(rested)

main()
