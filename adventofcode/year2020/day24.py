from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.grid import Point2D
from typing import Dict


directions = (Point2D(1, 1), Point2D(2, 0), Point2D(1, -1), Point2D(-1, -1), Point2D(-2, 0), Point2D(-1, 1))


class HexGrid(object):
    def __init__(self):
        self._grid: Dict[Point2D, int] = {Point2D(0, 0): 1}

    @property
    def black_tiles(self) -> int:
        return sum((1 for c in self._grid.values() if c == 0))

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

    def _neighbors(self, position: Point2D) -> int:
        neighbors = 0
        for direction in directions:
            neighbor = position + direction
            if neighbor in self._grid:
                neighbors += 1 if self._grid[neighbor] == 0 else 0
        return neighbors

    def day(self) -> None:
        black_tiles = set([])
        white_tiles = set([])
        for position, color in self._grid.items():
            if color == 0:
                black_tiles.add(position)
                for direction in directions:
                    neighbor = position + direction
                    if neighbor not in self._grid or self._grid[neighbor] == 1:
                        white_tiles.add(neighbor)
            else:
                white_tiles.add(position)
        grid = {}
        for position in black_tiles:
            neighbors = self._neighbors(position)
            grid[position] = 1 if neighbors == 0 or neighbors > 2 else 0
        for position in white_tiles:
            neighbors = self._neighbors(position)
            grid[position] = 0 if neighbors == 2 else 1
        self._grid = grid


class Day24(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._input = self._load_input_as_lines()
        self._grid = HexGrid()

    def part_one(self):
        for s in self._input:
            self._grid.process(s)

        return self._grid.black_tiles

    def part_two(self):
        for _ in range(100):
            self._grid.day()
            print(f"day {_ + 1} : {self._grid.black_tiles}")

        return self._grid.black_tiles
