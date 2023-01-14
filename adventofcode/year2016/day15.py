from __future__ import annotations
from adventofcode.common import Solution
from functools import reduce

import math
import re


class Disc(object):
    def __init__(self, id: int, positions: int, starting_position: int):
        self._id = id
        self._positions = positions
        self._starting_position = starting_position

    @property
    def positions(self):
        return self._positions

    def is_open(self, t: int) -> int:
        return (t + self._id + self._starting_position) % self._positions == 0


class Day15(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        regex = re.compile(r'Disc #(\d+) has (\d+) positions; at time=0, it is at position (\d+)')
        self._discs = []

        for line in self._load_input_as_lines():
            m = regex.match(line)
            self._discs.append(Disc(int(m.groups()[0]), int(m.groups()[1]), int(m.groups()[2])))

    def part_one(self):
        t = 0
        for i in range(0, math.lcm(*(d.positions for d in self._discs))):
            if reduce(lambda acc, d: acc and d.is_open(i), self._discs, True):
                t = i
                break

        return t

    def part_two(self):
        self._discs.append(Disc(len(self._discs) + 1, 11, 0))

        t = 0
        for i in range(0, math.lcm(*(d.positions for d in self._discs))):
            if reduce(lambda acc, d: acc and d.is_open(i), self._discs, True):
                t = i
                break

        return t
