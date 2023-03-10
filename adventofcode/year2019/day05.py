from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.year2019.day02 import IntCodeCPU
from collections import deque
from typing import List


class IntCodeCPUV2(IntCodeCPU):
    def __init__(self, instructions: List[int], verbose: bool = False):
        super().__init__(instructions, verbose)
        self._instructions = [i for i in instructions]
        self._inputs = deque([])
        self._output = 0

    def add_input(self, value: int):
        self._inputs.append(value)

    def get_output(self) -> int:
        return self._output

    def _operation3(self):
        value = self._inputs.popleft()
        if self._verbose:
            print(f"{self._index}: {self._instructions[self._index:(self._index + 2)]} : address[{self._instructions[self._index + 1]}] = {value}")
        self._instructions[self._instructions[self._index + 1]] = value
        self._index += 2

    def _operation4(self):
        if self._verbose:
            print(f"{self._index}: {self._instructions[self._index:(self._index + 2)]} : {self._get_parameter1()}")
            print(f"offset : {self._instructions[self._instructions[self._index + 1]]}")
        self._output = self._get_parameter1()
        self._paused = True
        self._index += 2

    def _operation5(self):
        next_index = self._get_parameter2() if self._get_parameter1() != 0 else self._index + 3
        if self._verbose:
            print(f"{self._index}: {self._instructions[self._index:(self._index + 3)]} : pointer = {next_index}")
        self._index = next_index

    def _operation6(self):
        next_index = self._get_parameter2() if self._get_parameter1() == 0 else self._index + 3
        if self._verbose:
            print(f"{self._index}: {self._instructions[self._index:(self._index + 3)]} : pointer = {next_index}")
        self._index = next_index

    def _operation7(self):
        value = 1 if self._get_parameter1() < self._get_parameter2() else 0
        if self._verbose:
            print(f"{self._index}: {self._instructions[self._index:(self._index + 4)]} : address[{self._instructions[self._index + 3]}] = {value}")
        self._instructions[self._instructions[self._index + 3]] = value
        self._index += 4

    def _operation8(self):
        value = 1 if self._get_parameter1() == self._get_parameter2() else 0
        if self._verbose:
            print(f"{self._index}: {self._instructions[self._index:(self._index + 4)]} : address[{self._instructions[self._index + 3]}] = {value}")
        self._instructions[self._instructions[self._index + 3]] = value
        self._index += 4


class Day05(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._input = [int(i) for i in self._load_input_as_string().split(',')]

    def part_one(self):
        cpu = IntCodeCPUV2(self._input, True)
        cpu.add_input(1)
        outputs = []
        while not cpu.halted:
            cpu.run()
            if not cpu.halted:
                outputs.append(cpu.get_output())
        print(outputs)
        return outputs[-1]

    def part_two(self):
        cpu = IntCodeCPUV2(self._input, True)
        cpu.add_input(5)
        outputs = []
        while not cpu.halted:
            cpu.run()
            if not cpu.halted:
                outputs.append(cpu.get_output())
        print(outputs)
        return outputs[-1]
