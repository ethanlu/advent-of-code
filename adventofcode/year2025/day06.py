from __future__ import annotations
from adventofcode.common import Solution
from functools import reduce
from typing import List

import re


space_regex = re.compile(r"\s+")


def process_math(operators: List[str], operands: List[List[int]]) -> int:
    total = 0
    for operator, operands in zip(operators, operands):
        match operator:
            case '+':
                total += reduce(lambda t, o: t + o, operands, 0)
            case '*':
                total += reduce(lambda t, o: t * o, operands, 1)
            case _:
                raise Exception(f"invalid operator : {operator}")
    return total


class Day06(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._input = [line.replace("\n", "") for line in self._load_input_as_lines(strip=False)]

    def part_one(self):
        operators = re.split(space_regex, self._input[-1].strip())
        operands = []
        data = []
        for line in self._input[:-1]:
            data.append([int(o) for o in re.split(space_regex, line.strip())])
        for i in range(len(operators)):
            operands.append([row[i] for row in data])

        return process_math(operators, operands)

    def part_two(self):
        operators = list(reversed(re.split(space_regex, self._input[-1].strip())))
        operands = []

        line = []
        for i in range(len(self._input[0])-1, -1, -1):   # read right to left
            data = ("".join([row[i] for row in self._input[:-1]])).strip()
            if not data:
                # column read was empty, completed a set of operands
                operands.append(line)
                line = []
            else:
                # column had data, so it is an operand
                line.append(int(data))
        operands.append(line)
        return process_math(operators, operands)
