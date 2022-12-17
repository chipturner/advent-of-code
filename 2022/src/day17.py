from __future__ import annotations

import helpers
from helpers import Point

import hashlib
import numpy
import itertools
import more_itertools


raw_pieces = [
    [Point(n, 0) for n in range(4)],
    [Point(1, 0)] + [Point(n, 1) for n in range(3)] + [Point(1, 2)],
    [Point(2, 0), Point(2, 1), Point(0, 2), Point(1, 2), Point(2, 2)],
    [Point(0, n) for n in range(4)],
    [Point(i, j) for i in range(2) for j in range(2)],
]

pieces = itertools.cycle(raw_pieces)

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
    print(len(board))
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


def calc_board_top_bitmap(board):
    array = numpy.zeros([7, 32], dtype=numpy.uint8)
    for x in range(1, 8):
        for y in range(32):
            array[x - 1, y] = board.get(Point(x, y)) == "#"
    return hashlib.sha1(array.data).hexdigest()


def main() -> None:
    lines = helpers.read_input()
    jets = more_itertools.peekable(enumerate(itertools.cycle(lines[0])))

    board = {Point(i, 0): "-" for i in range(9)}

    show_output = False

    fingerprint_first_seen = dict()
    cycle_heights = {}
    for rock_count, (piece, piece_height) in enumerate(zip(pieces, piece_heights)):
        top_bitmap = calc_board_top_bitmap(board)
        jet_count = jets.peek()[0]
        fingerprint = (
            rock_count % len(raw_pieces),
            jet_count % len(lines[0]),
            top_bitmap,
        )
        column_height = calc_column_height(board)
        if fingerprint in fingerprint_first_seen:
            cycle_start_count, cycle_start_height = fingerprint_first_seen[fingerprint]
            cycle_growth_height = column_height - cycle_start_height
            cycle_repeat_period = rock_count - cycle_start_count
            print(
                f"CYCLE found, rock {cycle_start_count}->{rock_count} ({rock_count-cycle_start_count}) height {cycle_start_height}->{column_height} ({column_height-cycle_start_height})",
                fingerprint,
                fingerprint_first_seen[fingerprint],
            )
            break
        else:
            fingerprint_first_seen[fingerprint] = (
                rock_count,
                column_height,
            )

        cycle_heights[rock_count] = column_height
        if show_output:
            print(f"Rock {rock_count} jet {jet_count} row top {top_bitmap}")

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
            if show_output:
                print(f"Gusting {gust_ch} ({jet_idx})")
                print()

            if not collides(board, piece, Point(x_delta + gust, y_pos)):
                x_delta += gust

            if show_output:
                print("Dropping")
            dropping = not collides(board, piece, Point(x_delta, y_pos + 1))
            y_pos += 1

        if show_output:
            helpers.print_grid(ghost_piece(board, piece, Point(x_delta, y_pos - 1)))
        place_piece(board, piece, Point(x_delta, y_pos - 1), "#")

        rock_count += 1

    DST_ROCK = 1000000000000
    print(f"Computing height of rock {DST_ROCK}...")
    result = cycle_heights[cycle_start_count]
    repeats, remainder = divmod(DST_ROCK - cycle_start_count, cycle_repeat_period)
    print("divmod", repeats, remainder)
    result += repeats * cycle_growth_height
    result += (
        cycle_heights[remainder + cycle_start_count] - cycle_heights[cycle_start_count]
    )
    print(result)


main()
