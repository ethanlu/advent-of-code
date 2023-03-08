from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.grid import Point2D
from functools import reduce
from typing import List


class Day03(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._input = [l for l in self._load_input_as_lines()]

    def _get_delta(self, direction: str) -> Point2D:
        match direction:
            case 'U':
                return Point2D(0, -1)
            case 'R':
                return Point2D(1, 0)
            case 'D':
                return Point2D(0, 1)
            case 'L':
                return Point2D(-1, 0)
            case _:
                raise Exception(f"Invalid direction : {direction}")

    def part_one(self):
        origin = Point2D(0, 0)
        paths = []
        for wire in [wire.split(',') for wire in self._input]:
            visited = set([])
            position = origin

            for path in wire:
                for i in range(int(path[1:])):
                    position += self._get_delta(path[0])
                    visited.add(position)
            paths.append(visited)

        intersections = reduce(lambda a, b: a.intersection(b), paths)
        return reduce(lambda a, b: a if a < b else b, (abs(p.x) + abs(p.y) for p in intersections))

    def part_two(self):
        origin = Point2D(0, 0)
        paths = []
        for wire in [wire.split(',') for wire in self._input]:
            visited = {}
            position = origin
            steps = 0

            for path in wire:
                for i in range(int(path[1:])):
                    position += self._get_delta(path[0])
                    steps += 1
                    if position not in visited:
                        visited[position] = steps
            paths.append(visited)

        intersections = reduce(lambda a, b: a.intersection(b), [set(p.keys()) for p in paths])
        return reduce(lambda a, b: a if a < b else b, (paths[0][p] + paths[1][p] for p in intersections))
