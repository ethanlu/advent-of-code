from __future__ import annotations
from adventofcode.common import Solution
from typing import List
from functools import cache


class Day06(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._fishes = [int(f) for f in self._load_input_as_string().split(',')]

    def part_one(self):
        def step(fishes: List[int]) -> List[int]:
            next_fishes = []
            new_fishes = []
            for fish in fishes:
                match fish:
                    case 0:
                        new_fishes.append(8)
                        next_fishes.append(6)
                    case _:
                        next_fishes.append(fish - 1)
            return next_fishes + new_fishes
        current = self._fishes
        for c in range(80):
            current = step(current)
        return len(current)

    def part_two(self):
        @cache
        def steps(fish: int, amount: int) -> int:
            if amount == 0 or fish > amount:
                return 0
            new_fish = 0
            amount_left = amount - fish
            while amount_left > 0:
                new_fish += 1
                new_fish += steps(9, amount_left)
                amount_left -= 7
            return new_fish
        total = len(self._fishes)
        for fish in self._fishes:
            total += steps(fish, 256)
        return total
