from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.year2019.day05 import IntCodeCPUModified
from typing import List


class IntCodeCPUComplete(IntCodeCPUModified):
    def __init__(self, instructions: List[int], verbose: bool = False):
        super().__init__(instructions, verbose)

    def _operation9(self):
        param1 = self.read_memory(self._get_parameter_index(1))
        if self._verbose:
            print(f"{self._instruction_index}: {self._memory[self._instruction_index:(self._instruction_index + 2)]} : relative base : {self._relative_base} + {param1}")
        self._relative_base += param1
        self._instruction_index += 2


class Day09(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._input = [int(i) for i in self._load_input_as_string().split(',')]

    def part_one(self):
        cpu = IntCodeCPUComplete(self._input, True)
        cpu.add_input(1)
        outputs = []
        while not cpu.halted:
            cpu.run()
            if cpu.has_output:
                outputs.append(cpu.get_output())
        print(outputs)
        return outputs[-1]

    def part_two(self):
        cpu = IntCodeCPUComplete(self._input, False)
        cpu.add_input(2)
        outputs = []
        while not cpu.halted:
            cpu.run()
            if cpu.has_output:
                outputs.append(cpu.get_output())
        print(outputs)
        return outputs[-1]
