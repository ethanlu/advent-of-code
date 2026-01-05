from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.grid import Point2D
from adventofcode.common.util import show_dict_grid
from itertools import cycle
from typing import List


deltas = (
    Point2D(-1, -1), Point2D(0, -1), Point2D(1, -1),
    Point2D(-1, 0), Point2D(0, 0), Point2D(1, 0),
    Point2D(-1, 1), Point2D(0, 1), Point2D(1, 1),
)


class ScannerImage(object):
    def __init__(self, image_enhancement_algorithm: str, image: List[str]):
        self._image_enhancement_algorithm = image_enhancement_algorithm
        self._miny, self._minx = 0, 0
        self._maxy, self._maxx = len(image), len(image[0])
        self._image = {}
        for y, row in enumerate(image):
            for x, cell in enumerate(row):
                self._image[Point2D(x, y)] = cell
        match self._image_enhancement_algorithm[0], self._image_enhancement_algorithm[-1]:
            case '.', _:
                # first pixel is empty, so infinite space will always be dark at every step
                self._fillspace = cycle('.')
            case '#', '#':
                # first and last pixel are lit, so infinite space will always be lit at every step
                self._fillspace = cycle('#')
            case '#', '.':
                # first pixel is lit, but last pixel is dark....so infinite space will alternate between being all lit and all dark
                self._fillspace = cycle(('.', '#'))
            case _:
                raise Exception(f"unexpected image enhancement algorithm beginning and end states: {self._image_enhancement_algorithm[0]} {self._image_enhancement_algorithm[-1]}")

    @property
    def lit(self) -> int:
        amount = 0
        for y in range(self._miny, self._maxy, 1):
            for x in range(self._minx, self._maxx, 1):
                p = Point2D(x, y)
                amount += 1 if self._image[p] == '#' else 0
        return amount

    def _neighbors(self, position: Point2D, fill: str) -> int:
        pixels = []
        for delta in deltas:
            n = position + delta
            pixels.append(self._image[n] if n in self._image else fill)
        return int(''.join(pixels).replace('.', '0').replace('#', '1'), 2)

    def show(self):
        grid = {}
        tx, ty = 0, 0
        for y in range(self._miny, self._maxy, 1):
            tx = 0
            for x in range(self._minx, self._maxx, 1):
                p = Point2D(x, y)
                grid[(tx, ty)] = self._image[p]
                tx += 1
            ty += 1
        show_dict_grid(grid, tx, ty)

    def step(self):
        miny, minx, maxy, maxx = self._miny, self._minx, self._maxy, self._maxx
        image = {}
        fill = next(self._fillspace)
        for y in range(self._miny - 1, self._maxy + 1, 1):
            for x in range(self._minx - 1, self._maxx + 1, 1):
                position = Point2D(x, y)
                image[position] = self._image_enhancement_algorithm[self._neighbors(position, fill)]
                if image[position] == '#':
                    miny = miny if miny < y else y
                    minx = minx if minx < x else x
                    maxy = maxy if maxy > y else y
                    maxx = maxx if maxx > x else x
        self._image = image
        self._miny, self._minx, self._maxy, self._maxx = miny, minx, maxy + 1, maxx + 1


class Day20(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._data = self._load_input_as_lines()

    def part_one(self):
        si = ScannerImage(self._data[0], self._data[2:])
        for i in range(2):
            si.step()
        print(f"\nafter 2 steps")
        return si.lit

    def part_two(self):
        si = ScannerImage(self._data[0], self._data[2:])
        for i in range(50):
            if i % 10 == 0:
                print(f"step {i}")
            si.step()
        si.show()
        return si.lit
