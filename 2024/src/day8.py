from __future__ import annotations

import helpers

import itertools
import collections
import re


def main() -> None:
    grid = helpers.Grid.from_list_of_strings(helpers.read_input())
    grid.print()

    antennas = collections.defaultdict(set)
    for pos, ch in grid.items():
        if ch != '.':
            antennas[ch].add(pos)

    print(antennas)

    antinodes = set()
    for ch, locations in antennas.items():
        for location_tuple in itertools.combinations(locations, 2):
            delta = location_tuple[0] - location_tuple[1]
            p1 = location_tuple[0] + delta
            p2 = location_tuple[1] - delta
            if grid.in_bounds(p1):
                antinodes.add(p1)
            if grid.in_bounds(p2):
                antinodes.add(p2)
    print('anti', len(antinodes))


main()
