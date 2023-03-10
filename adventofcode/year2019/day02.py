from __future__ import annotations
from adventofcode.common import Solution
from itertools import permutations
from typing import List


class IntCodeCPU(object):
    def __init__(self, instructions: List[int], verbose: bool = False):
        self._instructions = [i for i in instructions]
        self._index = 0
        self._verbose = verbose

    def set_position(self, position: int, value: int) -> None:
        self._instructions[position] = value

    def position(self, i: int) -> int:
        return self._instructions[i]

    def _get_operation_details(self) -> str:
        return str(self._instructions[self._index]).strip('-').zfill(5)

    def _get_parameter1(self) -> int:
        return self._instructions[self._instructions[self._index + 1]] if int(self._get_operation_details()[-3]) == 0 else self._instructions[self._index + 1]

    def _get_parameter2(self) -> int:
        return self._instructions[self._instructions[self._index + 2]] if int(self._get_operation_details()[-4]) == 0 else self._instructions[self._index + 2]

    def _operation1(self) -> None:
        if self._verbose:
            print(f"{self._index}: {self._instructions[self._index:(self._index + 4)]} : address[{self._instructions[self._index + 3]}] = {self._get_parameter1()} + {self._get_parameter2()}")
        self._instructions[self._instructions[self._index + 3]] = self._get_parameter1() + self._get_parameter2()
        self._index += 4

    def _operation2(self) -> None:
        if self._verbose:
            print(f"{self._index}: {self._instructions[self._index:(self._index + 4)]} : address[{self._instructions[self._index + 3]}] = {self._get_parameter1()} * {self._get_parameter2()}")
        self._instructions[self._instructions[self._index + 3]] = self._get_parameter1() * self._get_parameter2()
        self._index += 4

    def run(self) -> None:
        self._index = 0
        while True:
            opcode = int(self._get_operation_details()[-2:])
            if opcode == 99:
                break

            operation = f"_operation{opcode}"
            if hasattr(self, operation):
                getattr(self, operation)()
            else:
                raise Exception(f"Invalid opcode {self._instructions[self._index]} @ {self._index}")


class Day02(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._input = [int(i) for i in self._load_input_as_string().split(',')]

    def part_one(self):
        cpu = IntCodeCPU(self._input, True)
        cpu.set_position(1, 12)
        cpu.set_position(2, 2)
        cpu.run()
        return cpu.position(0)

    def part_two(self):
        noun = verb = None
        for (n, v) in permutations(range(100), 2):
            cpu = IntCodeCPU(self._input)
            cpu.set_position(1, n)
            cpu.set_position(2, v)
            cpu.run()

            if cpu.position(0) == 19690720:
                noun = n
                verb = v
                break

        return 100 * noun + verb