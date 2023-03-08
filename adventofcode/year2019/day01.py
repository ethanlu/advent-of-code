from __future__ import annotations
from adventofcode.common import Solution


class Day01(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._input = [int(l) for l in self._load_input_as_lines()]

    def part_one(self):
        return sum(module // 3 - 2 for module in self._input)

    def part_two(self):
        total_fuel = 0
        for module in self._input:
            fuel = module // 3 - 2
            while fuel > 0:
                total_fuel += fuel
                fuel = max(0, fuel // 3 - 2)

        return total_fuel
