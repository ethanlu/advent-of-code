from __future__ import annotations
from adventofcode.common import Solution
from typing import Dict


class Day10(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._input = sorted([int(line) for line in self._load_input_as_lines()])

    def part_one(self):
        differences = {1: 0, 2: 0, 3: 1}
        current = 0
        for adapter in self._input:
            diff = adapter - current
            if diff > 3 or diff < 1:
                raise Exception(f"Unexpected adapter difference between {adapter} and {current}")
            differences[diff] += 1
            current = adapter

        print(differences)

        return differences[1] * differences[3]

    def part_two(self):
        combinations: Dict[int, int] = {0: 1}
        for n in (self._input + [self._input[-1] + 3]):
            combinations[n] = 0
            if (n - 3) in combinations.keys():
                combinations[n] += combinations[n - 3]
            if (n - 2) in combinations.keys():
                combinations[n] += combinations[n - 2]
            if (n - 1) in combinations.keys():
                combinations[n] += combinations[n - 1]

        return combinations[self._input[-1] + 3]
