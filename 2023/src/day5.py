from __future__ import annotations

import helpers

import itertools
import collections
import re

import multiprocessing

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

def backwards_find_path(paths, loc):
    cur = loc
    global path
    map_order = reversed(list(zip(path[:-1], path[1:])))
    for f, t in map_order:
        cur_path = paths[(f, t)]
        for segment in cur_path:
            (dst0, dst1), (src0, src1) = segment
            if dst0 <= cur <= dst1:
                cur = src0 + cur - dst0
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

    print('ttt', find_path(dicts, 897591494))
    print('ttt', find_path(dicts, 897591494-100))

    seed_ranges = [ (s[0], s[0] + s[1] - 1) for s in zip(seeds[::2], seeds[1::2]) ]

    def worker(num_workers, offset):
        i = offset
        while i < seed_ranges[-1][0] + seed_ranges[-1][1]:
            if i % 100000 == offset:
                print(f'checking for seed {i}')
            maybe_seed = backwards_find_path(dicts, i)
            for seed_range in seed_ranges:
                if seed_range[0] <= maybe_seed < seed_range[1]:
                    print(f"{i} {maybe_seed} {backwards_find_path(dicts, i)}")
                    return
            i += num_workers

    pool_size = 64
    w = []
    for i in range(pool_size):
        p = multiprocessing.Process(target=worker, args=(pool_size, i))
        p.start()
        w.append(p)
    for x in w:
        x.join()

main()
