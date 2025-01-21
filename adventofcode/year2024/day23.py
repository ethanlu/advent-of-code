from __future__ import annotations
from adventofcode.common import Solution
from itertools import combinations
from typing import List, Set


class Day23(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._computers = {}
        for line in self._load_input_as_lines():
            c1, c2 = line.split('-')
            if c1 not in self._computers:
                self._computers[c1] = set([])
            self._computers[c1].add(c2)
            if c2 not in self._computers:
                self._computers[c2] = set([])
            self._computers[c2].add(c1)

    def part_one(self):
        group_size = 3
        groups = []
        # in order to form groups of size group_size, the computers in the group first all must have at least group_size - 1 connections
        for candidate_group in combinations(self._computers.keys(), group_size):
            for candidate_computer in candidate_group:
                # all computers in the candidate group should contain the other members, so the intersection of their connections with the group should be the group_size - 1
                if len(self._computers[candidate_computer].intersection(candidate_group)) != (group_size - 1):
                    break
            else:
                groups.append(sorted(candidate_group))

        count = 0
        for group in sorted(groups):
            for computer in group:
                if computer[0] == 't':
                    print(f"{group} contains t")
                    count += 1
                    break
            else:
                print(f"{group}")
                continue
        return count

    def part_two(self):
        def bron_kerbosch_with_pivot(group: Set[str], remaining: Set[str], exclude: Set[str]) -> Set[str]:
            # https://en.wikipedia.org/wiki/Bron%E2%80%93Kerbosch_algorithm
            if not remaining and not exclude:
                return group

            pivot = remaining.union(exclude).pop()
            found_groups = []
            for next_computer in (remaining - self._computers[pivot]):
                found_groups.append(bron_kerbosch_with_pivot(group.union({next_computer}), remaining.intersection(self._computers[next_computer]), exclude.intersection(self._computers[next_computer])))
                remaining = remaining - {next_computer}
                exclude = exclude.union({next_computer})
            return max(found_groups, default=set([]), key=lambda g: len(g))

        return ','.join(sorted(list(bron_kerbosch_with_pivot(set([]), set(self._computers.keys()), set([])))))
