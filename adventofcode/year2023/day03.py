from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.grid import Point2D
from functools import reduce
from typing import Dict, List, Set, Optional


directions = (Point2D(-1, -1), Point2D(-1, 0), Point2D(-1, 1), Point2D(0, -1), Point2D(0, 1), Point2D(1, -1), Point2D(1, 0), Point2D(1, 1))


class Label(object):
    def __init__(self, p: Point2D, n: str):
        self._start = p
        self._value = int(n)

    def __repr__(self):
        return str(self._value)

    def __hash__(self):
        return self._start.x * 13 + self._start.y * 37 + self._value * 1337

    def __eq__(self, other):
        return self._start.x == other.start.x and self._start.y == other.start.y and self._value == other.value if issubclass(type(other), Label) else False

    @property
    def value(self) -> int:
        return self._value

    @property
    def start(self) -> Point2D:
        return self._start


class Schematic(object):
    def __init__(self, data: List[str]):
        self._schematic: Dict[Point2D, str] = {}
        self._numbers: Dict[Point2D, Label] = {}
        self._parts: List[Point2D] = []

        for y, l in enumerate(data):
            number = ''
            number_points = []
            for x, c in enumerate(l):
                p = Point2D(x, y)
                self._schematic[p] = c
                match c:
                    case '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | '0':
                        number += c
                        number_points.append(p)
                    case z:
                        if z != '.':
                            self._parts.append(p)
                        if number:
                            label = Label(number_points[0], number)
                            for p2 in number_points:
                                self._numbers[p2] = label
                        number = ''
                        number_points = []
            if number:
                label = Label(number_points[0], number)
                for p2 in number_points:
                    self._numbers[p2] = label

    @property
    def parts(self) -> List[Point2D]:
        return self._parts

    def get_part_at(self, p: Point2D) -> Optional[str]:
        return self._schematic[p] if p in self._schematic else None

    def get_part_number_at(self, p: Point2D) -> Optional[Label]:
        return self._numbers[p] if p in self._numbers else None


class Day03(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._schematic = Schematic(self._load_input_as_lines())

    def part_one(self):
        part_numbers = []
        for p in self._schematic.parts:
            for d in directions:
                pn = self._schematic.get_part_number_at(p + d)
                if pn:
                    part_numbers.append(pn)

        print(f"part numbers : {set(part_numbers)}")
        return sum((pn.value for pn in set(part_numbers)))

    def part_two(self):
        gear_ratios = []
        for p in self._schematic.parts:
            if self._schematic.get_part_at(p) == '*':
                part_numbers = []
                for d in directions:
                    pn = self._schematic.get_part_number_at(p + d)
                    if pn:
                        part_numbers.append(pn)
                adjacent_part_numbers = set(part_numbers)
                if len(adjacent_part_numbers) == 2:
                    print(f"gears : {adjacent_part_numbers}")
                    gear_ratios.append(reduce(lambda x, y: x.value * y.value, adjacent_part_numbers))

        print(f"gear ratios : {gear_ratios}")
        return sum(gear_ratios)
