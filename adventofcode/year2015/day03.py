from itertools import cycle
from adventofcode.common import Solution

from typing import Set


class Day03(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)

        self._directions = self._load_input_as_string()

    def _journey(self, directions) -> Set:
        x = 0
        y = 0
        visited_houses = {(x, y)}
        for d in directions:
            if d == '>':
                x += 1
            elif d == '<':
                x -= 1
            elif d == '^':
                y += 1
            elif d == 'v':
                y -= 1
            else:
                assert False, f"Unrecognized direction : {d}"
            visited_houses.add((x, y))
        return visited_houses

    def part_one(self):
        return len(self._journey(self._directions))

    def part_two(self):
        # use cycle module to alternate between the two direction lists
        direction_list = cycle([[], []])
        list(map(lambda d: next(direction_list).append(d), self._directions))
        return len(self._journey(next(direction_list)).union(self._journey(next(direction_list))))
