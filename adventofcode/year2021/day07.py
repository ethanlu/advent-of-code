from __future__ import annotations
from adventofcode.common import Solution
from typing import Callable, Dict, Tuple


def cheapest_position(positions: Dict[int, int], cost_function: Callable) -> Tuple[int, int]:
    cheapest = 999999999
    cheapest_position = -1
    for candidate_position in range(max(positions.keys()) + 1):
        cost = 0
        for position, amount in positions.items():
            cost += cost_function(candidate_position, position, amount)
        if cost < cheapest:
            cheapest_position = candidate_position
            cheapest = cost
    return cheapest_position, cheapest


class Day07(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._positions = {}
        for p in self._load_input_as_string().split(','):
            position = int(p)
            if position not in self._positions:
                self._positions[position] = 0
            self._positions[position] += 1

    def part_one(self):
        position, cost = cheapest_position(self._positions, lambda cp, p, a: abs(cp - p) * a)
        print(f"cheapest position at {position} with cost of {cost}")
        return cost

    def part_two(self):
        position, cost = cheapest_position(self._positions, lambda cp, p, a: sum(range(1, abs(cp - p) + 1, 1)) * a)
        print(f"cheapest position at {position} with cost of {cost}")
        return cost
