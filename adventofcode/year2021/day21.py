from __future__ import annotations
from adventofcode.common import Solution
from collections import Counter
from functools import cache
from itertools import cycle, product
from typing import Iterable, List, Tuple


class DeterministicDice(object):
    def __init__(self):
        self._die = cycle(range(1, 101, 1))
        self._rolls = 0

    @property
    def rolls(self) -> int:
        return self._rolls

    def roll(self) -> Tuple[int, int, int]:
        self._rolls += 3
        return next(self._die), next(self._die), next(self._die)


class DiracDice(object):
    def __init__(self):
        self._outcomes = Counter()
        for roll in product((1, 2, 3), repeat=3):
            s = sum(roll)
            self._outcomes[s] += 1

    def rolls(self) -> Iterable[Tuple[int, int]]:
        for roll, repeat in self._outcomes.items():
            yield roll, repeat


class ScoreBoard(object):
    def __init__(self, positions: List[int], scores: List[int], turn: int):
        self._positions = positions
        self._scores = scores
        self._turn = turn

    def __hash__(self):
        return hash((self._positions[0], self._positions[1], self._scores[0], self._scores[1], self._turn))

    def __eq__(self, other):
        return self._positions == other.positions and self._scores == other.scores and self._turn == other.turn if issubclass(type(other), ScoreBoard) else False

    @property
    def positions(self) -> List[int]:
        return self._positions

    @property
    def scores(self) -> List[int]:
        return self._scores

    @property
    def turn(self) -> int:
        return self._turn

    def next_turn(self) -> int:
        t = self._turn
        self._turn = (self._turn + 1) % 2
        return t

    def move(self, steps: int):
        player = self._turn
        position = (self._positions[player] + steps) % 10
        self._positions[player] = 10 if position == 0 else position
        self._scores[player] += self._positions[player]
        self._turn = (self._turn + 1) % 2

    def has_winner(self, threshold: int) -> bool:
        return any((s >= threshold for s in self._scores))


class Day21(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        data = self._load_input_as_lines()
        self._positions = int(data[0].split(' ')[-1]), int(data[1].split(' ')[-1])

    def part_one(self):
        sb = ScoreBoard([p for p in self._positions], [0, 0], 0)
        dd = DeterministicDice()
        threshold = 1000
        while not sb.has_winner(threshold):
            sb.move(sum(dd.roll()))
        match sb.scores[0] >= threshold, sb.scores[1] >= threshold:
            case True, False:
                print(f"player 1 won with {sb.scores[0]} after {dd.rolls} rolls. player 2 lost with score of {sb.scores[1]}.")
                loser = sb.scores[1]
            case False, True:
                print(f"player 2 won with {sb.scores[1]} after {dd.rolls} rolls. player 1 lost with score of {sb.scores[0]}.")
                loser = sb.scores[0]
            case _:
                raise Exception(f"unexpected game outcome : p1={sb.scores[0]}, p2={sb.scores[1]}")
        return loser * dd.rolls

    def part_two(self):
        @cache
        def play(sb: ScoreBoard) -> Tuple[int, int]:
            if sb.has_winner(threshold):
                match sb.scores[0] >= threshold, sb.scores[1] >= threshold:
                    case True, False:
                        return 1, 0
                    case False, True:
                        return 0, 1
                    case _:
                        raise Exception(f"unexpected game outcome : p1={sb.scores[0]}, p2={sb.scores[1]}")
            running_score = 0, 0
            for (steps, repeated) in dd.rolls():
                nsb = ScoreBoard([p for p in sb.positions], [s for s in sb.scores], sb.turn)
                nsb.move(steps)
                running_score = tuple(sum(n) for n in zip(running_score, (s * repeated for s in play(nsb))))
            return running_score
        threshold = 21
        dd = DiracDice()
        scores = play(ScoreBoard([p for p in self._positions], [0, 0], 0))
        print(f"scores : {scores}")
        return max(scores)
