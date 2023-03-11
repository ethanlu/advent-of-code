from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.grid import Point2D
from adventofcode.year2019.day09 import IntCodeCPUComplete
from typing import List

import sys


class HullPaintingRobot(object):
    def __init__(self, program: List[int], initial_input: int):
        self._cpu = IntCodeCPUComplete(program)
        self._cpu.add_input(initial_input)
        self._position = Point2D(0, 0)
        self._panels = {}
        self._orientation_index = 0
        self._deltas = (Point2D(0, -1), Point2D(1, 0), Point2D(0, 1), Point2D(-1, 0))   # up, right, down, left
        self._minx = sys.maxsize
        self._maxx = -sys.maxsize
        self._miny = sys.maxsize
        self._maxy = -sys.maxsize

    def run(self) -> int:
        painted = 0
        while not self._cpu.halted:
            # paint panel
            self._cpu.run()
            paint = self._cpu.get_output()
            painted += (1 if self._position not in self._panels.keys() else 0)
            self._panels[self._position] = paint

            # turn and move
            self._cpu.run()
            turn = self._cpu.get_output()
            match turn:
                case 0: # turn left
                    self._orientation_index = (self._orientation_index - 1) if (self._orientation_index - 1) >= 0 else (len(self._deltas) - 1)
                case 1: # turn right
                    self._orientation_index = (self._orientation_index + 1) if (self._orientation_index + 1) < len(self._deltas) else 0
                case _:
                    raise Exception(f"Invalid turn : {turn}")
            self._position += self._deltas[self._orientation_index]

            # update width and height tracking
            self._minx = self._position.x if self._position.x < self._minx else self._minx
            self._maxx = self._position.x if self._position.x > self._maxx else self._maxx
            self._miny = self._position.y if self._position.y < self._miny else self._miny
            self._maxy = self._position.y if self._position.y > self._maxy else self._maxy

            # feed next input
            self._cpu.add_input(self._panels[self._position] if self._position in self._panels.keys() else 0)

        return painted

    def show(self) -> None:
        for y in range(self._miny, self._maxy - self._miny + 1):
            row = []
            for x in range(self._minx, self._maxx - self._minx + 1):
                p = Point2D(x, y)
                paint = self._panels[p] if p in self._panels.keys() else 0
                row.append(' ' if paint == 0 else '#')
            print("".join(row))

class Day11(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._input = [int(i) for i in self._load_input_as_string().split(',')]

    def part_one(self):
        hpb = HullPaintingRobot(self._input, 0)
        return hpb.run()

    def part_two(self):
        hpb = HullPaintingRobot(self._input, 1)
        hpb.run()
        hpb.show()

        return ""
