from __future__ import annotations
from adventofcode.common import Solution


class Day06(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._input = self._load_input_as_lines()

    def part_one(self):
        counts = 0
        yes = set([])
        for answers in self._input:
            if answers == "":
                counts += len(yes)
                yes.clear()
            else:
                yes = yes.union(set(answers))
        counts += len(yes)

        return counts

    def part_two(self):
        counts = 0
        group_yes = None
        for answers in self._input:
            if answers == "":
                counts += len(group_yes)
                group_yes = None
            else:
                if group_yes is None:
                    group_yes = set(answers)
                else:
                    group_yes = group_yes.intersection(set(answers))
        counts += len(group_yes)

        return counts
