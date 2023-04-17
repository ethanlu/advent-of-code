from __future__ import annotations
from adventofcode.common import Solution
from collections import deque
from typing import List


class XMAS(object):
    def __init__(self, sequence: List[int]):
        self._sequence = sequence

    def find_invalid(self, size) -> int:
        queue = self._sequence[0:size]
        for next_number in self._sequence[size:]:
            lookup = set(queue)

            for x in queue:
                if (next_number - x) in lookup:
                    break
            else:
                return next_number
            queue = queue[1:] + [next_number]

    def find_subsequence(self, invalid: int) -> List[int]:
        subsequence = deque(self._sequence[0:2])
        total = sum(subsequence)
        for n in self._sequence:
            total += n
            while total > invalid and len(subsequence) > 2:
                x = subsequence.popleft()
                total -= x
            subsequence.append(n)
            if total == invalid:
                return list(subsequence)
            if len(subsequence) <= 2:
                return []


class Day09(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._input = [int(line) for line in self._load_input_as_lines()]

    def part_one(self):
        x = XMAS(self._input)

        return x.find_invalid(25)

    def part_two(self):
        x = XMAS(self._input)
        ss = x.find_subsequence(x.find_invalid(25))

        return min(ss) + max(ss)
