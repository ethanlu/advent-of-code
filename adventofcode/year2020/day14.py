from __future__ import annotations
from adventofcode.common import Solution
from collections import defaultdict
from itertools import product
from typing import List

import re


class MemoryDecoder(object):
    def __init__(self):
        self._ones = 0
        self._zeroes = 0
        self._memory = defaultdict(int)

    def set_bitmask(self, mask: str) -> None:
        self._ones = int(mask.replace('X', '0'), 2)
        self._zeroes = int(mask.replace('X', '1'), 2)

    def write(self, address: int, value: int) -> None:
        self._memory[address] = (value | self._ones) & self._zeroes

    def checksum(self) -> int:
        return sum(self._memory.values())


class MemoryDecoder2(MemoryDecoder):
    def __init__(self):
        super().__init__()
        self._floating = []

    def set_bitmask(self, mask: str) -> None:
        super().set_bitmask(mask)
        self._floating = [i for i, d in enumerate(reversed(list(mask))) if d == 'X']

    def write(self, address: int, value: int) -> None:
        for permutation in product(range(2), repeat=len(self._floating)):
            masked_address = address | self._ones
            for position, bit in zip(self._floating, permutation):
                if bit == 1:
                    masked_address = masked_address | (1 << position)
                else:
                    masked_address = masked_address & ~(1 << position)
            self._memory[masked_address] = value


class Day14(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._input = self._load_input_as_lines()
        self._regex = re.compile(r"^mem\[(\d+)\] = (\d+)")

    def part_one(self):
        md = MemoryDecoder()
        for line in self._input:
            if line[0:4] == "mask":
                md.set_bitmask(line[7:])
            else:
                m = self._regex.match(line)
                md.write(int(m.groups()[0]), int(m.groups()[1]))

        return md.checksum()

    def part_two(self):
        md = MemoryDecoder2()
        for line in self._input:
            if line[0:4] == "mask":
                md.set_bitmask(line[7:])
            else:
                m = self._regex.match(line)
                md.write(int(m.groups()[0]), int(m.groups()[1]))

        return md.checksum()
