from __future__ import annotations

import helpers

import itertools
import collections


class NumPos:
    def __init__(self, num):
        self.num = num
        self.nxt = None
        self.prv = None

    def __str__(self):
        return f"NumPos({self.num}, {id(self.prv)}, {id(self.nxt)})"

    __repr__ = __str__


def stringify_chain(cursor, num):
    while cursor.num != num:
        cursor = cursor.nxt
    last = cursor.prv
    ret = []
    while cursor != last:
        ret.append(str(cursor.num))
        cursor = cursor.nxt
    ret.append(str(cursor.num))
    return ", ".join(ret)


def move(idx_to_pos, idx):
    cursor = idx_to_pos[idx]
    num = n = cursor.num
    n = n % (len(idx_to_pos) - 1)
    tmp_prv = cursor.prv
    cursor.nxt.prv = cursor.prv
    tmp_prv.nxt = cursor.nxt

    while n > 0:
        cursor = cursor.nxt
        n -= 1
    if n < 0:
        n -= 1
    while n < 0:
        cursor = cursor.prv
        n += 1

    new_node = NumPos(num)
    new_node.prv = cursor
    new_node.nxt = cursor.nxt
    cursor.nxt = new_node
    new_node.nxt.prv = new_node
    idx_to_pos[idx] = new_node


def main() -> None:
    lines = helpers.read_input()
    numbers = list([int(n) * 811589153 for n in lines])

    prv, first, last = None, None, None
    idx_to_pos = {}
    for idx, val in enumerate(numbers):
        numpos = NumPos(val)
        if prv:
            prv.nxt = numpos
        else:
            first = numpos
        numpos.prv = prv
        prv = numpos
        last = numpos
        idx_to_pos[idx] = numpos
    last.nxt = first
    first.prv = last

    for numpos in idx_to_pos.values():
        assert numpos.nxt != None, f"{numpos} has no nxt"
        assert numpos.prv != None, f"{numpos} has no prv"

    # print(idx_to_pos)
    print(stringify_chain(idx_to_pos[0], 0))
    print()

    for i in range(10):
        for idx, n in enumerate(numbers):
            if n == 0:
                continue
            move(idx_to_pos, idx)
        print(stringify_chain(idx_to_pos[0], 0))

    p = idx_to_pos[0]
    while p.num != 0:
        p = p.nxt
    print("zero", p)
    output = 0
    for i in range(3):
        for i in range(1000):
            p = p.nxt
        output += p.num
        print(p)
    print(output)


main()
