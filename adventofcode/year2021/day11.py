from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.grid import Point2D
from adventofcode.common.util import show_dict_grid
from collections import deque
from typing import List


deltas = (
    Point2D(-1, -1), Point2D(0, -1), Point2D(1, -1),
    Point2D(-1, 0), Point2D(1, 0),
    Point2D(-1, 1), Point2D(0, 1), Point2D(1, 1)
)


class DumboOctopusCave(object):
    def __init__(self, data: List[str]):
        self._maxy = len(data)
        self._maxx = len(data[0])
        self._octopuses = {}
        for y, row in enumerate(data):
            for x, cell in enumerate(row):
                p = Point2D(x, y)
                self._octopuses[p] = int(cell)

    @property
    def size(self) -> int:
        return len(self._octopuses.keys())

    def show(self) -> None:
        grid = {(p.x, p.y): str(c) for p, c in self._octopuses.items()}
        show_dict_grid(grid, self._maxx, self._maxy)

    def _energize(self, positions: List[Point2D]) -> List[Point2D]:
        flashing = []
        for position in positions:
            self._octopuses[position] += 1
            if self._octopuses[position] > 9:
                flashing.append(position)
        return flashing

    def step(self) -> int:
        flashed = set([])
        remaining = deque([list(self._octopuses.keys())])
        while len(remaining) > 0:
            energizing = []
            for flashing_position in self._energize(remaining.popleft()):
                if flashing_position not in flashed:
                    flashed.add(flashing_position)
                    for delta in deltas:
                        neighbor = flashing_position + delta
                        if neighbor in self._octopuses and neighbor not in flashed:
                            energizing.append(neighbor)
            if len(energizing) > 0:
                remaining.append(list(energizing))
        for p in list(flashed):
            self._octopuses[p] = 0
        return len(flashed)


class Day11(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._input = self._load_input_as_lines()

    def part_one(self):
        doc = DumboOctopusCave(self._input)
        total = 0
        print(f"initial")
        doc.show()
        for i in range(100):
            total += doc.step()
        print(f"\nafter 100 steps:")
        doc.show()
        return total

    def part_two(self):
        doc = DumboOctopusCave(self._input)
        i = 0
        while True:
            flashed = doc.step()
            i += 1
            if flashed == doc.size:
                print(f"step {i}")
                doc.show()
                break
        return i
