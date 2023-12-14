from __future__ import annotations

import helpers

import functools
import itertools
import collections
import re


def tprint(*args):
    pass


@functools.lru_cache
def count_matches(state, blocks):
    tprint("cm", state, blocks)
    if not blocks:
        if "#" in state:
            return 0
        else:
            return 1
    while state and state[0] == ".":
        state = state[1:]
    if not state:
        return 0

    ret = 0
    if state[0] == "?":
        # dot case
        ret += count_matches(state[1:], blocks)

    block_remaining = blocks[0]
    if len(state) < block_remaining:
        tprint("shorty")
        return ret
    if "." in state[:block_remaining]:
        tprint("gap")
        return ret
    if block_remaining < len(state) and state[block_remaining] == "#":
        tprint("stringy", block_remaining, state, state[block_remaining])
        return ret
    tprint("chomping", state, blocks)
    ret += count_matches(state[block_remaining + 1 :], blocks[1:])

    return ret


def main() -> None:
    s = 0
    for state, blocks in helpers.read_input_split():
        blocks = [int(i) for i in blocks.split(",")] * 5
        state = "?".join((state, state, state, state, state))
        m = count_matches(state, tuple(blocks))
        print("RES", state, blocks, m)
        s += m
    print(s)


main()
