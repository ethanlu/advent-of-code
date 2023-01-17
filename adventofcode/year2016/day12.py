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
            match self._instructions[index].split(' '):
                case 'cpy', x, y:
                    self._registers[y] = self._registers[x] if x in self._registers else int(x)
                    index += 1
                case 'inc', x:
                    self._registers[x] += 1
                    index += 1
                case 'dec', x:
                    self._registers[x] -= 1
                    index += 1
                case 'jnz', x, y:
                    x = self._registers[x] if x in self._registers else int(x)
                    index += int(y) if x != 0 else 1
                case _:
                    raise Exception(f"Unrecognized instruction : {self._instructions[index]}")


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
