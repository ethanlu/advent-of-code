from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.year2019.day05 import IntCodeCPUModified
from itertools import permutations
from typing import List


class AmplifierSystem(object):
    def __init__(self, instructions: List[int], amplifiers: int):
        self._amplifiers = [IntCodeCPUModified(instructions) for i in range(amplifiers)]

    def set_phase(self, index: int, phase: int):
        self._amplifiers[index].add_input(phase)

    def run(self, feedback: bool) -> int:
        thruster_input = 0
        amplifier_input = 0
        finished = False
        while not finished:
            for i, amplifier in enumerate(self._amplifiers):
                amplifier.add_input(amplifier_input)
                if not feedback:
                    while not amplifier.halted:
                        amplifier.run()
                else:
                    amplifier.run()
                amplifier_input = amplifier.get_output()

            thruster_input = amplifier_input
            finished = self._amplifiers[-1].halted

        return thruster_input


class Day07(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._input = [int(i) for i in self._load_input_as_string().split(',')]

    def part_one(self):
        best = 0
        for permutation in permutations(range(5), 5):
            ampsys = AmplifierSystem(self._input, 5)
            for i, phase in enumerate(permutation):
                ampsys.set_phase(i, phase)
            output = ampsys.run(False)

            print(f"phase configuration : {permutation} --> {output}")
            if output > best:
                best = output

        return best

    def part_two(self):
        best = 0
        for permutation in permutations(range(5, 10), 5):
            ampsys = AmplifierSystem(self._input, 5)
            for i, phase in enumerate(permutation):
                ampsys.set_phase(i, phase)
            output = ampsys.run(True)

            print(f"phase configuration : {permutation} --> {output}")
            if output > best:
                best = output

        return best