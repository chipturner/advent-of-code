from __future__ import annotations

import helpers

import itertools
import collections
import re
import numpy as np

def old_minimize_press(button_a, button_b, prize):
    for a_presses in range(1, 101):
        for b_presses in range(1, 101):
            position = [button_a[0] * a_presses + button_b[0] * b_presses,
                        button_a[1] * a_presses + button_b[1] * b_presses]
            if position == prize:
                return a_presses, b_presses

def minimize_press(button_a, button_b, prize):
    a = np.array([button_a, button_b]).T
    b = np.array(prize)
    solution = np.linalg.solve(a, b)
    solution_int = solution.round().astype(int)
    magnitude = np.sum((solution_int - solution)**2)
    if magnitude < 1e-6 and 0 <= solution_int[0] and 0 <= solution_int[1]:
        return int(solution_int[0]), int(solution_int[1])
    else:
        return None

def main() -> None:
    lines = helpers.read_input()
    chunks = [l.split('\n') for l in "\n".join(lines).split("\n\n")]

    machines = []
    for chunk in chunks:
        machines.append([[int(x[0]), int(x[1])] for x in (re.findall(r'\d+', chunk[0]), re.findall(r'\d+', chunk[1]), re.findall(r'\d+', chunk[2]))])
        machines[-1][-1][0] += 10000000000000
        machines[-1][-1][1] += 10000000000000

    cost = 0
    for idx, machine in enumerate(machines):
        presses = minimize_press(*machine)
        if presses:
            cost += 3 * presses[0] + presses[1]

    print(cost)

main()
