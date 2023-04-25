from __future__ import annotations
from adventofcode.common import Solution
from functools import reduce

import sys


class Day13(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        input = self._load_input_as_lines()
        self._estimate = int(input[0])
        self._schedules = input[1].split(",")

    def part_one(self):
        id = sys.maxsize
        shortest = sys.maxsize
        for s in self._schedules:
            if s == "x":
                continue

            schedule = int(s)
            if (self._estimate % schedule) == 0:
                waiting = 0
            else:
                waiting = (((self._estimate // schedule) + 1) * schedule) - self._estimate

            if shortest > waiting:
                shortest = waiting
                id = schedule

        print(f"id : {id}")
        print(f"waiting : {shortest}")

        return id * shortest

    def part_two(self):
        # chinese remainder theorem : https://en.wikipedia.org/wiki/Chinese_remainder_theorem
        congruences = [(i, int(schedule)) for i, schedule in enumerate(self._schedules) if schedule != "x"]
        N = reduce(lambda acc, x: acc * x[1], congruences, 1)

        x = sum([a * (N // n) * pow((N // n), -1, n) for a, n in congruences])

        return N - (x % N)
