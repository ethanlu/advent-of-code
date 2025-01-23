from __future__ import annotations
from adventofcode.common import Solution
from itertools import combinations
from typing import List

import re


regex = re.compile(r"^(\w{3})\s(AND|OR|XOR)\s(\w{3}) -> (\w{3})$")


def wire_name(name: str, digit: int) -> str:
    return f"{name}{digit:02}"


class Adder(object):
    '''https://en.wikipedia.org/wiki/Adder_(electronics)'''
    def __init__(self, data: List[str]):
        self._wires = {}
        reading_initial_wires = True
        for line in data:
            if not line:
                reading_initial_wires = False
                continue
            if reading_initial_wires:
                wire, value = line.split(': ')
                self._wires[wire] = True if value == '1' else False
            else:
                m = regex.match(line)
                self._wires[m.groups()[3]] = (m.groups()[0], m.groups()[1], m.groups()[2])

    @property
    def output(self) -> List[int]:
        return [int(self.value(w)) for w in reversed(sorted((wire for wire, value in self._wires.items() if wire[0] == 'z' and type(value) is tuple)))]

    @property
    def gate_outputs(self) -> List[str]:
        return [wire for wire, value in self._wires.items() if type(value) is tuple]

    def dependent_outputs(self, wire: str) -> List[str]:
        match self._wires[wire]:
            case True | False:
                return []
            case w1, _, w2:
                return [wire] + self.dependent_outputs(w1) + self.dependent_outputs(w2)
            case _:
                raise Exception(f"unexpected wire : {wire}")

    def value(self, wire: str) -> bool:
        match self._wires[wire]:
            case True | False:
                return self._wires[wire]
            case w1, gate, w2:
                match gate:
                    case 'AND':
                        return self.value(w1) and self.value(w2)
                    case 'OR':
                        return self.value(w1) or self.value(w2)
                    case 'XOR':
                        return self.value(w1) != self.value(w2)
                    case _:
                        raise Exception(f"unexpected gate : {gate}")
            case _:
                raise Exception(f"unexpected wire : {wire}")

    def show(self, wire: str, level: int = 0) -> None:
        match self._wires[wire]:
            case True | False:
                print(f"{'  ' * level}{wire}")
            case w1, gate, w2:
                match gate:
                    case 'AND':
                        print(f"{'  ' * level}{wire} = {w1} AND {w2}")
                        self.show(w1, level + 1)
                        self.show(w2, level + 1)
                    case 'OR':
                        print(f"{'  ' * level}{wire} = {w1} OR {w2}")
                        self.show(w1, level + 1)
                        self.show(w2, level + 1)
                    case 'XOR':
                        print(f"{'  ' * level}{wire} = {w1} XOR {w2}")
                        self.show(w1, level + 1)
                        self.show(w2, level + 1)
                    case _:
                        raise Exception(f"unexpected gate : {gate}")
            case _:
                raise Exception(f"unexpected wire : {wire}")

    def swap(self, w1: str, w2: str) -> None:
        self._wires[w1], self._wires[w2] = self._wires[w2], self._wires[w1]

    def _is_half_adder_output(self, w: str, d: int) -> bool:
        if type(self._wires[w]) is not tuple:
            return False
        a, g, b = self._wires[w]
        return g == 'XOR' and ((a == wire_name('x', d) and b == wire_name('y', d)) or (a == wire_name('y', d) and b == wire_name('x', d)))

    def _is_half_adder_carry(self, w: str, d: int) -> bool:
        if type(self._wires[w]) is not tuple:
            return False
        a, g, b = self._wires[w]
        return g == 'AND' and ((a == wire_name('x', d) and b == wire_name('y', d)) or (a == wire_name('y', d) and b == wire_name('x', d)))

    def _is_full_adder_output(self, w: str, d: int) -> bool:
        if type(self._wires[w]) is not tuple:
            return False
        a, g, b = self._wires[w]
        if d == 1:
            return g == 'XOR' and ((self._is_half_adder_output(a, d) and self._is_half_adder_carry(b, d - 1)) or (self._is_half_adder_carry(a, d - 1) and self._is_half_adder_output(b, d)))
        else:
            return g == 'XOR' and ((self._is_half_adder_output(a, d) and self._is_full_adder_carry(b, d - 1)) or (self._is_full_adder_carry(a, d - 1) and self._is_half_adder_output(b, d)))

    def _is_full_adder_intermediate(self, w: str, d: int) -> bool:
        if type(self._wires[w]) is not tuple:
            return False
        a, g, b = self._wires[w]
        if d == 1:
            return g == 'AND' and ((self._is_half_adder_output(a, d) and self._is_half_adder_carry(b, d - 1)) or (self._is_half_adder_carry(a, d - 1) and self._is_half_adder_output(b, d)))
        else:
            return g == 'AND' and ((self._is_half_adder_output(a, d) and self._is_full_adder_carry(b, d - 1)) or (self._is_full_adder_carry(a, d - 1) and self._is_half_adder_output(b, d)))

    def _is_full_adder_carry(self, w: str, d: int) -> bool:
        if type(self._wires[w]) is not tuple:
            return False
        a, g, b = self._wires[w]
        return g == 'OR' and ((self._is_half_adder_carry(a, d) and self._is_full_adder_intermediate(b, d)) or (self._is_full_adder_intermediate(a, d) and self._is_half_adder_carry(b, d)))

    def checksum(self, digit: int) -> bool:
        match digit:
            case 0:
                # right-most digit output is half adder
                return self._is_half_adder_output(wire_name('z', digit), digit)
            case 1:
                # second right-most digit output is special case full adder that uses half adder carry
                return self._is_full_adder_output(wire_name('z', digit), digit)
            case 45:
                # last digit output is just the carry output from the last full adder
                return self._is_full_adder_carry(wire_name('z', digit), digit - 1)
            case _:
                # all digits in between are full adders with full adder carries
                return self._is_full_adder_output(wire_name('z', digit), digit)


class Day24(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._adder = Adder(self._load_input_as_lines())

    def part_one(self):
        return int(''.join((str(d) for d in self._adder.output)), 2)

    def part_two(self):
        digit = 0
        errors = []
        all_outputs = set(self._adder.gate_outputs)
        good_outputs = set([])
        while digit < len(self._adder.output):
            valid = self._adder.checksum(digit)
            if not valid:
                # reached a digit that failed checksum...generate all possible wire swaps with remaining unknown wires and try until it passes
                #self._adder.show(wire_name('z', digit))
                for w1, w2 in combinations(all_outputs - good_outputs, 2):
                    self._adder.swap(w1, w2)
                    if self._adder.checksum(digit):
                        print(f"digit {digit} : swapped {w1} and {w2}")
                        errors += [w1] + [w2]
                        break
                    else:
                        self._adder.swap(w1, w2)
                else:
                    raise Exception(f"unexpected correction attempt at digit {digit}")
            good_outputs.update(self._adder.dependent_outputs(wire_name('z', digit)))
            digit += 1
        return ','.join(sorted(errors))
