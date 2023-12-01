from __future__ import annotations
from adventofcode.common import Solution

import re


class Day01(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._input = self._load_input_as_lines()

    def part_one(self):
        calibration = 0
        for s in self._input:
            digits = [c for c in s if re.match(r"\d", c)]
            if digits:
                calibration += int(f"{digits[0]}{digits[-1]}")
        return calibration

    def part_two(self):
        numbers = ('one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine')

        calibration = 0
        for s in self._input:
            first_number_index = len(s)
            first_number = 0

            last_number_index = -1
            last_number = 0

            for i, n in enumerate(numbers):
                j = s.find(n)
                if j != -1 and j < first_number_index:
                    first_number_index = j
                    first_number = i + 1

                j = s.rfind(n)
                if j != -1 and j > last_number_index:
                    last_number_index = j
                    last_number = i + 1

            digits = [(i, c) for i, c in enumerate(s) if re.match(r"\d", c)]
            if digits:
                if digits[0][0] < first_number_index:
                    first_number = digits[0][1]
                if digits[-1][0] > last_number_index:
                    last_number = digits[-1][1]

            #print(f"{s} -> {first_number}{last_number}")
            calibration += int(f"{first_number}{last_number}")

        return calibration
