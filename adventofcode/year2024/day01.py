from __future__ import annotations
from adventofcode.common import Solution
from functools import reduce


class Day01(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._left = []
        self._right = []
        for i in self._load_input_as_lines():
            l, r = i.split('   ')
            self._left.append(int(l))
            self._right.append(int(r))

    def part_one(self):
        return reduce(lambda t, p: t + abs(p[0] - p[1]), zip(sorted(self._left), sorted(self._right)), 0)

    def part_two(self):
        score = 0
        tallied = {}
        for i in self._left:
            if i not in tallied:
                tallied[i] = i * reduce(lambda t, c: t + (1 if i == c else 0), self._right, 0)
            score += tallied[i]
        return score
