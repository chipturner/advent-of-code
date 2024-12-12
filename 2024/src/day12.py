from __future__ import annotations

import helpers

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
        # print(f[r[0][0]], len(r), len(p))
        s += len(r) * len(p)
    print(s)

main()
