from __future__ import annotations
from adventofcode.common import Solution
from itertools import permutations
from typing import List


class IntCodeCPU(object):
    def __init__(self, instructions: List[int], verbose: bool = False):
        self._memory = [i for i in instructions]
        self._relative_base = 0
        self._instruction_index = 0
        self._need_input = False
        self._has_output = False

        self._halted = False
        self._verbose = verbose

    @property
    def need_input(self) -> bool:
        return self._need_input

    @property
    def has_output(self) -> bool:
        return self._has_output

    @property
    def halted(self) -> bool:
        return self._halted

    def read_memory(self, index: int):
        if index >= len(self._memory):
            self._memory = self._memory + [0 for _ in range(len(self._memory))]
        return self._memory[index]

    def write_memory(self, index: int, value: int) -> None:
        if index >= len(self._memory):
            self._memory = self._memory + [0 for _ in range(len(self._memory))]
        self._memory[index] = value

    def _get_operation_details(self) -> str:
        return str(self.read_memory(self._instruction_index)).strip('-').zfill(5)

    def _get_parameter_index(self, parameter_index: int) -> int:
        param_mode = int(self._get_operation_details()[-2 - parameter_index])
        match param_mode:
            case 0:
                return self.read_memory(self._instruction_index + parameter_index)
            case 1:
                return self._instruction_index + parameter_index
            case 2:
                return self._relative_base + self.read_memory(self._instruction_index + parameter_index)
            case _:
                raise Exception(f"Invalid parameter mode : {param_mode}")

    def _operation1(self) -> None:
        param1 = self.read_memory(self._get_parameter_index(1))
        param2 = self.read_memory(self._get_parameter_index(2))
        param3 = self._get_parameter_index(3)
        if self._verbose:
            print(f"{self._instruction_index}: {self._memory[self._instruction_index:(self._instruction_index + 4)]} : address[{param3}] = {param1} + {param2}")
        self.write_memory(param3, param1 + param2)
        self._instruction_index += 4

    def _operation2(self) -> None:
        param1 = self.read_memory(self._get_parameter_index(1))
        param2 = self.read_memory(self._get_parameter_index(2))
        param3 = self._get_parameter_index(3)
        if self._verbose:
            print(f"{self._instruction_index}: {self._memory[self._instruction_index:(self._instruction_index + 4)]} : address[{param3}] = {param1} * {param2}")
        self.write_memory(param3, param1 * param2)
        self._instruction_index += 4

    def _operation99(self) -> None:
        self._halted = True

    def run(self) -> None:
        while not self._halted and not self._need_input and not self._has_output:
            opcode = int(self._get_operation_details()[-2:])
            operation = f"_operation{opcode}"
            if hasattr(self, operation):
                getattr(self, operation)()
            else:
                raise Exception(f"Invalid opcode {self._memory[self._instruction_index]} @ {self._instruction_index}")


class Day02(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._input = [int(i) for i in self._load_input_as_string().split(',')]

    def part_one(self):
        cpu = IntCodeCPU(self._input, True)
        cpu.write_memory(1, 12)
        cpu.write_memory(2, 2)
        cpu.run()
        return cpu.read_memory(0)

    def part_two(self):
        noun = verb = None
        for (n, v) in permutations(range(100), 2):
            cpu = IntCodeCPU(self._input)
            cpu.write_memory(1, n)
            cpu.write_memory(2, v)
            cpu.run()

            if cpu.read_memory(0) == 19690720:
                noun = n
                verb = v
                break

        return 100 * noun + verb