from __future__ import annotations

import helpers

import itertools
import collections
import sys
import parse

from dataclasses import dataclass

monkey_fmt = r"""Monkey {num}:
  Starting items: {items}
  Operation: {operation}
  Test: divisible by {divisor}
    If true: throw to monkey {target_true}
    If false: throw to monkey {target_false}
""".strip()


@dataclass
class Monkey:
    number: int
    worry_level: int
    operation: str
    divisor: int
    items: List[int]
    target_true: int
    target_false: int
    inspections: int = 0


def main() -> None:
    input_monkeys = sys.stdin.read()
    monkey_chunks = input_monkeys.split("\n\n")
    print(monkey_chunks)

    monkeys = []
    for chunk in monkey_chunks:
        result = parse.parse(monkey_fmt, chunk.strip())
        monkey = Monkey(
            int(result["num"]),
            0,
            result["operation"],
            int(result["divisor"]),
            list(int(v) for v in result["items"].split(", ")),
            int(result["target_true"]),
            int(result["target_false"]),
        )
        print(monkey)
        monkeys.append(monkey)

    for turn in range(1, 21):
        for monkey in monkeys:
            while monkey.items:
                monkey.inspections += 1
                item = monkey.items.pop(0)
                l = dict(old=item)
                exec(monkey.operation, None, l)
                new = l['new'] // 3
                if (new % monkey.divisor) == 0:
                    dest = monkey.target_true 
                else:
                    dest = monkey.target_false
                print(f'item {item} going to {dest} as {new}')
                monkeys[dest].items.append(new)
        print(monkeys)
    business = sorted([ monkey.inspections for monkey in monkeys ], reverse=True)
    print(business[0] * business[1])
main()
