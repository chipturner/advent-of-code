from __future__ import annotations

import heapq
import helpers
import sys

import collections


def height_diff(c1, c2):
    remap = {"S": "a", "E": "z"}
    c1 = remap.get(c1, c1)
    c2 = remap.get(c2, c2)
    return ord(c2) - ord(c1)


def main() -> None:
    grid = helpers.read_input_digit_grid(str)
    starting_spots = []
    nodes = set()
    edges = collections.defaultdict(list)

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            nodes.add((i, j))

            if grid[i, j] == "S" or grid[i, j] == "a":
                starting_spots.append((i, j))
            elif grid[i, j] == "E":
                end = (i, j)
            for neighbor in helpers.neighbors(grid, i, j):
                if height_diff(grid[i, j], grid[neighbor]) < 2:
                    edges[(i, j)].append(neighbor)

    answers = []
    for start in starting_spots:
        horizon = []
        heapq.heappush(horizon, (0, start))

        distances = collections.defaultdict(lambda: sys.maxsize)
        distances[start] = 0

        while horizon and (dist_u := heapq.heappop(horizon)):
            dist, u = dist_u
            if u == end:
                answers.append((dist, start))
                break
            if distances[u] < dist:
                continue
            for neighbor in edges[u]:
                dist = distances[u] + 1
                if dist < distances[neighbor]:
                    heapq.heappush(horizon, (dist, neighbor))
                    distances[neighbor] = dist

    print(sorted(answers)[0][0])


main()
