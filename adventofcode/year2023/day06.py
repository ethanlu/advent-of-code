from __future__ import annotations
from adventofcode.common import Solution
from functools import reduce
from typing import List, Tuple


class BoatRace(object):
    def __init__(self, t:int, d: int, s: int):
        self._time = t
        self._distance = d
        self._speed = s

    @property
    def time(self) -> int:
        return self._time

    @property
    def distance(self) -> int:
        return self._distance

    def solve(self) -> List[Tuple[int, int]]:
        solutions = []
        for t in range(1, self._time - 1):
            d = (self._time - t) * (self._speed * t)
            if d > self._distance:
                solutions.append((t, d))
        return solutions

class Day06(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        input = self._load_input_as_lines()
        self._times = [int(t) for t in input[0][5:].strip().split(' ') if t != '']
        self._distances = [int(d) for d in input[1][9:].strip().split(' ') if d != '']

    def part_one(self):
        solutions = []
        for i, br in enumerate([BoatRace(t, d, 1) for t, d in zip(self._times, self._distances)]):
            s = br.solve()
            solutions.append(len(s))
            print(f"race {i} lasts {br.time} ms and must beat {br.distance} mm : {len(s)} solutions")
        return reduce(lambda x, y: x * y, solutions)

    def part_two(self):
        br = BoatRace(int(''.join((str(n) for n in self._times))), int(''.join((str(n) for n in self._distances))), 1)
        solutions = br.solve()
        print(f"race lasts {br.time} ms and must beat {br.distance} mm : {len(solutions)} solutions")
        return len(solutions)
