from __future__ import annotations

import helpers

import itertools
import collections


def main() -> None:
    lines = helpers.read_input()
    pending_adds = []
    x = 1
    strength_sum = 0
    cycle_signals = dict()
    cycle = 0
    instructions = lines
    while instructions:
        cycle += 1
        next_instruction = instructions.pop(0)
        s = next_instruction.split()
        if len(pending_adds):
            x += pending_adds.pop(0)
        strength = x * cycle
        cycle_signals[cycle] = strength
        print(cycle, x)
        if s[0] == 'noop':
            continue
        else:
            assert s[0] == 'addx'
            pending_adds.extend((0, int(s[1])))
            instructions.insert(0, 'noop')
            
    interesting = [ 20, 60, 100, 140, 180, 220 ]
    print(sum(cycle_signals[i] for i in interesting))


main()
