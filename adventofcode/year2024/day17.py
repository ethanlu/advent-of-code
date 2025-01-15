from __future__ import annotations
from adventofcode.common import Solution
from functools import reduce
from typing import List

import math


class ChronospatialComputer(object):
    def __init__(self, a: int, b: int, c: int, program: List[int]):
        self._a = a
        self._b = b
        self._c = c
        self._program = program
        self._output = []
        self._index = 0

    @property
    def output(self) -> List[int]:
        return self._output

    def _get_combo(self, operand: int) -> int:
        match operand:
            case 0 | 1 | 2 | 3:
                return operand
            case 4:
                return self._a
            case 5:
                return self._b
            case 6:
                return self._c
            case _:
                raise Exception(f"invalid combo operand value : {operand}")

    def step(self) -> bool:
        if self._index < len(self._program):
            operator = self._program[self._index]
            operand = self._program[self._index + 1]
            index_increment = 2
            match operator:
                case 0:
                    # adv
                    self._a = self._a // (2 ** self._get_combo(operand))
                case 1:
                    # bxl
                    self._b = self._b ^ operand
                case 2:
                    # bst
                    self._b = self._get_combo(operand) % 8
                case 3:
                    # jnz
                    if self._a != 0:
                        self._index = operand
                        index_increment = 0
                case 4:
                    # bxc
                    self._b = self._b ^ self._c
                case 5:
                    # out
                    self._output.append(self._get_combo(operand) % 8)
                case 6:
                    # bdv
                    self._b = self._a // (2 ** self._get_combo(operand))
                case 7:
                    # cdv
                    self._c = self._a // (2 ** self._get_combo(operand))
            self._index += index_increment
            return True
        return False


class Day17(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        input = self._load_input_as_lines()
        self._a = int(input[0].split(' ')[-1])
        self._b = int(input[1].split(' ')[-1])
        self._c = int(input[2].split(' ')[-1])
        self._program = [int(c) for c in input[4].split(' ')[-1].split(',')]

    def part_one(self):
        cc = ChronospatialComputer(self._a, self._b, self._c, self._program)
        while cc.step():
            pass
        return ",".join((str(c) for c in cc.output))

    def part_two(self):
        dl = len(self._program)
        a = 0
        for di in range(dl):
            while True:
                cc = ChronospatialComputer(a, self._b, self._c, self._program)
                while cc.step():
                    pass
                if cc.output == self._program[(dl - di - 1):]:
                    a = a << 3
                    break
                a += 1
        a = a >> 3

        cc = ChronospatialComputer(a, self._b, self._c, self._program)
        while cc.step():
            pass
        print(f"program: {','.join((str(d) for d in self._program))}")
        print(f"found  : {','.join((str(c) for c in cc.output))}")
        return a
