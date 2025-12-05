from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.grid import Point2D
from adventofcode.common.util import show_dict_grid
from typing import Dict, List, Set


deltas = (Point2D(-1, -1), Point2D(0, -1), Point2D(1, -1), Point2D(-1, 0), Point2D(1, 0), Point2D(-1, 1), Point2D(0, 1), Point2D(1, 1))


class PrintingDepartmentMap(object):
    def __init__(self, data: List[str]):
        self._maxy = len(data)
        self._maxx = len(data[0])
        self._paper_rolls = []
        self._grid = {}
        for y, row in enumerate(data):
            for x, c in enumerate(row):
                p = Point2D(x, y)
                self._grid[p] = c
                if c == '@':
                    self._paper_rolls.append(p)

    @property
    def maxx(self) -> int:
        return self._maxx

    @property
    def maxy(self) -> int:
        return self._maxy

    @property
    def grid(self) -> Dict[Point2D]:
        return self._grid

    def _neighbors(self, position: Point2D) -> List[Point2D]:
        neighbors = []
        for delta in deltas:
            neighbor_p = position + delta
            if neighbor_p in self._grid and self._grid[neighbor_p] == '@':
                neighbors.append(neighbor_p)
        return neighbors

    def remove(self, position: Point2D) -> None:
        if position not in self._grid or self._grid[position] != '@':
            raise Exception(f"invalid paper roll position : {position}")
        self._grid[position] = '.'
        self._paper_rolls.remove(position)

    def accessible(self, max_neighbors: int) -> Set[Point2D]:
        accessible_roll = []
        for p in self._paper_rolls:
            if len(self._neighbors(p)) < max_neighbors:
                accessible_roll.append(p)
        return set(accessible_roll)


class Day04(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._pdm = PrintingDepartmentMap(self._load_input_as_lines())

    def part_one(self):
        return len(self._pdm.accessible(4))

    def part_two(self):
        total = 0
        removable_rolls = self._pdm.accessible(4)
        print('initial:')
        show_dict_grid({(p.x, p.y): 'x' if p in removable_rolls else v for p, v in self._pdm.grid.items()}, self._pdm.maxx, self._pdm.maxy)
        while len(removable_rolls) > 0:
            print(f"moving {len(removable_rolls)} paper rolls")
            total += len(removable_rolls)
            for p in removable_rolls:
                self._pdm.remove(p)
            removable_rolls = self._pdm.accessible(4)
        show_dict_grid({(p.x, p.y): 'x' if p in removable_rolls else v for p, v in self._pdm.grid.items()}, self._pdm.maxx, self._pdm.maxy)
        return total