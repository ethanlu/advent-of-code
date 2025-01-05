from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.grid import Point2D
from adventofcode.common.util import show_dict_grid
from itertools import combinations
from typing import List


class AntennaPair(object):
    def __init__(self, antenna1: Point2D, antenna2: Point2D):
        self._antenna1 = antenna1
        self._antenna2 = antenna2

    @property
    def antenna1(self) -> Point2D:
        return self._antenna1

    @property
    def antenna2(self) -> Point2D:
        return self._antenna2

    @property
    def distance(self) -> Point2D:
        return self._antenna1 - self._antenna2


class AntennaMap(object):
    def __init__(self, data: List[str]):
        self._grid = {}
        self._antennas = {}
        self._maxy = len(data)
        self._maxx = len(data[0])

        t = {}
        for y, row in enumerate(data):
            for x, cell in enumerate(row):
                p = Point2D(x, y)
                self._grid[p] = cell
                if cell != '.':
                    if cell not in t:
                        t[cell] = []
                    t[cell].append(p)
        for frequency, antennas in t.items():
            self._antennas[frequency] = [AntennaPair(p1, p2) for p1, p2 in combinations(antennas, 2)]

    def show(self, antinodes: List[Point2D]) -> None:
        grid = {}
        for p in self._grid:
            grid[(p.x, p.y)] = self._grid[p]
        for p in antinodes:
            if grid[(p.x, p.y)] == '.':
                grid[(p.x, p.y)] = '#'
        show_dict_grid(grid, self._maxx, self._maxy)

    def antinode_locations(self, resonance: bool = False) -> List[Point2D]:
        locations = set([])
        for frequency, pairs in self._antennas.items():
            for pair in pairs:
                antinode_position = pair.antenna1
                locations.add(antinode_position)
                while True:
                    antinode_position = antinode_position + pair.distance
                    if antinode_position in self._grid:
                        locations.add(antinode_position)
                    if not resonance or antinode_position not in self._grid:
                        break
                antinode_position = pair.antenna2
                locations.add(antinode_position)
                while True:
                    antinode_position = antinode_position - pair.distance
                    if antinode_position in self._grid:
                        locations.add(antinode_position)
                    if not resonance or antinode_position not in self._grid:
                        break
        return list(locations)


class Day08(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._am = AntennaMap(self._load_input_as_lines())

    def part_one(self):
        antinodes = self._am.antinode_locations(False)
        self._am.show(antinodes)
        return len(antinodes)

    def part_two(self):
        antinodes = self._am.antinode_locations(True)
        self._am.show(antinodes)
        return len(antinodes)
