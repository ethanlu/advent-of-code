from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.util import roundrobin
from collections import deque
from typing import List


def evaluate_equation(answer: int, operands: List[int], allow_concat: bool = False) -> List[str]:
    remaining = deque([(operands[0], operands[1:], [])])

    while len(remaining):
        partial_answer, remaining_operands, operation_sequence = remaining.popleft()

        if len(remaining_operands):
            # there are still operands remaining, so add to deque with possible operations
            next_operand = remaining_operands[0]
            next_operands = remaining_operands[1:]

            if (partial_answer + next_operand) <= answer:
                remaining.append((partial_answer + next_operand, next_operands, operation_sequence + ['+']))
            if (partial_answer * next_operand) <= answer:
                remaining.append((partial_answer * next_operand, next_operands, operation_sequence + ['*']))
            if allow_concat and (int(str(partial_answer) + str(next_operand))) <= answer:
                remaining.append((int(str(partial_answer) + str(next_operand)), next_operands, operation_sequence + ['||']))
        else:
            # no more operands, check if partial answer matches target answer
            if partial_answer == answer:
                break
    else:
        return []
    return operation_sequence


class Day07(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._input = []
        for line in self._load_input_as_lines():
            answer, operands = line.split(': ')
            self._input.append((int(answer), [int(operand) for operand in operands.split(' ')]))

    def part_one(self):
        total = 0
        for answer, operands in self._input:
            operations = evaluate_equation(answer, operands, False)
            if len(operations):
                print(f"{answer} = {' '.join(roundrobin([str(o) for o in operands], operations))}")
                total += answer
        return total

    def part_two(self):
        total = 0
        for answer, operands in self._input:
            operations = evaluate_equation(answer, operands, True)
            if len(operations):
                print(f"{answer} = {' '.join(roundrobin([str(o) for o in operands], operations))}")
                total += answer
        return total
