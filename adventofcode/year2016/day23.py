from __future__ import annotations
from adventofcode.common import Solution
from copy import copy
from typing import List


class OptimizedCPU(object):
    def __init__(self, instructions: List[str]):
        self._instructions = copy(instructions)
        self._registers = {'a': 0,  'b': 0, 'c': 0, 'd': 0}
        self._verbose = False

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

    @property
    def instructions(self):
        return self._instructions

    def verbose(self, toggle: bool) -> None:
        self._verbose = toggle

    def run(self) -> None:
        index = 0
        while index < len(self._instructions):

            # look ahead to optimize incremental loops
            if index + 4 < len(self._instructions):
                match [self._instructions[index + i].split(' ') for i in range(5)]:
                    case ['inc', x1], ['dec', x2], ['jnz', _, '-2'], ['dec', _], ['jnz', x5, '-5']:
                        # multiplication sequence can be optimized to x1 += x2 * x5
                        self._registers[x1] += self._registers[x2] * self._registers[x5]

                        if self._verbose:
                            print(f"a:{self.a} b:{self.b} c:{self.c} d:{self.d} @ [{index}] optimized 5 instructions to {x1} += {x2} * {x5}")

                        index += 5
                        continue
                    case ['dec', x1], ['inc', x2], ['jnz', _, '-2'], _, _:
                        # copy sequence can be optimized to x2 += x1
                        self._registers[x2] += self._registers[x1]

                        if self._verbose:
                            print(f"a:{self.a} b:{self.b} c:{self.c} d:{self.d} @ [{index}] optimized 3 instructions to {x2} += {x1}")

                        index += 3
                        continue
                    case _:
                        pass

            match self._instructions[index].split(' '):
                case 'cpy', x, y:
                    if y in self._registers:
                        self._registers[y] = self._registers[x] if x in self._registers else int(x)
                    if self._verbose:
                        print(f"a:{self.a} b:{self.b} c:{self.c} d:{self.d} @ [{index}] {self._instructions[index]}")
                    index += 1
                case 'inc', x:
                    if x in self._registers:
                        self._registers[x] += 1
                    if self._verbose:
                        print(f"a:{self.a} b:{self.b} c:{self.c} d:{self.d} @ [{index}] {self._instructions[index]}")
                    index += 1
                case 'dec', x:
                    if x in self._registers:
                        self._registers[x] -= 1
                    if self._verbose:
                        print(f"a:{self.a} b:{self.b} c:{self.c} d:{self.d} @ [{index}] {self._instructions[index]}")
                    index += 1
                case 'jnz', x, y:
                    x = self._registers[x] if x in self._registers else int(x)
                    y = self._registers[y] if y in self._registers else int(y)
                    if self._verbose:
                        print(f"a:{self.a} b:{self.b} c:{self.c} d:{self.d} @ [{index}] {self._instructions[index]}")
                    index += y if x != 0 else 1
                case 'tgl', x:
                    x = self._registers[x] if x in self._registers else int(x)
                    if 0 <= (index + x) < len(self._instructions):
                        match self._instructions[index + x].split(' '):
                            case 'cpy', _, _:
                                self._instructions[index + x] = self._instructions[index + x].replace('cpy', 'jnz')
                            case 'inc', _:
                                self._instructions[index + x] = self._instructions[index + x].replace('inc', 'dec')
                            case 'dec', _:
                                self._instructions[index + x] = self._instructions[index + x].replace('dec', 'inc')
                            case 'jnz', _, _:
                                self._instructions[index + x] = self._instructions[index + x].replace('jnz', 'cpy')
                            case 'tgl', _:
                                self._instructions[index + x] = self._instructions[index + x].replace('tgl', 'inc')
                            case _:
                                raise Exception(f"Unrecognized instruction : {self._instructions[index + x]}")
                    if self._verbose:
                        print(f"a:{self.a} b:{self.b} c:{self.c} d:{self.d} @ [{index}] {self._instructions[index]}")
                    index += 1
                case _:
                    raise Exception(f"Unrecognized instruction : {self._instructions[index]}")


class Day23(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._instructions = self._load_input_as_lines()

    def part_one(self):
        cpu = OptimizedCPU(self._instructions)
        cpu.verbose(True)
        cpu.a = 7
        cpu.run()

        return cpu.a

    def part_two(self):
        cpu = OptimizedCPU(self._instructions)
        cpu.verbose(True)
        cpu.a = 12
        cpu.run()

        return cpu.a
