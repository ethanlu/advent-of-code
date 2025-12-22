from __future__ import annotations
from adventofcode.common import Solution
from collections import deque
from functools import reduce
from typing import Optional, Tuple


close_pairs = {'(': ')', '[': ']', '{': '}', '<': '>'}
illegal_character_score = {')': 3, ']': 57, '}': 1197, '>': 25137}
incomplete_character_score = {')': 1, ']': 2, '}': 3, '>': 4}


def is_valid(chunk: str) -> Tuple[str, Optional[str]]:
    close_order = deque([])
    for c in chunk:
        match c:
            case '(' | '[' | '{' | '<':
                close_order.appendleft(close_pairs[c])
            case ')' | ']' | '}' | '>':
                required_close = close_order.popleft()
                if required_close != c:
                    return required_close, c
            case _:
                raise Exception(f"unexpected character {c} for chunk {chunk}")

    return ''.join(list(close_order)), None


class Day10(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._chunks = self._load_input_as_lines()

    def part_one(self):
        corrupted = {k: 0 for k in illegal_character_score.keys()}
        for chunk in self._chunks:
            expected, actual = is_valid(chunk)
            if actual is not None:
                print(f"{chunk} - expected {expected} but found {actual} instead")
                corrupted[actual] += 1
        return reduce(lambda total, corruption_count: total + illegal_character_score[corruption_count[0]] * corruption_count[1], corrupted.items(), 0)

    def part_two(self):
        scores = []
        for chunk in self._chunks:
            expected, actual = is_valid(chunk)
            if actual is None:
                print(f"{chunk} - complete by adding {expected}")
                scores.append(reduce(lambda total, character: (total * 5) + incomplete_character_score[character], expected, 0))

        return sorted(scores)[len(scores) // 2]
