from __future__ import annotations

import helpers

import itertools
import collections
import re

def blink(stone):
    if stone == '0':
        return ['1']

    if len(stone) % 2 == 0:
        return [str(int(v)) for v in (stone[:len(stone)//2], stone[len(stone)//2:])]

    return [str(int(stone) * 2024)]

def blink_all(stones):
    ret = []
    for stone in stones:
        ret.extend(blink(stone))
    return ret

def main() -> None:
    lines = helpers.read_input()
    stones = lines[0].split(' ')

    for blink in range(27):
        # print('blink', blink, ' '.join(stones))
        print('blink', blink, len(stones))
        stones = blink_all(stones)


main()
