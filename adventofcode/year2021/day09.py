from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.grid import Point2D
from collections import deque
from typing import Any, List, Set, Tuple


deltas = (Point2D(0, -1), Point2D(1, 0), Point2D(0, 1), Point2D(-1, 0))


class HeightMap(object):
    def __init__(self, data: List[str]):
        self._maxy = len(data)
        self._maxx = len(data[0])
        self._heights = {}
        for y, row in enumerate(data):
            for x, cell in enumerate(row):
                p = Point2D(x, y)
                self._heights[p] = int(cell)

    @property
    def positions(self) -> Tuple[Point2D]:
        return tuple(self._heights.keys())

    def height(self, position: Point2D) -> int:
        return self._heights[position]

    def neighbors(self, position: Point2D) -> Tuple[Any]:
        return tuple([position + delta for delta in deltas if (position + delta) in self._heights])


class Day09(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._hm = HeightMap(self._load_input_as_lines())

    def part_one(self):
        lows = []
        for position in self._hm.positions:
            if self._hm.height(position) < 9:
                position_height = self._hm.height(position)
                neighbors = self._hm.neighbors(position)
                if len([1 for n in neighbors if self._hm.height(n) > position_height]) == len(neighbors):
                    lows.append(position_height)
        return sum([low + 1 for low in lows])

    def part_two(self):
        lows = []
        for position in self._hm.positions:
            if self._hm.height(position) < 9:
                position_height = self._hm.height(position)
                neighbors = self._hm.neighbors(position)
                if len([1 for n in neighbors if self._hm.height(n) > position_height]) == len(neighbors):
                    lows.append(position)
        basins = []
        processed = set()
        for low in lows:
            if low not in processed:
                remaining = deque([low])
                basin = set([])
                while len(remaining) > 0:
                    position = remaining.popleft()
                    basin.add(position)
                    processed.add(position)
                    for neighbor in self._hm.neighbors(position):
                        if self._hm.height(neighbor) < 9 and neighbor not in processed:
                            remaining.append(neighbor)
                basins.append(basin)
        basins = sorted(basins, key=len)
        return len(basins[-1]) * len(basins[-2]) * len(basins[-3])
