from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.range import Interval
from adventofcode.common.grid import Point2D
from adventofcode.common.util import show_grid
from itertools import combinations
from typing import List


directions = (Point2D(0, -1), Point2D(1, 0), Point2D(0, 1), Point2D(-1, 0))


class Universe(object):
    def __init__(self, data: List[List[str]]):
        self._universe = data
        self._maxy = len(data)
        self._maxx = len(data[0])
        self._horizontal_gaps = []
        self._vertical_gaps = []
        for y in range(self._maxy):
            for x in range(self._maxx):
                if self._universe[y][x] != '.':
                    break
            else:
                self._horizontal_gaps.append(y)
        for x in range(self._maxx):
            for y in range(self._maxy):
                if self._universe[y][x] != '.':
                    break
            else:
                self._vertical_gaps.append(x)

    @property
    def universe(self) -> List[List[str]]:
        return self._universe

    @property
    def maxy(self) -> int:
        return self._maxy

    @property
    def maxx(self) -> int:
        return self._maxx

    @property
    def galaxies(self) -> List[Point2D]:
        galaxies = []
        for y, row in enumerate(self._universe):
            for x, cell in enumerate(row):
                if self._universe[y][x] == '#':
                    galaxies.append(Point2D(x, y))
        return galaxies

    def distance(self, g1: Point2D, g2: Point2D, expansion: int) -> int:
        y_distance = abs(g1.y - g2.y)
        y_interval = Interval(min(g1.y, g2.y), max(g1.y, g2.y))
        y_gaps = sum((1 for y in self._horizontal_gaps if y_interval.contains(y)))

        x_distance = abs(g1.x - g2.x)
        x_interval = Interval(min(g1.x, g2.x), max(g1.x, g2.x))
        x_gaps = sum((1 for x in self._vertical_gaps if x_interval.contains(x)))

        return (y_distance - y_gaps) + (x_distance - x_gaps) + (y_gaps * expansion) + (x_gaps * expansion)


class Day11(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._universe = Universe([list(l) for l in self._load_input_as_lines()])

    def part_one(self):
        total = 0
        for g1, g2 in combinations(self._universe.galaxies, 2):
            total += self._universe.distance(g1, g2, 2)
        return total

    def part_two(self):
        total = 0
        for g1, g2 in combinations(self._universe.galaxies, 2):
            total += self._universe.distance(g1, g2, 1000000)
        return total
