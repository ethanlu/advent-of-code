from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.range import Interval
from functools import reduce
from typing import List


def repeating_ids(i: Interval, repeat: int) -> List:
    invalids = []
    current = int('0' + str(i.left)[0:len(str(i.left)) // repeat])
    end = int('0' + str(i.right)[0:len(str(i.right)) // repeat]) if len(str(i.left)) == len(str(i.right)) else int(str(i.right)[0:(len(str(i.right)) // repeat) + 1])
    while current <= end:
        s = str(current) * repeat
        if i.contains(int(s)):
            invalids.append(s)
        current += 1
    return invalids


class Day02(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._input = [Interval(int(r.split('-')[0]), int(r.split('-')[1])) for r in self._load_input_as_string().split(',')]

    def part_one(self):
        count = 0
        for i in self._input:
            invalids = repeating_ids(i, 2)

            if invalids:
                print(f"{str(i.left)}-{str(i.right)} has {len(invalids)} invalids : {invalids}")
            count = reduce(lambda t, x: t + int(x), invalids, count)
        return count

    def part_two(self):
        count = 0
        for i in self._input:
            invalids = set([])
            for repeats in range(2, len(str(i.right))+1):
                invalids = invalids.union(set(repeating_ids(i, repeats)))
            if invalids:
                print(f"{str(i.left)}-{str(i.right)} has {len(invalids)} invalids : {invalids}")
            count = reduce(lambda t, x: t + int(x), invalids, count)
        return count
