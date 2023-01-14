from __future__ import annotations
from adventofcode.common import Solution


def dragon_curve(data: str, length: int) -> str:
    while len(data) < length:
        data = data + '0' + ''.join(('1' if c == '0' else '0' for c in reversed(data)))
    return data[:length]


def checksum(data: str) -> str:
    while True:
        data = ''.join(('1' if a == b else '0' for (a, b) in zip(*[iter(data)] * 2)))
        if len(data) % 2 == 1:
            break
    return data


class Day16(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._input = self._load_input_as_string()

    def part_one(self):
        return checksum(dragon_curve(self._input, 272))

    def part_two(self):
        return checksum(dragon_curve(self._input, 35651584))
    