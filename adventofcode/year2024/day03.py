from __future__ import annotations
from adventofcode.common import Solution
from functools import reduce

import re


mul_regex = r"mul\((\d{1,3}),(\d{1,3})\)"
do_regex = r"do\(\)"
dont_regex = r"don't\(\)"


class Day03(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._input = self._load_input_as_lines()

    def _find_all_multiply(self, input: str) -> int:
        found = re.findall(mul_regex, input)
        if found:
            return reduce(lambda t, i: t + int(i[0]) * int(i[1]), found, 0)
        else:
            return 0

    def part_one(self):
        return reduce(lambda t, i: t + self._find_all_multiply(i), self._input, 0)

    def part_two(self):
        total = 0
        do_mul = True
        for input in self._input:
            current = input
            while True:
                if do_mul:
                    # when multiple is enabled, find all multiply-commands between current index and next dont-index (if it exists)
                    found = re.search(dont_regex, current)
                    if found:
                        total += self._find_all_multiply(current[:found.span()[1]])
                        current = current[found.span()[1]:]
                        do_mul = False
                    else:
                        # no more dont-commands, so can just get all remaining multiply commands
                        total += self._find_all_multiply(current)
                        break
                else:
                    # when multiple is disabled, find next do-command (if exists) and move current index to that
                    found = re.search(do_regex, current)
                    if found:
                        # move index to after do-command
                        current = current[found.span()[1]:]
                        do_mul = True
                    else:
                        # no more do-commands exist, can ignore all remaining multiply-commands
                        break
        return total
