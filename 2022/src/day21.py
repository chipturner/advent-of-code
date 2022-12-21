from __future__ import annotations

import helpers

import itertools
import collections

from pprint import pprint


def expand(d, node):
    if node == "humn":
        return [node]
    todo = d[node]
    if type(todo) == list:
        assert len(todo) == 3
        return [expand(d, todo[0]), todo[1], expand(d, todo[2])]
    else:
        return [todo]


def eval_tree(node):
    if type(node) == int:
        return node
    assert len(node) in (1, 3)
    if len(node) == 1:
        return node[0]
    else:
        lhs, rhs = eval_tree(node[0]), eval_tree(node[2])
        op = node[1]
        to_eval = f"{lhs} {op} {rhs}"
        print("will eval", to_eval)
        return eval(to_eval, None, None)


def has_human(node):
    print("checking", node)
    if type(node) == list:
        for n in node:
            if has_human(n):
                return True
    return node == "humn"


opposite = {"+": "-", "-": "+", "*": "/", "/": "*"}


def main() -> None:
    lines = helpers.read_input()

    d = dict()
    for line in lines:
        lhs, rhs = line.split(": ")
        rhs = rhs.split()
        if len(rhs) == 1:
            rhs = int(rhs[0])
        d[lhs] = rhs

    del d["humn"]
    expression = expand(d, "root")
    print(expression)

    top = expression
    other_side = [0]
    while "humn" not in top:
        print("considering", top[0], "and", top[2])
        if has_human(top[0]):
            assert not has_human(top[2])
            human_idx, numeric_idx = 0, 2
        else:
            assert not has_human(top[0])
            human_idx, numeric_idx = 2, 0

        other_side = [other_side, opposite[top[1]], top[numeric_idx]]
        top = top[human_idx]
        print("top", top)
        print("other", other_side)
    print(top)
    print(other_side)
    print(eval_tree(other_side))


main()
