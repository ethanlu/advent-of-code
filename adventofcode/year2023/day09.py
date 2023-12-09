from __future__ import annotations
from adventofcode.common import Solution
from functools import reduce
from itertools import pairwise
from typing import List


class OASIS(object):
    def __init__(self, data: List[int]):
        self._data = data

    def _differential(self, data: List[int], predictions: List[int]) -> int:
        next_data = []
        all_zero = True
        for a, b in pairwise(data):
            diff = b - a
            next_data.append(diff)
            all_zero = True if all_zero and diff == 0 else False
        if all_zero:
            return reduce(lambda x, y: x + y, reversed(predictions + [data[-1]]))
        else:
            return self._differential(next_data, predictions + [data[-1]])

    def predict_future(self) -> int:
        return self._differential(self._data, [])

    def predict_past(self):
        return self._differential(list(reversed(self._data)), [])


class Day09(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._oasis = []
        for l in self._load_input_as_lines():
            self._oasis.append(OASIS([int(d) for d in l.split(' ')]))

    def part_one(self):
        total = 0
        for o in self._oasis:
            total += o.predict_future()
        return total

    def part_two(self):
        total = 0
        for o in self._oasis:
            total += o.predict_past()
        return total
