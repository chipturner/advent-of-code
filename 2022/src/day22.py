from __future__ import annotations

import numpy
import helpers

import itertools
import collections
import fileinput


def pos_advance(grid, pos, d):
    maybe_pos = pos + d
    maybe_pos[0] = maybe_pos[0] % grid.shape[0]
    maybe_pos[1] = maybe_pos[1] % grid.shape[1]
    if grid[maybe_pos[0], maybe_pos[1]] == " ":
        return pos_advance(grid, maybe_pos, d)
    return maybe_pos


def main() -> None:
    lines = list([l.rstrip("\n") for l in fileinput.input()])

    instructions = []
    for lchunk in lines.pop().split("L"):
        for rchunk in lchunk.split("R"):
            instructions.append(int(rchunk))
            instructions.append("R")
        instructions.pop()
        instructions.append("L")
    instructions.pop()
    lines.pop()
    print(instructions)

    height = len(lines)
    width = max([len(l) for l in lines])
    grid = numpy.ndarray((width, height), dtype="|U1")

    for row_num in range(height):
        for col_num in range(width):
            if col_num >= len(lines[row_num]):
                grid[col_num, row_num] = " "
            else:
                grid[col_num, row_num] = lines[row_num][col_num]

    dirs = [numpy.array(v) for v in [(1, 0), (0, 1), (-1, 0), (0, -1)]]
    cur_dir = 0
    pos = numpy.array([(numpy.where(grid[:, 0] == ".")[0][0]), 0])

    for ins in instructions:
        if ins == "L":
            cur_dir = (cur_dir - 1) % 4
        elif ins == "R":
            cur_dir = (cur_dir + 1) % 4
        else:
            d = dirs[cur_dir]
            for step in range(ins):
                maybe_pos = pos_advance(grid, pos, d)
                print(pos, d, maybe_pos)
                if grid[maybe_pos[0], maybe_pos[1]] == "#":
                    break
                pos = maybe_pos
                grid[pos[0], pos[1]] = "X"

    print(pos)
    print(1000 * (pos[1] + 1) + 4 * (pos[0] + 1) + cur_dir)


main()
