from __future__ import annotations

import helpers
from helpers import up, down, left, right

import itertools
import collections
import re

def perimiter(grid, region):
    region_pts = {r[0] for r in region}
    fence = list()
    for pos, ch in region:
        for n in grid.neighbors4(pos):
            if n not in region_pts:
                fence.append(n)
    return fence

def edges(grid, region, perimiter):
    region_pts = {r[0] for r in region}
    perimiter = set(perimiter)
    ret = 0

    for row in range(grid.nrows):
        col = 0
        wall_checks = []
        while 0 <= col < grid.ncols:
            probe = helpers.Coordinate(row, col)
            #print('c', probe, probe in perimiter, probe + down in region_pts)
            walking_wall = probe in perimiter and probe + down in region_pts
            wall_checks.append(walking_wall)
            col += 1
        #print(wall_checks)
        deltas = sum(a != b for a, b in itertools.pairwise(wall_checks))
        walls = deltas // 2
        #print(deltas, walls)
        ret += walls

    for row in range(grid.nrows):
        col = grid.ncols - 1
        wall_checks = []
        while 0 <= col < grid.ncols:
            probe = helpers.Coordinate(row, col)
            #print('c', probe, probe in perimiter, probe + up in region_pts)
            walking_wall = probe in perimiter and probe + up in region_pts
            wall_checks.append(walking_wall)
            col -= 1
        #print(wall_checks)
        deltas = sum(a != b for a, b in itertools.pairwise(wall_checks))
        walls = deltas // 2
        #print(deltas, walls)
        ret += walls

    for col in range(grid.ncols):
        row = 0
        wall_checks = []
        while 0 <= row < grid.nrows:
            probe = helpers.Coordinate(row, col)
            #print('c', probe, probe in perimiter, probe + right in region_pts)
            walking_wall = probe in perimiter and probe + right in region_pts
            wall_checks.append(walking_wall)
            row += 1
        #print(wall_checks)
        deltas = sum(a != b for a, b in itertools.pairwise(wall_checks))
        walls = deltas // 2
        #print(deltas, walls)
        ret += walls

    for col in range(grid.ncols):
        row = grid.nrows - 1
        wall_checks = []
        while 0 <= row < grid.nrows:
            probe = helpers.Coordinate(row, col)
            #print('c', probe, probe in perimiter, probe + left in region_pts)
            walking_wall = probe in perimiter and probe + left in region_pts
            wall_checks.append(walking_wall)
            row -= 1
        #print(wall_checks)
        deltas = sum(a != b for a, b in itertools.pairwise(wall_checks))
        walls = deltas // 2
        #print(deltas, walls)
        ret += walls

    return ret
            
def main() -> None:
    grid = helpers.Grid.from_list_of_strings(helpers.read_input()).pad('.')
    grid.print()

    seen = {}
    regions = []
    for pos, ch in grid.items():
        if ch == '.':
            continue
        if pos not in seen:
            regions.append(list(grid.floodfill(pos)))
            seen.update(regions[-1])
    s = 0
    for r in regions:
        f = helpers.SparseGrid('.')
        p = perimiter(grid, r)
        for pos in p:
            f[pos] = '+'
        for pos, ch in r:
            f[pos] = ch
        print()
        f.print()
        print(f[r[0][0]], len(r), len(p), edges(grid, r, p))
        s += len(r) * edges(grid, r, p)
    print(s)

main()
