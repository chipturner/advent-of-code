from __future__ import annotations

import helpers

import itertools
import collections
import re

def delta(nums):
    return [ v1 - v0 for v0, v1 in zip(nums[:-1], nums[1:]) ]

def main() -> None:
    lines = [ list(map(int, l.split())) for l in helpers.read_input() ]

    s = 0
    out_seqs = []
    for nums in lines:
        nums_seq = [nums]
        while any(v != 0 for v in nums):
            nums = delta(nums)
            nums_seq.append(nums)

        nums_seq.reverse()
        nums_seq[0].append(0)
        for idx in range(len(nums_seq) - 1):
            last_delta = nums_seq[idx][0]
            nums_seq[idx + 1].insert(0, (nums_seq[idx + 1][0] - last_delta))
        print(nums_seq)
        out_seqs.append(nums_seq)
    print()
    print(list(v[-1] for v in out_seqs))
    print(sum(v[-1][0] for v in out_seqs))


main()
