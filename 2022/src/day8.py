from __future__ import annotations

import helpers

import itertools
import collections

def vslice(grid, row, col):
    ret = [[], []]
    for j in range(len(grid[row])):
        if j < col:
            ret[0].append(grid[row][j])
        elif j > col:
            ret[1].append(grid[row][j])
    return ret

def hslice(grid, row, col):
    ret = [[], []]
    for j in range(len(grid[row])):
        if j < row:
            ret[0].append(grid[j][col])
        elif j > row:
            ret[1].append(grid[j][col])
    return ret

def calc_score(val, seq):
    ret = 0
    for s in seq:
        ret += 1
        if val <= s:
            break
    return ret

def main() -> None:
    lines = helpers.read_input_digit_grid(int)
    print(lines)

    for row in range(len(lines)):
        for col in range(len(lines[0])):
            vs1, vs2 = vslice(lines, row, col)
            vs1.reverse()
            hs1, hs2 = hslice(lines, row, col)
            hs1.reverse()
            score = calc_score(lines[row][col], vs1)
            score *= calc_score(lines[row][col], vs2)
            score *= calc_score(lines[row][col], hs1)
            score *= calc_score(lines[row][col], hs2)
            print(row, col, score)
            
main()
