from __future__ import annotations
from adventofcode.common import Solution
from itertools import cycle

import math, re


regex = re.compile(r"([A-Z]{3}) = \(([A-Z]{3}), ([A-Z]{3})\)")


class Day08(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._moves = []
        self._network = {}
        read_network = False
        for l in self._load_input_as_lines():
            if l == "":
                read_network = True
                continue
            if read_network:
                start, left, right = regex.match(l).groups()
                self._network[start] = {'L': left, 'R': right}
            else:
                self._moves = list(l)

    def part_one(self):
        steps = 0
        moves = cycle(self._moves)
        current = 'AAA'
        while current != 'ZZZ':
            current = self._network[current][next(moves)]
            steps += 1
        return steps

    def part_two(self):
        finished = []
        moves = cycle(self._moves)
        currents = [(k, 0) for k in self._network.keys() if k[2] == 'A']
        while currents:
            next_currents = []
            move = next(moves)
            for current, steps in currents:
                next_current = self._network[current][move]
                next_steps = steps + 1
                if next_current[2] == 'Z':
                    finished.append(next_steps)
                else:
                    next_currents.append((next_current, next_steps))
            currents = next_currents
        return math.lcm(*finished)
