import helpers

import itertools
import collections


def priority(ch):
    if "a" <= ch <= "z":
        return ord(ch) - ord("a") + 1
    else:
        return ord(ch) - ord("A") + 27


def main() -> None:
    lines = helpers.read_input()
    elf_teams = []
    current_team = []
    for sack in lines:
        if len(current_team) == 3:
            elf_teams.append(current_team)
            current_team = []
        current_team.append(set(sack))
    elf_teams.append(current_team)

    tot = 0
    for team in elf_teams:
        common = team[0].intersection(team[1]).intersection(team[2])
        print(common)
        assert len(common) == 1
        tot += priority(next(iter(common)))
    print(tot)


main()
