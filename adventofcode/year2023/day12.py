from __future__ import annotations
from adventofcode.common import Solution
from functools import cache
from typing import List, Tuple

import re


good_springs_regex = re.compile(r"^(\.+)")


class SpringRecord(object):
    def __init__(self, row: str, damaged: List[int]):
        self._row = row
        self._damaged = damaged

    @property
    def row(self) -> str:
        return self._row

    @property
    def damaged(self) -> List[int]:
        return self._damaged

    def arrangements(self) -> int:
        @cache
        def find_fit(row: str, damaged: Tuple[int]) -> int:
            if not row:
                return 1 if not damaged else 0
            if not damaged:
                return 1 if '#' not in row else 0

            # case 1: if row starts with a sequence of good springs, we can skip them and move to the first unknown or bad spring
            gm = good_springs_regex.search(row)
            if gm:
                return find_fit(row[len(gm.group()):], damaged)

            # from this point, the first spring in the row is either bad or unknown springs
            results = 0

            # case 2: first spring is unknown, but we treat it as good
            if row[0] == '?':
                results += find_fit(row[1:], damaged)

            # case 3: first spring is bad or is unknown, but we treat it as bad
            # damage can fit if row contains correct number of ? or # followed by possible good spring (. or ?) or nothing at all
            d = damaged[0]
            m = re.search(r"^([#?]{" + str(d) + r"})(\.|\?|$)", row)
            if m:
                results += find_fit(row[len(m.group()):], damaged[1:])

            return results
        return find_fit(self._row, tuple(self._damaged))

class Day12(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._data = []
        for l in self._load_input_as_lines():
            t = l.split(' ')
            self._data.append((t[0], [int(n) for n in t[1].split(',')]))

    def part_one(self):
        total = 0
        for data in self._data:
            record = SpringRecord(data[0], data[1])
            arrangements = record.arrangements()
            #print(f"{record.row} {record.damaged} has {arrangements} possible damaged arrangements")
            total += arrangements
        return total

    def part_two(self):
        unfold = 5
        total = 0
        for data in self._data:
            record = SpringRecord("?".join((data[0] for _ in range(unfold))), data[1] * unfold)
            arrangements = record.arrangements()
            #print(f"{record.row} {record.damaged} has {arrangements} possible damaged arrangements")
            total += arrangements
        return total
