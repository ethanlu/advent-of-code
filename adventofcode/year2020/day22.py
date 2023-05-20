from __future__ import annotations
from adventofcode.common import Solution
from collections import deque
from functools import reduce
from typing import List, Set


class Deck(object):
    def __init__(self, cards: List[int]):
        self._cards = deque(cards)

    @property
    def cards(self) -> List[int]:
        return list(self._cards)

    @property
    def size(self) -> int:
        return len(self._cards)

    @property
    def score(self) -> int:
        return reduce(lambda acc, p: acc + ((p[0] + 1) * p[1]), enumerate(reversed(self._cards)), 0)

    @property
    def fingerprint(self) -> str:
        return ".".join((str(c) for c in self._cards))

    def add(self, card: int) -> Deck:
        self._cards.append(card)
        return self

    def top(self) -> int:
        return self._cards.popleft()


class Combat(object):
    def __init__(self, p1: Deck, p2: Deck):
        self._p1 = p1
        self._p2 = p2

    @property
    def winner(self) -> int:
        return 1 if self._p1.size > 0 else 2

    @property
    def score(self) -> int:
        return self._p1.score if self._p1.size > 0 else self._p2.score

    def play(self) -> None:
        while self._p1.size > 0 and self._p2.size > 0:
            c1 = self._p1.top()
            c2 = self._p2.top()

            if c1 > c2:
                self._p1.add(c1).add(c2)
            else:
                self._p2.add(c2).add(c1)


class RecursiveCombat(Combat):
    def __init__(self, p1: Deck, p2: Deck):
        super().__init__(p1, p2)
        self._history1: Set[str] = set([])
        self._history2: Set[str] = set([])

    def play(self) -> None:
        while self._p1.fingerprint not in self._history1 and self._p2.fingerprint not in self._history2 and self._p1.size > 0 and self._p2.size > 0:
            self._history1.add(self._p1.fingerprint)
            self._history2.add(self._p2.fingerprint)

            c1 = self._p1.top()
            c2 = self._p2.top()

            if self._p1.size >= c1 and self._p2.size >= c2:
                rc = RecursiveCombat(Deck(self._p1.cards[:c1]), Deck(self._p2.cards[:c2]))
                rc.play()
                if rc.winner == 1:
                    self._p1.add(c1).add(c2)
                else:
                    self._p2.add(c2).add(c1)
            else:
                if c1 > c2:
                    self._p1.add(c1).add(c2)
                else:
                    self._p2.add(c2).add(c1)


class Day22(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._deck1 = []
        self._deck2 = []

        player = 0
        for line in self._load_input_as_lines():
            if line.startswith("Player") or not line:
                player += 1
                continue

            if player == 1:
                self._deck1.append(int(line))
            else:
                self._deck2.append(int(line))

    def part_one(self):
        c = Combat(Deck(self._deck1), Deck(self._deck2))
        c.play()

        print(f"player {c.winner} won with score : {c.score}")

        return c.score

    def part_two(self):
        rc = RecursiveCombat(Deck(self._deck1), Deck(self._deck2))
        rc.play()

        print(f"player {rc.winner} won with score : {rc.score}")

        return rc.score
