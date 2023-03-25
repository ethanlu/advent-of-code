from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.grid import Point2D
from adventofcode.common.range import Box2D
from adventofcode.year2019.day09 import IntCodeCPUComplete
from functools import reduce
from typing import Dict, List

import sys


deltas = (Point2D(-1, -1), Point2D(-1, 0), Point2D(0, -1))


class TractorBeamSystem(object):
    def __init__(self, program: List[int]):
        self._program = program

    def measure_position(self, position: Point2D) -> int:
        drone = IntCodeCPUComplete(self._program)
        drone.add_input(position.x)
        drone.add_input(position.y)
        drone.run()
        return drone.get_output()

    def measure_space(self, space: Dict[Point2D, str]) -> int:
        return sum((1 for p, c in space.items() if c == '#'))

    def scan_square(self, position: Point2D, size: int) -> Dict[Point2D, str]:
        space: Dict[Point2D, str] = {}
        for y in range(position.y, position.y + size):
            for x in range(position.x, position.x + size):
                p = Point2D(x, y)
                response = self.measure_position(p)
                space[p] = '#' if response == 1 else '.'
        return space

    def scan_horizontal(self, y: int, startX: int, endX: int) -> Dict[Point2D, str]:
        space: Dict[Point2D, str] = {}
        for x in range(startX, endX):
            p = Point2D(x, y)
            response = self.measure_position(p)
            space[p] = '#' if response == 1 else '.'
        return space

    def show(self, space: Dict[Point2D, str], box: Box2D = None) -> None:
        minx = reduce(lambda acc, p: acc if acc < p.x else p.x, space.keys(), sys.maxsize)
        maxx = reduce(lambda acc, p: acc if acc > p.x else p.x, space.keys(), -sys.maxsize)
        miny = reduce(lambda acc, p: acc if acc < p.y else p.y, space.keys(), sys.maxsize)
        maxy = reduce(lambda acc, p: acc if acc > p.y else p.y, space.keys(), -sys.maxsize)
        for y in range(miny, maxy + 1):
            row = []
            for x in range(minx, maxx + 1):
                p = Point2D(x, y)
                if box is not None and box.contains(p):
                    row.append('|')
                elif p in space.keys():
                    row.append(space[p])
            print("".join(row))


class Day19(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._input = [int(i) for i in self._load_input_as_string().split(',')]

    def part_one(self):
        tbs = TractorBeamSystem(self._input)
        space = tbs.scan_square(Point2D(0, 0), 50)
        tbs.show(space)
        return tbs.measure_space(space)

    def part_two(self):
        tbs = TractorBeamSystem(self._input)
        target_length = 100

        # estimate start x, end x, and length of tractor beam per y position
        y = 100
        line = tbs.scan_horizontal(y, 0, 500)
        length = tbs.measure_space(line)
        x = sys.maxsize
        for p, c in line.items():
            if c == '#':
                x = p.x if p.x < x else x

        estimated_y = 3 * (y * target_length) // length
        estimated_x = (estimated_y * x) // y

        candidate = Box2D(Point2D(estimated_x, estimated_y - target_length + 1), Point2D(estimated_x + target_length - 1, estimated_y))
        best = candidate
        while True:
            corners = (
                tbs.measure_position(candidate.bottom_left),
                tbs.measure_position(candidate.top_left),
                tbs.measure_position(candidate.top_right),
                tbs.measure_position(candidate.bottom_right)
            )
            match corners:
                case (1, 1, 1, 1):
                    # fits completely in tractor beam...move up and left 1
                    best = candidate
                    delta = Point2D(-1, -1)
                case (0, 1, 1, 1):
                    # lower left corner is out of beam but everything else is in, move up 1
                    delta = Point2D(0, -1)
                case (1, 1, 0, 1):
                    # upper right corner is out of beam but everything else is in, move left 1
                    delta = Point2D(-1, 0)
                case _:
                    # cannot move anymore to have all corners in range
                    break
            candidate = Box2D(candidate.top_left + delta, candidate.bottom_right + delta)

        print(best.top_left)
        space = tbs.scan_square(Point2D(best.top_left.x - 25, best.top_left.y - 25), target_length + 50)
        tbs.show(space, best)
        return best.top_left.x * 10000 + best.top_left.y
