from __future__ import annotations

import helpers

import itertools
import collections
import re
from dataclasses import dataclass

@dataclass
class Block:
    file_id: Optional[int]
    offset: int
    size: int

def main() -> None:
    lines = helpers.read_input()
    block_spaces = [ int(v) for v in lines[0]]
    print(block_spaces)
    blocks, spaces = block_spaces[0::2], block_spaces[1::2]
    spaces.append(0)
    l = []
    cur_offset = 0
    for idx in range(len(blocks)):
        b = Block(idx, cur_offset, blocks[idx])
        cur_offset += b.size
        l.append(b)
        b = Block(None, cur_offset, spaces[idx])
        cur_offset += b.size
        l.append(b)

    

main()
