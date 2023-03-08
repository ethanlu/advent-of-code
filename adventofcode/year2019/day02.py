from __future__ import annotations
from adventofcode.common import Solution
from itertools import permutations
from typing import List


class IntCodeCPU(object):
    def __init__(self, instructions: List[int]):
        self._instructions = [i for i in instructions]

    def set_position(self, position: int, value: int) -> None:
        self._instructions[position] = value

    def position(self, i: int) -> int:
        return self._instructions[i]

    def run(self) -> None:
        i = 0
        while True:
            match self._instructions[i]:
                case 1:
                    self._instructions[self._instructions[i + 3]] = self._instructions[self._instructions[i + 1]] + self._instructions[self._instructions[i + 2]]
                case 2:
                    self._instructions[self._instructions[i + 3]] = self._instructions[self._instructions[i + 1]] * self._instructions[self._instructions[i + 2]]
                case 99:
                    break
                case _:
                    raise Exception(f"Invalid command {self._instructions[i]} @ {i}")
            i += 4


class Day02(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._input = [int(i) for i in self._load_input_as_string().split(',')]

    def part_one(self):
        cpu = IntCodeCPU(self._input)
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