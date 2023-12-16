from __future__ import annotations

import helpers

import itertools
import collections
import re

def hasher(s):
    val = 0
    for c in s:
        val += ord(c)
        val = val * 17 % 256
    return val

def main() -> None:
    seq = helpers.read_input()[0].split(',')
    print(seq)
    for s in seq:
        print(s, hasher(s))
    print(sum(hasher(s) for s in seq))

    boxes = [[] for i in range(256)]
    for s in seq:
        lens, op = re.match(r'^(\w+)([-=]\d*)$', s).groups()
        box = boxes[hasher(lens)]
        if op == '-':
            box[:] = [ (l, c) for l, c in box if l != lens ]
        else:
            assert op[0] == '='
            val = int(op[-1])
            print(s, lens, op, val)
            for idx, (l, v) in enumerate(box):
                if l == lens:
                    box[idx] = (l, val)
                    break
            else:
                 box.append((lens, val))

    print(boxes)
    tot = 0
    for boxnum, lenses in enumerate(boxes):
        for idx, (l, v) in enumerate(lenses):
            fpow = (boxnum + 1) * (idx + 1) * v
            print(boxnum + 1, idx + 1, v)
            tot += fpow
            print(fpow)
    print(tot)

main()
