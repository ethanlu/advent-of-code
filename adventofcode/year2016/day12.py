from __future__ import annotations
from adventofcode.common import Solution
from typing import List


class CPU(object):
    def __init__(self, instructions: List[str]):
        self._instructions = instructions
        self._registers = {'a': 0,  'b': 0, 'c': 0, 'd': 0}

    @property
    def a(self):
        return self._registers['a']

    @a.setter
    def a(self, value: int):
        self._registers['a'] = value

    @property
    def b(self):
        return self._registers['b']

    @b.setter
    def b(self, value: int):
        self._registers['b'] = value

    @property
    def c(self):
        return self._registers['c']

    @c.setter
    def c(self, value: int):
        self._registers['c'] = value

    @property
    def d(self):
        return self._registers['d']

    @d.setter
    def d(self, value: int):
        self._registers['d'] = value

    def run(self) -> None:
        index = 0
        while index < len(self._instructions):
            instruction = self._instructions[index].split(' ')

            match instruction[0]:
                case 'cpy':
                    self._registers[instruction[2]] = self._registers[instruction[1]] if instruction[1] in self._registers else int(instruction[1])
                    index += 1
                case 'inc':
                    self._registers[instruction[1]] += 1
                    index += 1
                case 'dec':
                    self._registers[instruction[1]] -= 1
                    index += 1
                case 'jnz':
                    if instruction[1] in self._registers:
                        index += int(instruction[2]) if self._registers[instruction[1]] != 0 else 1
                    else:
                        index += int(instruction[2]) if int(instruction[1]) != 0 else 1
                case _:
                    raise Exception(f"Unrecognized instruction : {instruction[0]}")


class Day12(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._instructions = self._load_input_as_lines()

    def part_one(self):
        cpu = CPU(self._instructions)
        cpu.run()

        return cpu.a

    def part_two(self):
        cpu = CPU(self._instructions)
        cpu.c = 1
        cpu.run()

        return cpu.a
