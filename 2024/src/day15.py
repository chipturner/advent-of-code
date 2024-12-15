from __future__ import annotations

import helpers

import copy
import itertools
import functools
import collections
import re

import blessed

from helpers import up, right, down, left

move_map = dict(zip('^>v<', (up, right, down, left)))

def make_move(grid, pos, move):
    probe = pos + move
    if grid[probe] == '.':
        grid[probe] = grid[probe - move]
        grid[probe - move] = '.'
        return True
    if grid[probe] == '#':
        return False
    if move in (up, down):
        if grid[probe] == '[':
            if make_move(grid, pos + move, move) and make_move(grid, pos + move + right, move):
                grid[probe] = grid[probe - move]
                grid[probe - move] = '.'
                return True
        if grid[probe] == ']':
            if make_move(grid, pos + move, move) and make_move(grid, pos + move + left, move):
                grid[probe] = grid[probe - move]
                grid[probe - move] = '.'
                return True
        return False
    # left/right
    if make_move(grid, pos + move, move):
        grid[probe] = grid[probe - move]
        grid[probe - move] = '.'
        return True
    return False

def main() -> None:
    lines = "\n".join(helpers.read_input())
    c1, c2 = lines.split('\n\n')
    grid = helpers.Grid.from_list_of_strings(c1.replace('#', '##').replace('O','[]').replace('.', '..').replace('@', '@.').split('\n'))
    moves = list(''.join(c2.split('\n')))

    term = blessed.Terminal()
    echo = functools.partial(print, end='', flush=True)

    pos = grid.find_all('@')[0]
    with term.hidden_cursor(), term.fullscreen():
        while moves:
            echo(term.move_xy(0, 0))
            grid.print()
            print('move', moves[0], pos)
            print()
            move = move_map[moves.pop(0)]
            saved = copy.deepcopy(grid)
            if make_move(grid, pos, move):
                grid[pos] = '.'
                pos = pos + move
                grid[pos] = '@'
            else:
                grid = saved

    grid.print()

    score = 0
    for pos, ch in grid.items():
        if ch == '[':
            score += pos.row * 100 + pos.col
    print(score)


main()
