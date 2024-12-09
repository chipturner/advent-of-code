from __future__ import annotations

import helpers

import itertools
import collections
import re

def contiguous_size(block_layout, pt, direction):
    orig_pt = pt
    orig_id = block_layout[pt]
    while 0 <= pt < len(block_layout) and orig_id == block_layout[pt]:
        pt += direction
    return abs(pt - orig_pt)

def file_size(block_layout, pt):
    file_ch = block_layout[pt]
    orig_pt = pt
    while pt < len(block_layout):
        pt += 1
    return pt - orig_pt

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
    size_to_move = contiguous_size(new_block_id_map, read_pt, -1)

    while read_pt > 0:
        size_to_move = contiguous_size(new_block_id_map, read_pt, -1)
        print('considering moving size ', size_to_move, 'at pt ', read_pt)
        #print('before', ''.join(block_layout))
        for write_pt in range(read_pt):
            if block_layout[write_pt] == '.' and contiguous_size(new_block_id_map, write_pt, 1) >= size_to_move:
                for _ in range(size_to_move):
                    block_layout[write_pt] = block_layout[read_pt]
                    block_layout[read_pt] = '.'
                    new_block_id_map[write_pt] = block_id_map[read_pt]
                    new_block_id_map[read_pt] = 0
                    read_pt -= 1
                    write_pt += 1
                break
        else:
            read_pt -= size_to_move
        #print('after ', ''.join(block_layout))

    print(sum(idx * v for idx, v in enumerate(new_block_id_map)))
main()
