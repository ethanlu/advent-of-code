from __future__ import annotations
from adventofcode.common import Solution
from itertools import pairwise


class Day01(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._readings = [int(line) for line in self._load_input_as_lines()]

    def part_one(self):
        return sum([r1 < r2 for r1, r2 in pairwise(self._readings)])

    def part_two(self):
        def triplewise(iterable):
            # https://docs.python.org/3.11/library/itertools.html#itertools-recipes
            for (a, _), (b, c) in pairwise(pairwise(iterable)):
                yield a, b, c
        return sum([sum(b1) < sum(b2) for b1, b2 in pairwise(triplewise(self._readings)) if len(b1) == 3 and len(b2) == 3])
