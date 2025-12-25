from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.grid import Point2D
from adventofcode.common.util import show_dict_grid
from typing import List


class TransparencyPaper(object):
    def __init__(self, data: List[str]):
        self._maxy = 0
        self._maxx = 0
        self._dots = set()
        for line in data:
            p = Point2D(*(int(n) for n in line.split(',')))
            self._dots.add(p)
            self._maxy = self._maxy if self._maxy > p.y else p.y
            self._maxx = self._maxx if self._maxx > p.x else p.x

    @property
    def dots(self) -> List[Point2D]:
        return list(self._dots)

    @property
    def dimensions(self) -> int:
        return self._maxx * self._maxy

    def show(self):
        grid = {}
        for y in range(self._maxy + 1):
            for x in range(self._maxx + 1):
                grid[(x, y)] = '.'
        for d in self._dots:
            grid[(d.x, d.y)] = '#'
        show_dict_grid(grid, self._maxx + 1, self._maxy + 1)

    def fold(self, axis: str, position: int) -> None:
        dots = []
        match axis:
            case 'x':
                for d in self._dots:
                    if d.x < position:
                        dots.append(d)
                    else:
                        dots.append(Point2D(position - abs(d.x - position), d.y))
            case 'y':
                for d in self._dots:
                    if d.y < position:
                        dots.append(d)
                    else:
                        dots.append(Point2D(d.x, position - abs(d.y - position)))
            case _:
                raise Exception(f"unexpected fold axis {axis}")
        self._dots = set(dots)
        self._maxy = max((d.y for d in self._dots))
        self._maxx = max((d.x for d in self._dots))

class Day13(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        dots = []
        self._folds = []
        reading_dots = True
        for line in self._load_input_as_lines():
            if not line:
                reading_dots = False
                continue
            if reading_dots:
                dots.append(line)
            else:
                axis, amount = (line.split(' ')[2]).split('=')
                self._folds.append((axis, int(amount)))
        self._tp = TransparencyPaper(dots)

    def part_one(self):
        for (axis, position) in self._folds:
            self._tp.fold(axis, position)
            break
        return len(self._tp.dots)

    def part_two(self):
        for (axis, position) in self._folds:
            self._tp.fold(axis, position)
            if self._tp.dimensions < 1000:
                print(f"\nafter fold on {axis}={position}")
                self._tp.show()
            else:
                print(f"folding...")
        return None
