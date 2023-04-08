from __future__ import annotations
from adventofcode.common import Solution

import re


class Day02(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        regex = re.compile(r"^(\d+)-(\d+) (\w): (\w+)$")
        self._input = []
        for line in self._load_input_as_lines():
            a, b, letter, password = regex.match(line).groups()
            self._input.append((int(a), int(b), letter, password))

    def part_one(self):
        valid = 0
        for minimum, maximum, letter, password in self._input:
            if minimum <= password.count(letter) <= maximum:
                valid += 1
        return valid

    def part_two(self):
        valid = 0
        for position1, position2, letter, password in self._input:
            if (password[position1 - 1] == letter and password[position2 - 1] != letter) or (password[position1 - 1] != letter and password[position2 - 1] == letter):
                valid += 1
        return valid
