from __future__ import annotations

import helpers

import itertools
import collections
import re

def card_wins(w, m):
    return len(m.intersection(w))

def main() -> None:
    lines = helpers.read_input()
    print(lines)
    cards = []
    for line in lines:
        m = re.match(r'Card +(\d+): +(.*) +\| +(.*) *$', line)
        card, winners, mine = m.groups()
        cards.append((set(winners.strip().split()), set(mine.strip().split())))
    score = 0
    idx = 0
    card_counts = [1] * len(cards)
    for idx, (w, m) in enumerate(cards):
        wins = card_wins(w, m)
        print(f'card {idx} won {wins} cards ({card_counts})')
        for j in range(wins):
            if idx + j + 1 < len(card_counts):
                card_counts[idx + j + 1] += card_counts[idx]
    print(card_counts)
    print(sum(card_counts))
        


main()
