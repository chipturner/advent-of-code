from __future__ import annotations

import helpers

import itertools
import collections
import re


def main() -> None:
    lines = helpers.read_input()
    block_spaces = [ int(v) for v in lines[0]]
    print(block_spaces)
    blocks, spaces = block_spaces[0::2], block_spaces[1::2]
    print(blocks, spaces)
    block_initial_offset = dict()

    cur_offset = 0
    space_indexes = []
    for idx, (block, space) in enumerate(zip(blocks, spaces)):
        block_initial_offset[idx] = cur_offset
        cur_offset += block
        for i in range(space):
            space_indexes.append(cur_offset)
            cur_offset += 1
    print(block_initial_offset)

    s_iter = iter(spaces)
    s_idx_iter = iter(space_indexes)
    b_iter = reversed(list(enumerate(blocks)))

    total = 0
    avail = next(s_iter)

    try:
        for b_idx, b_size in b_iter:
            while b_size > 0:
                while avail > 0:
                    avail -= 1
                    b_size -= 1
                    blocks[b_idx] = b_size
                    avail_idx = next(s_idx_iter)
                    total += b_idx * avail_idx
                    print(f'putting file id {b_idx} into avail idx {avail_idx}')
                if avail == 0:
                    avail = next(s_iter)
    except StopIteration:
        pass
    for b_idx, b_size in b_iter:
        total += sum(b_idx * i for i in range(block_initial_offset[b_idx], block_initial_offset[b_idx] + b_size))
    print(total)

main()
