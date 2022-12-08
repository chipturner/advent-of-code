from __future__ import annotations

import helpers

from typing import Iterable
import numpy


def calc_score(val: int, seq: Iterable[int]) -> int:
    ret = 0
    for s in seq:
        ret += 1
        if val <= s:
            break
    return ret


def main() -> None:
    lines = helpers.read_input_digit_grid(numpy.int_)
    print(lines)

    for row in range(len(lines)):
        for col in range(len(lines[0])):
            right = helpers.grid_line(lines, row, col, (1, 0))
            left = helpers.grid_line(lines, row, col, (-1, 0))
            up = helpers.grid_line(lines, row, col, (0, 1))
            down = helpers.grid_line(lines, row, col, (0, -1))

            score = calc_score(lines[row][col], right)
            score *= calc_score(lines[row][col], left)
            score *= calc_score(lines[row][col], up)
            score *= calc_score(lines[row][col], down)
            print(row, col, score)


main()
