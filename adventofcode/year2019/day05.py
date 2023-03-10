from __future__ import annotations
from adventofcode.common import Solution
from typing import List


class IntCodeCPUV2(object):
    def __init__(self, instructions: List[int], input: int):
        self._instructions = [i for i in instructions]
        self._input_value = input
        self._output_codes = []

    def set_position(self, position: int, value: int) -> None:
        self._instructions[position] = value

    def position(self, i: int) -> int:
        return self._instructions[i]

    def run(self, verbose: bool) -> List[int]:
        i = 0
        while True:
            parameter0 = str(self._instructions[i]).strip('-').zfill(5)
            opcode = int(parameter0[-2:])
            match opcode:
                case 1:
                    parameter1 = self._instructions[self._instructions[i + 1]] if int(parameter0[-3]) == 0 else self._instructions[i + 1]
                    parameter2 = self._instructions[self._instructions[i + 2]] if int(parameter0[-4]) == 0 else self._instructions[i + 2]
                    if verbose:
                        print(f"{i}: {self._instructions[i:(i + 4)]} : address[{self._instructions[i + 3]}] = {parameter1} + {parameter2}")
                    self._instructions[self._instructions[i + 3]] = parameter1 + parameter2
                    i += 4
                case 2:
                    parameter1 = self._instructions[self._instructions[i + 1]] if int(parameter0[-3]) == 0 else self._instructions[i + 1]
                    parameter2 = self._instructions[self._instructions[i + 2]] if int(parameter0[-4]) == 0 else self._instructions[i + 2]
                    if verbose:
                        print(f"{i}: {self._instructions[i:(i + 4)]} : address[{self._instructions[i + 3]}] = {parameter1} * {parameter2}")
                    self._instructions[self._instructions[i + 3]] = parameter1 * parameter2
                    i += 4
                case 3:
                    if verbose:
                        print(f"{i}: {self._instructions[i:(i + 2)]} : address[{self._instructions[i + 1]}] = {self._input_value}")
                    self._instructions[self._instructions[i + 1]] = self._input_value
                    i += 2
                case 4:
                    parameter1 = self._instructions[self._instructions[i + 1]] if int(parameter0[-3]) == 0 else self._instructions[i + 1]
                    if verbose:
                        print(f"{i}: {self._instructions[i:(i + 2)]} : {parameter1}")
                        print(f"offset : {self._instructions[self._instructions[i + 1]]}")
                    self._output_codes.append(parameter1)
                    i += 2
                case 5:
                    parameter1 = self._instructions[self._instructions[i + 1]] if int(parameter0[-3]) == 0 else self._instructions[i + 1]
                    parameter2 = self._instructions[self._instructions[i + 2]] if int(parameter0[-4]) == 0 else self._instructions[i + 2]
                    i = parameter2 if parameter1 != 0 else i + 3
                    if verbose:
                        print(f"{i}: {self._instructions[i:(i + 3)]} : pointer = {i}")
                case 6:
                    parameter1 = self._instructions[self._instructions[i + 1]] if int(parameter0[-3]) == 0 else self._instructions[i + 1]
                    parameter2 = self._instructions[self._instructions[i + 2]] if int(parameter0[-4]) == 0 else self._instructions[i + 2]
                    i = parameter2 if parameter1 == 0 else i + 3
                    if verbose:
                        print(f"{i}: {self._instructions[i:(i + 3)]} : pointer = {i}")
                case 7:
                    parameter1 = self._instructions[self._instructions[i + 1]] if int(parameter0[-3]) == 0 else self._instructions[i + 1]
                    parameter2 = self._instructions[self._instructions[i + 2]] if int(parameter0[-4]) == 0 else self._instructions[i + 2]
                    self._instructions[self._instructions[i + 3]] = 1 if parameter1 < parameter2 else 0
                    if verbose:
                        print(f"{i}: {self._instructions[i:(i + 4)]} : address[{self._instructions[i + 3]}] = {self._instructions[self._instructions[i + 3]]}")
                    i += 4
                case 8:
                    parameter1 = self._instructions[self._instructions[i + 1]] if int(parameter0[-3]) == 0 else self._instructions[i + 1]
                    parameter2 = self._instructions[self._instructions[i + 2]] if int(parameter0[-4]) == 0 else self._instructions[i + 2]
                    self._instructions[self._instructions[i + 3]] = 1 if parameter1 == parameter2 else 0
                    if verbose:
                        print(f"{i}: {self._instructions[i:(i + 4)]} : address[{self._instructions[i + 3]}] = {self._instructions[self._instructions[i + 3]]}")
                    i += 4
                case 99:
                    break
                case _:
                    raise Exception(f"Invalid command {self._instructions[i]} @ {i}")

        return self._output_codes


class Day05(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._input = [int(i) for i in self._load_input_as_string().split(',')]

    def part_one(self):
        cpu = IntCodeCPUV2(self._input, 1)
        output = cpu.run(True)
        print(output)
        return output[-1]

    def part_two(self):
        cpu = IntCodeCPUV2(self._input, 5)
        output = cpu.run(True)
        print(output)
        return output[-1]
