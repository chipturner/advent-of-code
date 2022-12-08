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

def main() -> None:
    lines = helpers.read_input_digit_grid(int)
    print(lines)

    count = 0
    for row in range(len(lines)):
        for col in range(len(lines[0])):
            vs1, vs2 = vslice(lines, row, col)
            hs1, hs2 = hslice(lines, row, col)
            if (row == 0 or row == len(lines) - 1 or col == 0 or col == len(lines) - 1 or
                lines[row][col] > max(vs1) or lines[row][col] >max(hs1) or
                lines[row][col] > max(vs2) or lines[row][col] >max(hs2)):
                count += 1
                
    print(count)
            
main()
