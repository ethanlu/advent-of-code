from __future__ import annotations
from adventofcode.common import Solution
from itertools import combinations


class Day01(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._input = [int(line) for line in self._load_input_as_lines()]

    def part_one(self):
        for a, b in combinations(self._input, 2):
            if a + b == 2020:
                return a * b
        return "ᕕ( ᐛ )ᕗ"

    def part_two(self):
        for a, b, c in combinations(self._input, 3):
            if a + b + c == 2020:
                return a * b * c
        return "ᕕ( ᐛ )ᕗ"
