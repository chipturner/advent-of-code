from __future__ import annotations

import helpers

import itertools
import collections
import re

def walk_ascent(grid, pos):
    ch = grid[pos]
    if ch == '9':
        print('peak', pos)
        return 1

    ret = 0
    for n in grid.neighbors4(pos):
        if grid[n] == f'{int(ch) + 1}':
            ret += walk_ascent(grid, n)
    return ret

def main() -> None:
    grid = helpers.Grid.from_list_of_strings(helpers.read_input())

    heads = []
    for pos, ch in grid.items():
        if ch == '0':
            print(f'trailhead at {pos}')
            heads.append(pos)

    ret = 0
    for head in heads:
        nines = walk_ascent(grid, head)
        print(nines)
        ret += nines
    print(ret)

main()
