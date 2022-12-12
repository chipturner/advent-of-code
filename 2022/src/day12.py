from __future__ import annotations

import helpers
import sys

import collections


def height_diff(c1, c2):
    remap = {"S": "a", "E": "z"}
    c1 = remap.get(c1, c1)
    c2 = remap.get(c2, c2)
    return ord(c2) - ord(c1)


def closest(g):
    min_dist = sys.maxsize
    min_node = None
    for n, dist in g.items():
        if dist < min_dist:
            min_dist = dist
            min_node = n
    return min_node


def main() -> None:
    grid = helpers.read_input_digit_grid(str)
    starting_spots = []
    end = None, None
    edges = collections.defaultdict(list)
    prev = {}

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            prev[(i, j)] = None

            if grid[i, j] == "S" or grid[i, j] == "a":
                starting_spots.append((i, j))
            elif grid[i, j] == "E":
                end = (i, j)
            for neighbor in helpers.neighbors(grid, i, j):
                if height_diff(grid[i, j], grid[neighbor]) < 2:
                    edges[(i, j)].append(neighbor)

    print(len(starting_spots))
    for start in starting_spots:
        distances = {}
        for n in prev:
            distances[n] = sys.maxsize
        distances[start] = 0
        unvisited = distances.copy()

        while (u := closest(unvisited)) != None:
            del unvisited[u]

            for neighbor in edges[u]:
                dist = distances[u] + 1
                if dist < distances[neighbor]:
                    distances[neighbor] = dist
                    prev[neighbor] = u
                    unvisited[neighbor] = dist
        print(start, distances[end])


main()
