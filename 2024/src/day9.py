from __future__ import annotations

import helpers

import itertools
import collections
import re


def main() -> None:
    lines = helpers.read_input()
    block_spaces = [ int(v) for v in lines[0]]
    blocks, spaces = block_spaces[0::2], block_spaces[1::2]
    spaces.append(0)
    block_layout = []
    block_id_map = []
    for idx in range(len(blocks)):
        block_layout += [str(idx)] * blocks[idx]
        block_layout += ['.'] * spaces[idx]
        block_id_map += [idx] * blocks[idx] + [0] * spaces[idx]
    print(''.join(block_layout))
    block_id_map.extend([0] * len(block_layout))
    print(block_id_map)

    write_pt = 0
    read_pt = len(block_layout) - 1

    new_block_id_map = list(block_id_map)
    while write_pt < read_pt:
        if block_layout[write_pt] != '.':
            write_pt += 1
            continue
        if block_layout[read_pt] == '.':
            read_pt -= 1
            continue
        block_layout[write_pt] = block_layout[read_pt]
        block_layout[read_pt] = '.'
        new_block_id_map[write_pt] = block_id_map[read_pt]
        new_block_id_map[read_pt] = 0
        read_pt -= 1
        write_pt += 1
        # print(''.join(block_layout))

    print(sum(idx * v for idx, v in enumerate(new_block_id_map)))
main()
