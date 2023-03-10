from __future__ import annotations
from adventofcode.common import Solution


class Day04(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._input = [int(x) for x in self._load_input_as_string().split('-')]

    def part_one(self):
        valid = 0
        for i in range(self._input[0], self._input[1] + 1):
            s = str(i)
            previous = s[0]
            increasing = True
            same = False
            for c in s[1:]:
                increasing = increasing and previous <= c
                same = same or previous == c
                previous = c
            valid += 1 if increasing and same else 0

        return valid

    def part_two(self):
        valid = 0
        for i in range(self._input[0], self._input[1] + 1):
            s = str(i)
            previous = s[0]
            increasing = True
            same = False
            pairs = 0
            for c in s[1:]:
                increasing = increasing and previous <= c
                if previous == c:
                    pairs += 1
                else:
                    same = same or pairs == 1
                    pairs = 0
                previous = c
            same = same or pairs == 1
            valid += 1 if increasing and same else 0

        return valid