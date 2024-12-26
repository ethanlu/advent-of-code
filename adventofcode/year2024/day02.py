from __future__ import annotations
from adventofcode.common import Solution
from itertools import pairwise
from typing import List


class Day02(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._reports = []
        for i in self._load_input_as_lines():
            self._reports.append([int(level) for level in i.split(' ')])

    def _is_safe(self, report: List[int]) -> bool:
        differentials = [s - f for f, s in pairwise(report)]
        safely_increasing = sum([1 for d in differentials if 1 <= d <= 3])
        safely_decreasing = sum([1 for d in differentials if -3 <= d <= -1])
        return safely_increasing == len(report) - 1 or safely_decreasing == len(report) - 1

    def part_one(self):
        return len([report for report in self._reports if self._is_safe(report)])

    def part_two(self):
        safe = []
        for report in self._reports:
            if self._is_safe(report):
                safe.append(report)
            else:
                # report was unsafe, but dampen problem by removing one level and see if report will become safe
                for i in range(len(report)):
                    if self._is_safe(report[:i] + report[(i + 1):]):
                        safe.append(report)
                        break
        return len(safe)
