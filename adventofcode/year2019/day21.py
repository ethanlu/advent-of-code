from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.year2019.day09 import IntCodeCPUComplete
from typing import List


class SpringBot(object):
    def __init__(self, program: List[int]):
        self._cpu = IntCodeCPUComplete(program)
        self._output = []

    def _compile(self, spring_script: List[str]) -> List[int]:
        return [ord(c) for c in "".join([f"{line}\n" for line in spring_script])]

    def run(self, spring_script: List[str]) -> int:
        for c in self._compile(spring_script):
            self._cpu.add_input(c)

        damage = 0
        while not self._cpu.halted:
            self._cpu.run()
            o = self._cpu.get_output()

            if o > 127:
                damage = o
            else:
                self._output.append(o)

        return damage

    def show(self) -> None:
        s = []
        for n in self._output:
            s.append(chr(n))
        print("".join(s))


class Day21(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._input = [int(i) for i in self._load_input_as_string().split(',')]

    def part_one(self):
        sb = SpringBot(self._input)
        response = sb.run([
            # jump if next step is hole
            "NOT A J",
            # jump if third step is hole and fourth step is ground (so we land on fourth step)
            "NOT C T",
            "AND D T",
            "OR T J",
            # execute program
            "WALK"
        ])
        sb.show()
        return response

    def part_two(self):
        sb = SpringBot(self._input)
        response = sb.run([
            # jump if next step is hole
            "NOT A J",
            # jump if second step is hole and fourth step is ground
            "NOT B T",
            "AND D T",
            "OR T J",
            # jump if third step is hole and fourth and eigth steps are ground
            "NOT C T",
            "AND D T",
            "AND H T",
            "OR T J",
            # execute program
            "RUN"
        ])
        sb.show()
        return response