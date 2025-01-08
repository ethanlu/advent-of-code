from __future__ import annotations
from adventofcode.common import Solution
from functools import cache, reduce


@cache
def blink(stone: int, left: int) -> int:
    if left == 0:
        # no more blinks left, so should only be 1 stone left
        return 1
    else:
        match stone, len(str(stone)) % 2:
            case 0, _:
                return blink(1, left - 1)
            case _, 0:
                mid = len(str(stone)) // 2
                return blink(int(str(stone)[:mid]), left - 1) + blink(int(str(stone)[mid:]), left - 1)
            case _, _:
                return blink(stone * 2024, left - 1)


class Day11(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._stones = [int(s) for s in self._load_input_as_string().split(' ')]

    def part_one(self):
        return reduce(lambda total, stone: total + blink(stone, 25), self._stones, 0)

    def part_two(self):
        return reduce(lambda total, stone: total + blink(stone, 75), self._stones, 0)
