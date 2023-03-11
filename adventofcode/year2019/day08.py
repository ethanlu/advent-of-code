from __future__ import annotations
from adventofcode.common import Solution
from functools import reduce
from typing import List

import sys


class SpaceImageFormat(object):
    def __init__(self, width: int, height: int, encoding: str):
        self._width = width
        self._height = height
        self._encoding = encoding
        self._layers = []
        for offset in range(0, len(self._encoding), (self._width * self._height)):
            self._layers.append([*self._encoding[offset:(offset + self._width * self._height)]])

    @property
    def layers(self):
        return self._layers

    def checksum(self):
        z = sys.maxsize
        l = None
        for layer in self._layers:
            zcount = reduce(lambda acc, x: acc + (1 if x == '0' else 0), layer, 0)
            if z > zcount:
                z = zcount
                l = layer
        return reduce(lambda acc, x: acc + (1 if x == '1' else 0), l, 0) * reduce(lambda acc, x: acc + (1 if x == '2' else 0), l, 0)

    def render(self) -> str:
        image = [['.' for _ in range(self._width)] for _ in range(self._height)]
        for x in range(self._width):
            for y in range(self._height):
                for l in self._layers:
                    match l[self._width * y + x]:
                        case '0':
                            image[y][x] = ' '
                            break
                        case '1':
                            image[y][x] = '#'
                            break
                        case _:
                            pass

        return "\n".join(["".join(row) for row in image])


class Day08(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._input = self._load_input_as_string()

    def part_one(self):
        image = SpaceImageFormat(25, 6, self._input)
        return image.checksum()

    def part_two(self):
        image = SpaceImageFormat(25, 6, self._input)
        return image.render()
