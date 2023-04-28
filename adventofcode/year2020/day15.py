from __future__ import annotations
from adventofcode.common import Solution
from typing import Iterable, List


class MemoryGame(object):
    def __init__(self, starting: List[int]):
        self._starting = starting
        self._history = {}
        self._turn = 0

    def _update_history(self, n: int) -> None:
        if n not in self._history:
            self._history[n] = [self._turn]
        if len(self._history[n]) == 1:
            self._history[n].append(self._turn)
        else:
            self._history[n] = [self._history[n][-1], self._turn]

    def numbers(self, max_turn: int) -> Iterable:
        spoken = None
        while self._turn < max_turn:
            if self._turn < len(self._starting):
                spoken = self._starting[self._turn]
            else:
                match len(self._history[spoken]):
                    case 1:
                        spoken = 0
                    case 2:
                        spoken = self._history[spoken][1] - self._history[spoken][0]
                    case _:
                        raise Exception(f"Unexpected history encountered on turn {self._turn} for previously spoken number {spoken}")

            self._update_history(spoken)
            yield spoken
            self._turn += 1
        return spoken


class Day15(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._input = [int(s) for s in self._load_input_as_string().split(",")]

    def part_one(self):
        mg = MemoryGame(self._input)
        *_, last = mg.numbers(2020)

        return last

    def part_two(self):
        mg = MemoryGame(self._input)
        *_, last = mg.numbers(30000000)

        return last
    