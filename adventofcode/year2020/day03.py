from __future__ import annotations
from adventofcode.common import Solution
from functools import reduce


class Day03(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._input = self._load_input_as_lines()

    def part_one(self):
        trees = x = y = 0
        while y < len(self._input) - 1:
            y += 1
            x = (x + 3) % len(self._input[y])
            trees += 1 if self._input[y][x] == '#' else 0
        return trees

    def part_two(self):
        all_trees = []
        for delta_x, delta_y in ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2)):
            trees = x = y = 0
            while y < len(self._input) - 1:
                y += delta_y
                x = (x + delta_x) % len(self._input[y])
                trees += 1 if self._input[y][x] == '#' else 0
            all_trees.append(trees)
        return reduce(lambda acc, tree: acc * tree, all_trees)
    