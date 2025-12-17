from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.grid import Point2D
from itertools import zip_longest
from typing import List


class HydroVent(object):
    def __init__(self, data: str):
        t = data.split(' -> ')
        self._start = Point2D(*(int(p) for p in t[0].split(',')))
        self._end = Point2D(*(int(p) for p in t[1].split(',')))

    @property
    def start(self) -> Point2D:
        return self._start

    @property
    def end(self) -> Point2D:
        return self._end

    def is_horizontal(self) -> bool:
        return self._start.x != self._end.x and self._start.y == self._end.y

    def is_vertical(self) -> bool:
        return self._start.x == self._end.x and self._start.y != self._end.y

    def positions(self) -> List[Point2D]:
        if self.is_horizontal():
            delta = Point2D((self._end.x - self._start.x) // abs(self._end.x - self._start.x), 0)
        elif self.is_vertical():
            delta = Point2D(0, (self._end.y - self._start.y) // abs(self._end.y - self._start.y))
        else:
            delta = Point2D((self._end.x - self._start.x) // abs(self._end.x - self._start.x), (self._end.y - self._start.y) // abs(self._end.y - self._start.y))
        positions = []
        current = self._start
        while current != self._end:
            positions.append(current)
            current += delta
        positions.append(current)
        return positions


class Day05(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._vents = [HydroVent(line) for line in self._load_input_as_lines()]

    def part_one(self):
        positions = {}
        for vent in self._vents:
            if vent.is_horizontal() or vent.is_vertical():
                for p in vent.positions():
                    if p not in positions:
                        positions[p] = 0
                    positions[p] += 1
        return sum((1 for v in positions.values() if v > 1))

    def part_two(self):
        positions = {}
        for vent in self._vents:
            for p in vent.positions():
                if p not in positions:
                    positions[p] = 0
                positions[p] += 1
        return sum((1 for v in positions.values() if v > 1))
