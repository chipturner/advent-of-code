from __future__ import annotations

import helpers


def main() -> None:
    lines = helpers.read_input()
    pending_adds = []
    x = 1
    cycle = 0
    instructions = lines
    while instructions:
        cycle += 1

        next_instruction = instructions.pop(0)
        s = next_instruction.split()
        if len(pending_adds):
            x += pending_adds.pop(0)
        sprite_center = (cycle - 1) % 40
        if x - 1 <= sprite_center <= x + 1:
            print("#", end="")
        else:
            print(".", end="")
        if cycle % 40 == 0:
            print()
        if s[0] == "noop":
            continue
        else:
            assert s[0] == "addx"
            pending_adds.extend((0, int(s[1])))
            instructions.insert(0, "noop")


main()
