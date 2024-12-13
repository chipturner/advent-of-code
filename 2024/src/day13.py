from __future__ import annotations

import helpers

import itertools
import collections
import re

def minimize_press(button_a, button_b, prize):
    solutions = []

    for a_presses in range(1, 101):
        for b_presses in range(1, 101):
            position = (button_a[0] * a_presses + button_b[0] * b_presses,
                        button_a[1] * a_presses + button_b[1] * b_presses)
            if position == prize:
                solutions.append((3*a_presses + b_presses, a_presses, b_presses))
    return solutions

def main() -> None:
    lines = helpers.read_input()
    chunks = [l.split('\n') for l in "\n".join(lines).split("\n\n")]

    machines = []
    for chunk in chunks:
        machines.append([(int(x[0]), int(x[1])) for x in (re.findall(r'\d+', chunk[0]), re.findall(r'\d+', chunk[1]), re.findall(r'\d+', chunk[2]))])

    cost = 0
    for machine in machines:
        presses = minimize_press(*machine)
        if presses:
            print(presses)
            print('ll', len(presses))
            cost += presses[0][0]

    print(cost)

main()
