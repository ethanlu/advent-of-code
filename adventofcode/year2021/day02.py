from __future__ import annotations
from adventofcode.common import Solution


class Day02(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._directions = [(line.split(' ')[0], int(line.split(' ')[1])) for line in self._load_input_as_lines()]

    def part_one(self):
        horizontal = 0
        depth = 0
        for direction, amount in self._directions:
            match direction:
                case 'up':
                    depth -= amount
                case 'down':
                    depth += amount
                case 'forward':
                    horizontal += amount
                case _:
                    raise Exception(f"unexpected direction: {direction}")
        return horizontal * depth

    def part_two(self):
        horizontal = 0
        depth = 0
        aim = 0
        for direction, amount in self._directions:
            match direction:
                case 'up':
                    aim -= amount
                case 'down':
                    aim += amount
                case 'forward':
                    horizontal += amount
                    depth += aim * amount
                case _:
                    raise Exception(f"unexpected direction: {direction}")
        return horizontal * depth
