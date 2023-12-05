from __future__ import annotations

import helpers

import itertools
import collections
import re

path = "seed soil fertilizer water light temperature humidity location".split()
def find_path(paths, seed):
    #print('find_path', paths, seed)
    cur = seed
    for f, t in zip(path[:-1], path[1:]):
        #print('testing', f, t)
        cur_path = paths[(f, t)]
        #print(f, cur, cur_path)
        for segment in cur_path:
            (dst0, dst1), (src0, src1) = segment
            if src0 <= cur <= src1:
                #print(f'hit: {cur} is in {src0}..{src1} with offset {cur-src0} so result os {dst0 + cur - src0}')
                cur = dst0 + cur - src0
                break
                
    return cur
        
    

def main() -> None:
    lines = helpers.read_input()
    seeds = list(map(int, lines[0].split()[1:]))
    print(seeds)

    idx = 1
    dicts = {}
    cur_list = []
    while idx < len(lines):
        if ':' in lines[idx]:
            m = lines[idx].split()[0]
            f, t = m.split('-to-')
            dicts[(f, t)] = []
            cur_list = dicts[(f, t)]
        elif ' ' in lines[idx]:
            dst, start, rng = map(int, lines[idx].split())
            cur_list.append([(dst, dst + rng - 1), (start, start + rng - 1)])
        idx += 1

    for seed_start, seed_range in zip(seeds[::2], seeds[1::2]):
        for s in range(seed_start, seed_start + seed_range):
            score = find_path(dicts, s)
            print(seed_start, seed_range, score - s, s, score)

main()
