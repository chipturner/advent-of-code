import helpers

import itertools
import collections

from enum import Enum

class Move(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

    def beater(m):
        if m == Move.ROCK:
            return Move.SCISSORS
        if m == Move.PAPER:
            return Move.ROCK
        if m == Move.SCISSORS:
            return Move.PAPER

    def loser(m):
        if m == Move.ROCK:
            return Move.PAPER
        if m == Move.PAPER:
            return Move.SCISSORS
        if m == Move.SCISSORS:
            return Move.ROCK

    def score(m1, m2):
        if m1 == m2:
            return 3
        if Move.beater(m1) == m2:
            return 6
        return 0

def main() -> None:
    for v in (Move.ROCK, Move.PAPER, Move.SCISSORS):
        assert Move.beater(Move.beater(Move.beater(v))) == v
        assert Move.loser(Move.loser(Move.loser(v))) == v
    lines = helpers.read_input()
    mapping = {'A': Move.ROCK, 'B': Move.PAPER, 'C': Move.SCISSORS}
    outcomes = {'X': 'lose', 'Y': 'draw', 'Z': 'win' }
    score = 0
    for l1, l2 in [ l.split() for l in lines ]:
        opponent_play, result_needed = Move(mapping[l1]), outcomes[l2]
        if result_needed == 'draw':
            self_play = opponent_play
        elif result_needed == 'win':
            self_play = Move.loser(opponent_play)
        else:
            self_play = Move.beater(opponent_play)
            
        v = Move.score(self_play, opponent_play) + self_play.value
        score += v
        print(f"{result_needed} {opponent_play} {self_play} -> {v} (tot {score})")
    print(score)



main()
