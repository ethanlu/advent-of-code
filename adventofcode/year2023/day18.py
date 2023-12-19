from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.grid import Point2D
from itertools import pairwise
from typing import List, Tuple


class LavaLagoon(object):
    def __init__(self, plan: List[Tuple[str, int, str]]):
        self._vertices = []
        self._perimeter = 0
        self._corners = 0
        p = Point2D(0, 0)
        for (direction, amount, _) in plan:
            self._perimeter += amount
            self._corners += 1
            match direction:
                case 'U':
                    p += Point2D(0, amount)
                case 'D':
                    p += Point2D(0, -amount)
                case 'L':
                    p += Point2D(-amount, 0)
                case 'R':
                    p += Point2D(amount, 0)
                case _:
                    raise Exception(f"Unexpected direction {direction}")
            self._vertices.append(p)

    def area(self) -> int:
        # based on https://en.wikipedia.org/wiki/Shoelace_formula
        # area of all cells within the perimeter and the parts of the perimeter cell
        area_inside = abs(sum((p1.x * p2.y - p2.x * p1.y for p1, p2 in pairwise([self._vertices[-1]] + self._vertices)))) // 2

        # parts of the perimeter that are straight have half of their area excluded from shoelace formula...so account for this missing area
        area_straight_edges = (self._perimeter - self._corners) // 2

        # closed loop means at least 4 corners must be outer corners where 3/4 of their area were excluded from shoelace formula. so these contribute an area of 3
        # any additional corners beyond the first 4 corners are always even and they can be paired so that each pair contributes an area of 1 each
        area_corners = 3 + (self._corners - 4) // 2

        return area_inside + area_straight_edges + area_corners


class Day18(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._data = []
        for l in self._load_input_as_lines():
            t = l.split(' ')
            self._data.append((t[0], int(t[1]), t[2][2:-1]))

    def part_one(self):
        ll = LavaLagoon(self._data)
        return ll.area()

    def part_two(self):
        direction_codes = {0: 'R', 1: 'D', 2: 'L', 3: 'U'}
        ll = LavaLagoon([(direction_codes[int(d[2][-1])], int(d[2][0:-1], 16), '') for d in self._data])
        return ll.area()