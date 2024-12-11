from __future__ import annotations

import helpers

import more_itertools
import itertools
import collections
import re
import functools

def single_blink(stone):
    if stone == '0':
        return ['1']

    if len(stone) % 2 == 0:
        return [str(int(v)) for v in (stone[:len(stone)//2], stone[len(stone)//2:])]

    return [str(int(stone) * 2024)]

def blink_all(num_blinks, stones):
    for i in range(num_blinks):
        stones = list(more_itertools.flatten(single_blink(stone) for stone in stones))
    return stones

@functools.lru_cache(maxsize=None)
def count_stones(num_blinks, stones):
    if num_blinks == 1:
        return len(stones)
    blinked = tuple(single_blink(s) for s in stones)
    return sum(count_stones(num_blinks - 1, tuple(s)) for s in blinked)

def main() -> None:
    lines = helpers.read_input()
    stones = tuple(lines[0].split(' '))
    for bn in range(1, 100):
        res = count_stones(bn, stones)
        print(bn-1, res)
    print(len(res))
main()
