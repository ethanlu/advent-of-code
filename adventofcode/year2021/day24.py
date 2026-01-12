from __future__ import annotations
from adventofcode.common import Solution
from collections import deque
from typing import Dict, List


class ALU(object):
    def __init__(self):
        self._variables = {'w': 0, 'x': 0, 'y': 0, 'z': 0}

    @property
    def variables(self) -> Dict[str, int]:
        return self._variables

    def _evaluate(self, v: str) -> int:
        return self._variables[v] if v in self._variables else int(v)

    def inp(self, a: str, value: str) -> None:
        if a not in self._variables:
            raise Exception(f"unexpected variable {a}")
        self._variables[a] = int(value)

    def add(self, a: str, b: str) -> None:
        self._variables[a] += self._evaluate(b)

    def mul(self, a: str, b: str) -> None:
        self._variables[a] *= self._evaluate(b)

    def div(self, a: str, b: str) -> None:
        if b == '0':
            raise Exception(f"unexpected b value in div operation : {b}")
        self._variables[a] //= self._evaluate(b)

    def mod(self, a: str, b: str) -> None:
        if b == '0':
            raise Exception(f"unexpected b value in mod operation : {b}")
        self._variables[a] %= self._evaluate(b)

    def eql(self, a: str, b: str) -> None:
        self._variables[a] = 1 if self._variables[a] == self._evaluate(b) else 0


class MONAD(object):
    def __init__(self, data: List[str]):
        self._alu = ALU()
        self._instructions = data
        """
        instructions are a set of 18 line instructions repeated 14 times (once for each digit in the model number).
        within each set of 18-instructions though, line 5, 6, and 16 can have a different constant value:
        
        inp w
        mul x 0
        add x z
        mod x 26
        div z z_divider     # the ? on this line will vary
        add x x_adder       # the ? on this line will vary
        eql x w
        eql x 0
        mul y 0
        add y 25
        mul y x
        add y 1
        mul z y
        mul y 0
        add y w
        add y y_adder       # the ? on this line will vary
        mul y x
        add z y
        """
        self._xyz = list(zip(
            # x_adder
            [int(self._instructions[line].split(' ')[-1]) for line in range(5, 18 * 14 + 1, 18)],
            # y_adder
            [int(self._instructions[line].split(' ')[-1]) for line in range(15, 18 * 14 + 1, 18)],
            # z_divider
            [int(self._instructions[line].split(' ')[-1]) for line in range(4, 18 * 14 + 1, 18)]
        ))

    def reset(self) -> None:
        self._alu = ALU()

    def find_model_numbers(self) -> List[int]:
        """
        the instructions can be summarized as:
        if previous_z % 26 + x_adder == w:
            z = previous_z // z_divider
        else:
            z = (previous_z // z_divider) * 26 + w + y_adder

        instead of finding z based on previous z, we start with final z = 0 and work backwards to find all possible previous_z and w value pairs that can yield the final z = 0
        the summarized instruction in reverse would be:

        # when previous_z % 26 + x_adder == w, then previous_z would be:
        previous_z = z * z_divider + K, where K is 0..25

        # when previous_z % 26 + x_adder != w, then previous_z would be:
        previous_z = (z - w - y_adder) // 26 * z_divider + K, where K is 0..25
        """
        solutions = []
        remaining = deque([(0, 13, [])])
        i = 0
        while len(remaining) > 0:
            i += 1
            if i % 100000 == 0:
                print(f"{i}: {len(remaining)}...")
            z, digit_index, digits = remaining.pop()
            if digit_index < 0:
                model_number = int(''.join((str(d) for d in reversed(digits))))
                solutions.append(model_number)
                continue
            x_adder, y_adder, z_divider = self._xyz[digit_index]
            for w in range(1, 10, 1):
                for k in range(26):
                    previous_z = z * z_divider + k
                    if previous_z % 26 + x_adder == w and previous_z // z_divider == z:
                        remaining.append((previous_z, digit_index - 1, digits + [w]))
                    previous_z = (z - w - y_adder) // 26 * z_divider * z_divider + k
                    if previous_z % 26 + x_adder != w and previous_z // z_divider * 26 + w + y_adder == z:
                        remaining.append((previous_z, digit_index - 1, digits + [w]))

        return solutions

    def run(self, model_number: int) -> Dict[str, int]:
        input_data = deque(str(model_number))
        for instruction in self._instructions:
            match instruction.split(' '):
                case 'inp', a:
                    self._alu.inp(a, input_data.popleft())
                case 'add', a, b:
                    self._alu.add(a, b)
                case 'mul', a, b:
                    self._alu.mul(a, b)
                case 'div', a, b:
                    self._alu.div(a, b)
                case 'mod', a, b:
                    self._alu.mod(a, b)
                case 'eql', a, b:
                    self._alu.eql(a, b)
                case _:
                    raise Exception(f"unexpected instruction : {instruction}")
        return self._alu.variables


class Day24(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._instructions = self._load_input_as_lines()
        m = MONAD(self._instructions)
        self._solutions = m.find_model_numbers()

    def part_one(self):
        largest = max(self._solutions)
        m = MONAD(self._instructions)
        variables = m.run(largest)
        print(f"largest model number {largest} yields {variables}")
        return largest

    def part_two(self):
        smallest = min(self._solutions)
        m = MONAD(self._instructions)
        variables = m.run(smallest)
        print(f"smallest model number {smallest} yields {variables}")
        return smallest
