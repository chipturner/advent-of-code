from __future__ import annotations

import helpers

import functools
import itertools
import collections
import re

strengths = {c: 14 - idx for idx, c in enumerate("AKQT987654321J")}
print(strengths)


def cmp(a, b):
    return (a > b) - (a < b)


@functools.cache
def rank_hand_inner(hand):
    occurs = collections.defaultdict(int)
    for c in hand:
        occurs[c] += 1

    for card, count in occurs.items():
        if count == 5:
            return 0xFF000000
        if count == 4:
            return 0xEE000000
        if count == 3 and any(
            other_count == 2
            for other_card, other_count in occurs.items()
            if other_card != card
        ):
            return 0xDD000000
        if count == 3:
            return 0xCC000000

    for card, count in occurs.items():
        if count == 2 and any(
            other_count == 2
            for other_card, other_count in occurs.items()
            if other_card != card
        ):
            return 0xBB000000
        if count == 2:
            return 0xAA000000

    return 0xF000000


@functools.cache
def rank_hand_middle(hand, orig_hand):
    ret = rank_hand_inner(hand) << 32
    for idx, ch in enumerate(orig_hand):
        ret |= strengths[ch] << 4 * (4 - idx)
    return ret


@functools.cache
def rank_hand(hand, orig_hand=None):
    if orig_hand is None:
        orig_hand = hand

    scores = [rank_hand_middle(hand, orig_hand)]
    for idx, c in enumerate(hand):
        if c == "J":
            for sub in strengths:
                if sub != "J":
                    scores.append(
                        rank_hand(hand[:idx] + sub + hand[idx + 1 :], orig_hand)
                    )
    return max(scores)


def cmp_card_values(hand1, hand2):
    for c1, c2 in zip(hand1, hand2):
        if strengths[c1] > strengths[c2]:
            return -1
        elif strengths[c1] < strengths[c2]:
            return 1
    return 0


def cmp_hands(hand1, hand2):
    return cmp(rank_hand(hand2), rank_hand(hand1))


def main() -> None:
    lines = helpers.read_input()
    hands = {}
    for line in lines:
        hand, bid = line.split()
        hands[hand] = bid

    tot = 0
    for idx, hand in enumerate(sorted(hands, key=functools.cmp_to_key(cmp_hands))):
        value = len(hands) - idx
        print(f"{hand} {rank_hand(hand):#018x} bid {hands[hand]}")
        tot += int(hands[hand]) * value
    print(tot)


main()
