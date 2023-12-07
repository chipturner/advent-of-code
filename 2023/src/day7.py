from __future__ import annotations

import helpers

import functools
import itertools
import collections
import re

strengths = {c: 14 - idx for idx, c in enumerate("AKQJT987654321")}
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
            return 0xff000000
        if count == 4:
            return 0xee000000
        if count == 3 and any(other_count == 2 for other_card, other_count in occurs.items() if other_card != card):
            return 0xdd000000
        if count == 3:
            return 0xcc000000

    for card, count in occurs.items():
        if count == 2 and any(other_count == 2 for other_card, other_count in occurs.items() if other_card != card):
            return 0xbb000000
        if count == 2:
            return 0xaa000000

    return 0xf000000


@functools.cache
def rank_hand(hand):
    ret = rank_hand_inner(hand) << 32
    for idx, ch in enumerate(hand):
        ret |= strengths[ch] << 4 * (4-idx)
    return ret


def cmp_card_values(hand1, hand2):
    for c1, c2 in zip(hand1, hand2):
        if strengths[c1] > strengths[c2]:
            return -1
        elif strengths[c1] < strengths[c2]:
            return 1
    return 0


def cmp_hands(hand1, hand2):
    return cmp(rank_hand(hand2), rank_hand(hand1))

t1, t2 = '12345 12345'.split()
print(t1, t2)
print(f'{rank_hand(t1):#018x} {rank_hand(t2):#018x}')
print(cmp_hands(t1, t2))
print(cmp_card_values(t1, t2))


def main() -> None:
    lines = helpers.read_input()
    hands = {}
    for line in lines:
        hand, bid = line.split()
        hands[hand] = bid

    tot = 0
    for idx, hand in enumerate(sorted(hands, key=functools.cmp_to_key(cmp_hands))):
        value = len(hands) - idx
        print(f'{hand} {rank_hand(hand):#018x} bid {hands[hand]}')
        tot += int(hands[hand]) * value
    print(tot)


main()
