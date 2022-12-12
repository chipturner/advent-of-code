from __future__ import annotations

import sys
import re
import math

from typing import List

from dataclasses import dataclass

monkey_fmt = r"""Monkey (?P<num>\d+):
  Starting items: (?P<items>.*)
  Operation: new = (?P<operation>.*)
  Test: divisible by (?P<divisor>\d+)
    If true: throw to monkey (?P<target_true>\d+)
    If false: throw to monkey (?P<target_false>\d+)
""".strip()
monkey_re = re.compile(monkey_fmt, re.MULTILINE)


@dataclass
class Monkey:
    number: int
    operation: str
    divisor: int
    items: List[int]
    target_true: int
    target_false: int
    inspections: int = 0


def main() -> None:
    input_monkeys = sys.stdin.read()
    results = monkey_re.finditer(input_monkeys.strip())

    monkeys = []
    for result in results:
        print(result)
        monkey = Monkey(
            int(result["num"]),
            result["operation"],
            int(result["divisor"]),
            list(int(v) for v in result["items"].split(", ")),
            int(result["target_true"]),
            int(result["target_false"]),
        )
        # monkey.operation = f'(({monkey.operation}) % {monkey.divisor})'
        print(monkey)
        monkeys.append(monkey)
    modulo_reduction = math.lcm(*[monkey.divisor for monkey in monkeys])

    for turn in range(1, 10001):
        for monkey in monkeys:
            while monkey.items:
                monkey.inspections += 1
                item = monkey.items.pop(0)
                l = dict(old=item)
                exec(f"new = ({monkey.operation})", None, l)
                new = l["new"]
                if (new % monkey.divisor) == 0:
                    dest = monkey.target_true
                else:
                    dest = monkey.target_false
                new = new % modulo_reduction
                monkeys[dest].items.append(new)
        print(f"Round {turn}")
        for monkey in monkeys:
            print(
                f"Monkey {monkey.number} inspected items {monkey.inspections} times has {len(monkey.items)} items"
            )
    business = sorted([monkey.inspections for monkey in monkeys], reverse=True)
    print(business[0] * business[1])


main()
