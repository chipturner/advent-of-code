from __future__ import annotations

import helpers

import itertools
import collections

words = list(enumerate("one two three four five six seven eight nine".split()))


def main() -> None:
    lines = helpers.read_input()
    vals = []
    for line in lines:
        nums = []
        for idx in range(len(line)):
            for val_m_1, word in words:
                str_val = str(val_m_1 + 1)
                if line[idx : idx + len(word)] == word:
                    nums.append(str_val)
                if line[idx] == str_val:
                    nums.append(str(val_m_1 + 1))
        print(line, nums)
        val = int(nums[0] + nums[-1])
        vals.append(val)
    print(vals)
    print(sum(vals))


main()
