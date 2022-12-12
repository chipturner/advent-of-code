from __future__ import annotations

import heapq
import helpers
import sys

import itertools
import collections

def height_diff(c1, c2):
    remap = { 'S': 'a', 'E': 'z' }
    c1 = remap.get(c1, c1)
    c2 = remap.get(c2, c2)
    return ord(c2) - ord(c1)

def closest(g):
    l = sorted([ (dist, n) for n, dist in g.items() ])
    return l[0][1]

def main() -> None:
    grid = helpers.read_input_digit_grid(str)
    start, end = None, None
    edges = collections.defaultdict(list)
    distances = {}
    prev = {}

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            distances[(i, j)] = sys.maxsize
            prev[(i, j)] = None
            
            if grid[i, j] == 'S':
                start = (i, j)
            elif grid[i, j] == 'E':
                end = (i, j)
            for neighbor in helpers.neighbors(grid, i, j):
                if height_diff(grid[i, j], grid[neighbor]) < 2:
                    print('ddd', grid[i, j], grid[neighbor])
                    edges[(i, j)].append(neighbor)

    distances[start] = 0
    unvisited = distances.copy()

    while unvisited:
        u = closest(unvisited)
        del unvisited[u]

        for neighbor in edges[u]:
            dist = distances[u] + 1
            if dist < distances[neighbor]:
                distances[neighbor] = dist
                prev[neighbor] = u
                unvisited[neighbor] = dist
    print(distances[end])


main()
