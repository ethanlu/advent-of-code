from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.year2019.day02 import IntCodeCPU
from collections import deque
from typing import List


class IntCodeCPUModified(IntCodeCPU):
    def __init__(self, instructions: List[int], verbose: bool = False):
        super().__init__(instructions, verbose)
        self._inputs = deque([])
        self._output = 0

    @property
    def is_input_empty(self) -> bool:
        return len(self._inputs) == 0

    def add_input(self, value: int):
        self._inputs.append(value)
        self._need_input = False

    def clear_input(self):
        self._inputs.clear()
        self._need_input = True

    def get_output(self) -> int:
        self._has_output = False
        return self._output

    def _operation3(self):
        param1 = self._get_parameter_index(1)
        if len(self._inputs) > 0:
            value = self._inputs.popleft()
            if self._verbose:
                print(f"{self._instruction_index}: {self._memory[self._instruction_index:(self._instruction_index + 2)]} : address[{param1}] = {value}")
            self.write_memory(param1, value)
            self._instruction_index += 2
        else:
            self._need_input = True

    def _operation4(self):
        param1 = self.read_memory(self._get_parameter_index(1))
        if self._verbose:
            print(f"{self._instruction_index}: {self._memory[self._instruction_index:(self._instruction_index + 2)]} : output address[{param1}]")
        self._output = param1
        self._has_output = True
        self._instruction_index += 2

    def _operation5(self):
        param1 = self.read_memory(self._get_parameter_index(1))
        param2 = self.read_memory(self._get_parameter_index(2))
        next_index = param2 if param1 != 0 else self._instruction_index + 3
        if self._verbose:
            print(f"{self._instruction_index}: {self._memory[self._instruction_index:(self._instruction_index + 3)]} : pointer = {next_index}")
        self._instruction_index = next_index

    def _operation6(self):
        param1 = self.read_memory(self._get_parameter_index(1))
        param2 = self.read_memory(self._get_parameter_index(2))
        next_index = param2 if param1 == 0 else self._instruction_index + 3
        if self._verbose:
            print(f"{self._instruction_index}: {self._memory[self._instruction_index:(self._instruction_index + 3)]} : pointer = {next_index}")
        self._instruction_index = next_index

    def _operation7(self):
        param1 = self.read_memory(self._get_parameter_index(1))
        param2 = self.read_memory(self._get_parameter_index(2))
        param3 = self._get_parameter_index(3)
        value = 1 if param1 < param2 else 0
        if self._verbose:
            print(f"{self._instruction_index}: {self._memory[self._instruction_index:(self._instruction_index + 4)]} : address[{param3}] = {value}")
        self.write_memory(param3, value)
        self._instruction_index += 4

    def _operation8(self):
        param1 = self.read_memory(self._get_parameter_index(1))
        param2 = self.read_memory(self._get_parameter_index(2))
        param3 = self._get_parameter_index(3)
        value = 1 if param1 == param2 else 0
        if self._verbose:
            print(f"{self._instruction_index}: {self._memory[self._instruction_index:(self._instruction_index + 4)]} : address[{param3}] = {value}")
        self.write_memory(param3, value)
        self._instruction_index += 4


class Day05(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._input = [int(i) for i in self._load_input_as_string().split(',')]

    def part_one(self):
        cpu = IntCodeCPUModified(self._input, True)
        cpu.add_input(1)
        outputs = []
        while not cpu.halted:
            cpu.run()
            if cpu.has_output:
                outputs.append(cpu.get_output())
        print(outputs)
        return outputs[-1]

    def part_two(self):
        cpu = IntCodeCPUModified(self._input, True)
        cpu.add_input(5)
        outputs = []
        while not cpu.halted:
            cpu.run()
            if cpu.has_output:
                outputs.append(cpu.get_output())
        print(outputs)
        return outputs[-1]
