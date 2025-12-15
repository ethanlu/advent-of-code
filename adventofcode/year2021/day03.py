from __future__ import annotations
from adventofcode.common import Solution
from itertools import chain
from typing import List


class Day03(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._input = [line for line in self._load_input_as_lines()]

    def part_one(self):
        gamma_rate = []
        epsilon_rate = []
        for i in range(len(self._input[0])):
            zero = 0
            one = 0
            for line in self._input:
                zero += 1 if line[i] == '0' else 0
                one += 1 if line[i] == '1' else 0
            gamma_rate.append('1' if one > zero else '0')
            epsilon_rate.append('1' if one < zero else '0')
        return int(''.join(gamma_rate), 2) * int(''.join(epsilon_rate), 2)

    def part_two(self):
        def generator_rating(readings: List[str], is_oxygen: bool = True) -> List[str]:
            remaining = [reading for reading in readings]
            index = 0
            while len(remaining) > 1:
                zero = []
                one = []
                for reading in remaining:
                    match reading[index]:
                        case '0':
                            zero.append(reading)
                        case '1':
                            one.append(reading)
                        case _:
                            raise Exception(f"unexpected digit : {reading[index]}")
                if is_oxygen:
                    if len(one) > len(zero):
                        remaining = one
                    elif len(one) < len(zero):
                        remaining = zero
                    else:
                        remaining = []
                        for reading in chain(zero, one):
                            if reading[index] == '1':
                                remaining.append(reading)
                else:
                    if len(one) < len(zero):
                        remaining = one
                    elif len(one) > len(zero):
                        remaining = zero
                    else:
                        remaining = []
                        for reading in chain(zero, one):
                            if reading[index] == '0':
                                remaining.append(reading)
                index += 1
            return remaining[0]

        oxygen_rating = generator_rating(self._input, True)
        co2_rating = generator_rating(self._input, False)
        return int(''.join(oxygen_rating), 2) * int(''.join(co2_rating), 2)