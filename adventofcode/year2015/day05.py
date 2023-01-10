from adventofcode import Solution

import re


class Day05(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)

        self._strings = list(map(lambda l: l.strip(), self._load_input_as_lines()))

    def part_one(self):
        return len([i for i in self._strings if len(re.findall(r"(ab|cd|pq|xy)", i)) == 0 and len(re.findall(r"[aeiou]", i)) >= 3 and len(re.findall(r"(?P<letter>[a-z])(?P=letter)", i)) >= 1])

    def part_two(self):
        return len([i for i in self._strings if len(re.findall(r"(?P<letter>[a-z][a-z]).*(?P=letter)", i)) >= 1 and len(re.findall(r"(?P<letter>[a-z])[a-z](?P=letter)", i)) >= 1])
