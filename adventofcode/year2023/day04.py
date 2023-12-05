from __future__ import annotations
from adventofcode.common import Solution
from typing import Set, Tuple


class ScratchOffCard(object):
    def __init__(self, s: str):
        t = s.split(':')
        n = t[1].split(' | ')
        self._card = int(t[0][5:])
        self._winning = set(int(n) for n in n[0].strip().split(' ') if n != '')
        self._picks = set(int(n) for n in n[1].strip().split(' ') if n != '')
        self._winners = self._winning.intersection(self._picks)

    @property
    def card(self) -> int:
        return self._card

    @property
    def winners(self) -> Tuple[int]:
        return tuple(self._winners)

    @property
    def score(self) -> int:
        c = len(self._winners)
        if c > 1:
            return pow(2, c - 1)
        else:
            return c

class Day04(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._cards = [ScratchOffCard(l) for l in self._load_input_as_lines()]

    def part_one(self):
        total = 0
        for c in self._cards:
            print(f"# {c.card} => score {c.score} with {c.winners}")
            total += c.score
        return total

    def part_two(self):
        copies = [1] * len(self._cards)
        for c in self._cards:
            for j in range(len(c.winners)):
                copies[c.card + j] += copies[c.card - 1]

        print(f"copies : {copies}")
        return sum(copies)
