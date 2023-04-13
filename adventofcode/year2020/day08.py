from __future__ import annotations
from adventofcode.common import Solution
from typing import List


class CPU(object):
    def __init__(self, instructions: List[str]):
        self._instructions = instructions
        self._index = 0
        self._value = 0

    @property
    def index(self) -> int:
        return self._index

    @property
    def value(self) -> int:
        return self._value

    @property
    def halted(self) -> bool:
        return not (0 <= self._index < len(self._instructions))

    def step(self):
        match self._instructions[self._index].split(" "):
            case "nop", _:
                self._index += 1
            case "acc", amount:
                self._value += int(amount)
                self._index += 1
            case "jmp", amount:
                self._index += int(amount)


class Day08(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._input = self._load_input_as_lines()

    def part_one(self):
        visited = set([])
        cpu = CPU(self._input)
        value = 0
        while not cpu.halted:
            if cpu.index not in visited:
                visited.add(cpu.index)
                cpu.step()
            else:
                value = cpu.value
                break

        return value

    def part_two(self):
        value = 0
        for change_index in [i for i, instruction in enumerate(self._input) if instruction.split(" ")[0] != "acc"]:
            modified_instructions = [l for l in self._input]
            if modified_instructions[change_index].startswith("nop"):
                modified_instructions[change_index] = modified_instructions[change_index].replace("nop", "jmp")
            else:
                modified_instructions[change_index] = modified_instructions[change_index].replace("jmp", "nop")

            visited = set([])
            cpu = CPU(modified_instructions)
            while not cpu.halted:
                if cpu.index not in visited:
                    visited.add(cpu.index)
                    cpu.step()
                else:
                    break
            else:
                value = cpu.value
                break

        return value
