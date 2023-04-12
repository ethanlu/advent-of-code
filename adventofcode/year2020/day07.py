from __future__ import annotations
from adventofcode.common import Solution
from collections import deque
from typing import Dict, List, Set, Tuple

import re


class BaggageCheck(object):
    def __init__(self, input: List[str]):
        self._regex = re.compile(r"^(\d+) (.+) bags?\.?$")
        self._rules: Dict[str, List[Tuple[int, str]]] = {}
        self._parents: Dict[str, Set[str]] = {}

        for rule in input:
            parts = rule.split("bags contain")
            color = parts[0].strip()
            bags = parts[1].strip()

            self._rules[color] = []
            if color not in self._parents:
                self._parents[color] = set([])
            if bags != "no other bags.":
                for bag in bags.split(", "):
                    n, c = self._regex.match(bag).groups()
                    self._rules[color].append((int(n), c))

                    if c not in self._parents:
                        self._parents[c] = set([])
                    self._parents[c].add(color)

    def contains(self, color: str) -> List[str]:
        bags = set([])
        remaining = deque(self._parents[color])

        while len(remaining) > 0:
            c = remaining.pop()
            if c not in bags:
                for dependency in self._parents[c]:
                    remaining.append(dependency)
            bags.add(c)

        return list(bags)

    def dependencies(self, color: str, amount: int) -> int:
        bags = 0
        for a, c in self._rules[color]:
            bags += amount * a + self.dependencies(c, amount * a)

        return bags


class Day07(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._bc = BaggageCheck(self._load_input_as_lines())

    def part_one(self):
        return len(self._bc.contains("shiny gold"))

    def part_two(self):
        return self._bc.dependencies("shiny gold", 1)