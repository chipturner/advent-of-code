from __future__ import annotations

import helpers
from helpers import Point

import itertools
import collections

pieces = itertools.cycle(
    [
        [Point(n, 0) for n in range(4)],
        [Point(1, 0)] + [Point(n, 1) for n in range(3)] + [Point(1, 2)],
        [Point(2, 0), Point(2, 1), Point(0, 2), Point(1, 2), Point(2, 2)],
        [Point(0, n) for n in range(4)],
        [Point(i, j) for i in range(2) for j in range(2)],
    ]
)

piece_heights = itertools.cycle([1, 3, 3, 4, 2])


def collides(board, piece, displacement):
    new_piece = [pt + displacement for pt in piece]
    for pt in new_piece:
        if pt in board:
            return True
    return False


def place_piece(board, piece, displacement, ch):
    if collides(board, piece, displacement):
        return
    new_piece = [pt + displacement for pt in piece]
    for pt in new_piece:
        board[pt] = ch


def shift_board(board, n):
    new_board = {Point(p.x, p.y + n): val for p, val in board.items()}
    for i in range(n):
        new_board[Point(0, i)] = "|"
        new_board[Point(8, i)] = "|"
    return new_board


def calc_shift_padding(board, piece_height):
    top_rock_y = min(p.y for p in board if p.x not in (0, 8))
    return 3 - top_rock_y + piece_height


def calc_column_height(board):
    top_rock_y = min(p.y for p in board if p.x not in (0, 8))
    bottom_wall_y = max(p.y for p in board)
    return bottom_wall_y - top_rock_y


def ghost_piece(board, piece, displacement):
    board = board.copy()
    place_piece(board, piece, displacement, "@")
    return board


def main() -> None:
    lines = helpers.read_input()
    jets = enumerate(itertools.cycle(lines[0]))

    board = {Point(i, 0): "-" for i in range(9)}

    show_output = False

    rock_count = 0
    for piece, piece_height in zip(pieces, piece_heights):
        print("New rock!")
        padding = calc_shift_padding(board, piece_height)
        board = shift_board(board, padding)
        if show_output:
            helpers.print_grid(ghost_piece(board, piece, Point(0, 3)))

        y_pos = 0
        x_delta = 3
        dropping = True

        while dropping:
            if show_output:
                helpers.print_grid(ghost_piece(board, piece, Point(x_delta, y_pos)))
            jet_idx, gust_ch = next(jets)
            gust = gust_ch == "<" and -1 or 1
            print(f"Gusting {gust_ch} ({jet_idx})")
            print()

            if not collides(board, piece, Point(x_delta + gust, y_pos)):
                x_delta += gust

            print("Dropping")
            dropping = not collides(board, piece, Point(x_delta, y_pos + 1))
            y_pos += 1

        if show_output:
            helpers.print_grid(ghost_piece(board, piece, Point(x_delta, y_pos - 1)))
        place_piece(board, piece, Point(x_delta, y_pos - 1), "#")

        rock_count += 1
        print(f"Rock {rock_count}, height {calc_column_height(board)}")
        print()
        if rock_count == 2022:
            break


main()
