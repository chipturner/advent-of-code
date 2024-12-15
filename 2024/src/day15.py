from __future__ import annotations

import helpers

import itertools
import collections
import re

from helpers import up, right, down, left

move_map = dict(zip('^>v<', (up, right, down, left)))

def main() -> None:
    lines = "\n".join(helpers.read_input())
    c1, c2 = lines.split('\n\n')
    grid = helpers.Grid.from_list_of_strings(c1.split('\n'))
    moves = list(''.join(c2.split('\n')))

    pos = grid.find_all('@')[0]
    while moves:
        print('move', moves[0], pos)
        grid.print()
        print('done')
        print()
        move = move_map[moves.pop(0)]

        probe = move + pos
        while grid[probe] == 'O':
            probe += move
        if grid[probe] == '#':
            continue

        while probe != pos:
            grid[probe] = grid[probe - move]
            probe -= move
        grid[pos] = '.'
        pos += move

    score = 0
    for pos, ch in grid.items():
        if ch == 'O':
            score += pos.row * 100 + pos.col
    print(score)


main()
