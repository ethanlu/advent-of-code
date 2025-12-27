from __future__ import annotations
from adventofcode.common import Solution
from functools import reduce
from itertools import pairwise
from typing import List, Tuple


class Polymerization(object):
    def __init__(self, template: str, rules: List[str]):
        self._template = template
        self._rules = {}
        for rule in rules:
            pair, insertion = rule.split(' -> ')
            self._rules[pair] = (f"{pair[0]}{insertion}", f"{insertion}{pair[1]}")

    def steps(self, amount: int) -> Tuple[Tuple[str, int], Tuple[str, int]]:
        # store running count of pairs seen as it goes through polymerization
        pairs = {}
        for e1, e2 in pairwise(self._template):
            p = f"{e1}{e2}"
            if p not in pairs:
                pairs[p] = 0
            pairs[p] += 1
        # run polymerazation for the given steps and tally up the counts
        for _ in range(amount):
            next_pairs = {}
            for pair, pair_count in pairs.items():
                for inserted_pair in self._rules[pair]:
                    if inserted_pair not in next_pairs:
                        next_pairs[inserted_pair] = 0
                    next_pairs[inserted_pair] += pair_count
            pairs = next_pairs
        # count elements seen from the pairs and return largest and smallest
        elements = {}
        for pair, pair_amount in pairs.items():
            # only need to count amount of the first element of a pair as the second element will always be part of another pair as the first element
            if pair[0] not in elements:
                elements[pair[0]] = 0
            elements[pair[0]] += pair_amount
        # last element in the input polymer will need to be counted one additional time as it will not be the first element of another pair
        elements[self._template[-1]] += 1

        return (reduce(lambda current, candidate: current if current[1] > candidate[1] else candidate, elements.items(), ('', 0)),
                reduce(lambda current, candidate: candidate if current[1] > candidate[1] else current, elements.items(), ('', 999999999999999)))


class Day14(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        lines = self._load_input_as_lines()
        self._p = Polymerization(lines[0], lines[2:])

    def part_one(self):
        largest, smallest = self._p.steps(10)
        print(f"largest element : {largest[0]} = {str(largest[1])}")
        print(f"smallest element : {smallest[0]} = {str(smallest[1])}")
        return largest[1] - smallest[1]

    def part_two(self):
        largest, smallest = self._p.steps(40)
        print(f"largest element : {largest[0]} = {str(largest[1])}")
        print(f"smallest element : {smallest[0]} = {str(smallest[1])}")
        return largest[1] - smallest[1]
