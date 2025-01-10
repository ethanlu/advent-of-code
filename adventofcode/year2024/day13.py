from __future__ import annotations
from adventofcode.common import Solution
from itertools import islice, product
from typing import List, Optional

import re


a_regex = re.compile(r'^Button A: X\+(\d+), Y\+(\d+)$')
b_regex = re.compile(r'^Button B: X\+(\d+), Y\+(\d+)$')
p_regex = re.compile(r'^Prize: X=(\d+), Y=(\d+)$')


def batched(iterable, n):
    # https://docs.python.org/3.11/library/itertools.html#itertools-recipes
    if n < 1:
        raise ValueError('n must be at least one')
    it = iter(iterable)
    while batch := tuple(islice(it, n)):
        yield batch


def solve_matrix_equations(matrix: List[List[int]]) -> Optional[List[int]]:
    # gaussian elimination
    for i in range(len(matrix)):
        if matrix[i][i] == 0:
            return None
        matrix[i] = [matrix[i][k] / matrix[i][i] for k in range(len(matrix[i]))]
        for j in range(i + 1, len(matrix)):
            matrix[j] = [matrix[j][k] - matrix[i][k] * matrix[j][i] for k in range(len(matrix[i]))]

    # back substituion
    for i in reversed(range(len(matrix))):
        for j in range(i):
            matrix[j] = [matrix[j][k] - matrix[i][k] * matrix[j][i] for k in range(len(matrix[i]))]

    return [int(round(r[-1], 2)) for r in matrix]


class Day13(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._input = []
        for batches in batched(self._load_input_as_lines(), 4):
            button_a_match = a_regex.match(batches[0])
            button_b_match = b_regex.match(batches[1])
            prize_match = p_regex.match(batches[2])
            self._input.append((
                int(button_a_match.groups()[0]), int(button_a_match.groups()[1]),
                int(button_b_match.groups()[0]), int(button_b_match.groups()[1]),
                int(prize_match.groups()[0]), int(prize_match.groups()[1])
            ))

    def part_one(self):
        total = 0
        for ax, ay, bx, by, x, y in self._input:
            costs = []
            a_presses, b_presses = solve_matrix_equations([[ax, bx, x], [ay, by, y]])
            if 0 <= a_presses <= 100 and 0 <= b_presses <= 100 and x == (a_presses * ax + b_presses * bx) and y == (a_presses * ay + b_presses * by):
                # solution must be positive and no greater than 100. in addition, rounding solution from float to int can produce wrong answer so confirm the solution is valid
                costs.append(a_presses * 3 + b_presses)
            if costs:
                total += sorted(costs)[0]
        return total

    def part_two(self):
        total = 0
        for ax, ay, bx, by, x, y in self._input:
            costs = []
            a_presses, b_presses = solve_matrix_equations([[ax, bx, x + 10000000000000], [ay, by, y + 10000000000000]])
            if 0 <= a_presses and 0 <= b_presses and (x + 10000000000000) == (a_presses * ax + b_presses * bx) and (y + 10000000000000) == (a_presses * ay + b_presses * by):
                # solution must be positive. in addition, rounding solution from float to int can produce wrong answer so confirm the solution is valid
                costs.append(a_presses * 3 + b_presses)
            if costs:
                total += sorted(costs)[0]
        return total
