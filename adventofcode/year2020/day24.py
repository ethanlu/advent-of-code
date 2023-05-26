from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.grid import Point2D
from typing import Dict


class HexGrid(object):
    def __init__(self):
        self._grid: Dict[Point2D, int] = {Point2D(0, 0): 1}
        self._flipped = 0

    @property
    def flipped(self) -> int:
        return self._flipped

    def process(self, sequence: str) -> None:
        position = Point2D(0, 0)
        direction = None
        for d in list(sequence):
            match d:
                case 'e' | 'w':
                    if direction is None:
                        direction = d
                    else:
                        direction += d
                case _:
                    direction = d
                    continue

            match direction:
                case 'ne':
                    position = position + Point2D(1, 1)
                case 'e':
                    position = position + Point2D(2, 0)
                case 'se':
                    position = position + Point2D(1, -1)
                case 'sw':
                    position = position + Point2D(-1, -1)
                case 'w':
                    position = position + Point2D(-2, 0)
                case 'nw':
                    position = position + Point2D(-1, 1)
            direction = None

        if position not in self._grid:
            self._grid[position] = 1
        self._grid[position] = (self._grid[position] + 1) % 2
        self._flipped += 1 if self._grid[position] == 0 else -1


class Day24(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._input = self._load_input_as_lines()

    def part_one(self):
        hg = HexGrid()
        for s in self._input:
            hg.process(s)

        return hg.flipped

    def part_two(self):
        return "ᕕ( ᐛ )ᕗ"
