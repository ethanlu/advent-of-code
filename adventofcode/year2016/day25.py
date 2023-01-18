from __future__ import annotations
from adventofcode.common import Solution
from copy import copy
from typing import List

import time


class SignalCPU(object):
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
            if index + 7 < len(self._instructions):
                match [self._instructions[index + i].split(' ') for i in range(8)]:
                    case ['inc', x1], ['dec', x2], ['jnz', _, '-2'], ['dec', _], ['jnz', x5, '-5'], _, _, _:
                        # multiplication sequence can be optimized to x1 += x2 * x5
                        self._registers[x1] += self._registers[x2] * self._registers[x5]

                        if self._verbose:
                            print(f"a:{self.a} b:{self.b} c:{self.c} d:{self.d} @ [{index}] optimized 5 instructions to {x1} += {x2} * {x5}")

                        index += 5
                        continue
                    case ['cpy', '2', y1], ['jnz', x2, '2'], ['jnz', '1', '6'], ['dec', x4], ['dec', x5], ['jnz', x6, '-4'], ['inc', x7], ['jnz', '1', '-7']:
                        # division sequence can be optimized to x7 += x4 // 2
                        self._registers[x7] = self._registers[x4] // 2
                        # y1 will be 1 or 2 depending on if x7 is divisible by 2 or not
                        self._registers[y1] = 2 - self._registers[x4] % 2

                        if self._verbose:
                            print(f"a:{self.a} b:{self.b} c:{self.c} d:{self.d} @ [{index}] optimized 8 instructions to {x7} = {x4} // 2 and {y1} = {x4} % 2 + 2")

                        index += 2
                        continue
                    case _:
                        pass

            match self._instructions[index].split(' '):
                case 'cpy', x, y:
                    self._registers[y] = self._registers[x] if x in self._registers else int(x)
                    if self._verbose:
                        print(f"a:{self.a} b:{self.b} c:{self.c} d:{self.d} @ [{index}] {self._instructions[index]}")
                    index += 1
                case 'inc', x:
                    self._registers[x] += 1
                    if self._verbose:
                        print(f"a:{self.a} b:{self.b} c:{self.c} d:{self.d} @ [{index}] {self._instructions[index]}")
                    index += 1
                case 'dec', x:
                    self._registers[x] -= 1
                    if self._verbose:
                        print(f"a:{self.a} b:{self.b} c:{self.c} d:{self.d} @ [{index}] {self._instructions[index]}")
                    index += 1
                case 'jnz', x, y:
                    x = self._registers[x] if x in self._registers else int(x)
                    if self._verbose:
                        print(f"a:{self.a} b:{self.b} c:{self.c} d:{self.d} @ [{index}] {self._instructions[index]}")
                    index += int(y) if x != 0 else 1
                case 'out', x:
                    print(self._registers[x] if x in self._registers else int(x))
                    time.sleep(1)
                    index += 1
                case _:
                    raise Exception(f"Unrecognized instruction : {self._instructions[index]}")


class Day25(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._instructions = self._load_input_as_lines()

    def part_one(self):
        cpu = SignalCPU(self._instructions)

        # based on input instruction variation, register d = b * c + a. register d is right-shifted (divided by 2) and the shifted bit has to alternate
        # so set a so that b * c + a will have an alternating binary pattern of 10101010101010...
        cpu.a = 2730 - 2541

        print(str(cpu.a))

        cpu.run()

        return cpu.a

    def part_two(self):
        return "ᕕ( ᐛ )ᕗ"
