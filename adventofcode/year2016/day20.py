from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.range import Interval
from itertools import pairwise
from typing import List


class Firewall(object):
    def __init__(self, addresses: List[List[str]]):
        self._addresses: List[Interval] = []

        merged_addresses = Interval(0, 0)
        for address in sorted((Interval(int(address[0]), int(address[1])) for address in addresses)):
            if merged_addresses.overlaps(address):
                merged_addresses = merged_addresses.union(address)
            elif address.contains(merged_addresses.right + 1):
                merged_addresses = Interval(merged_addresses.left, address.right)
            else:
                self._addresses.append(merged_addresses)
                merged_addresses = address
        self._addresses.append(merged_addresses)

    @property
    def addresses(self):
        return self._addresses


class Day20(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._input = [line.split('-') for line in self._load_input_as_lines()]

    def part_one(self):
        fw = Firewall(self._input)
        print(f"{fw.addresses[0]} and {fw.addresses[1]} ---> {fw.addresses[0].right + 1}")
        unblocked = fw.addresses[0].right + 1

        return unblocked

    def part_two(self):
        fw = Firewall(self._input)

        total_unblocked = 0
        for (a, b) in pairwise(fw.addresses):
            print(f"{a} and {b} ---> {b.left - a.right - 1} unblocked")
            total_unblocked += b.left - a.right - 1
        total_unblocked += 4294967295 - fw.addresses[-1].right

        return total_unblocked
