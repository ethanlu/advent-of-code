from __future__ import annotations
from adventofcode.common import Solution
from functools import cache
from typing import Tuple


@cache
def find_arrangements(patterns: Tuple[Tuple[int, str]], remaining: str) -> int:
    if not remaining:
        return 1
    arrangements = 0
    for pattern_length, pattern in patterns:
        if pattern == remaining[:pattern_length]:
            arrangements += find_arrangements(patterns, remaining[pattern_length:])
    return arrangements


class Day19(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        data = list(self._load_input_as_lines())
        self._patterns = tuple((len(p), p) for p in list(data[0].split(', ')))
        self._designs = data[2:]

    def part_one(self):
        total = 0
        for design in self._designs:
            possible = find_arrangements(self._patterns, design)
            if possible > 0:
                print(f"{design} is possible")
                total += 1
            else:
                print(f"{design} is impossible")
        return total

    def part_two(self):
        total = 0
        for design in self._designs:
            possible = find_arrangements(self._patterns, design)
            print(f"{design} has {possible} possible arrangements")
            total += possible
        return total
