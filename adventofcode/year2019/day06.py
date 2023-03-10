from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.graph import TreeNode
from collections import deque
from functools import cache
from typing import Deque, Dict, List


class OrbitMap(object):
    def __init__(self, orbits: List[str]):
        self._objects = {}
        for orbit in orbits:
            tmp = orbit.split(')')
            if tmp[0] not in self._objects.keys():
                self._objects[tmp[0]] = TreeNode(tmp[0])
            if tmp[1] not in self._objects.keys():
                self._objects[tmp[1]] = TreeNode(tmp[1])
            self._objects[tmp[0]].add_child(self._objects[tmp[1]])

    @property
    def objects(self) -> Dict[str, TreeNode]:
        return self._objects

    @cache
    def total_orbit(self, o: TreeNode) -> int:
        if o.id == 'COM':
            return 0
        else:
            return 1 + self.total_orbit(o.parent)

    def orbits(self, o: TreeNode) -> Deque[TreeNode]:
        orbits = deque([])
        current = o
        while current is not None:
            orbits.appendleft(current)
            current = current.parent
        return orbits


class Day06(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._input = self._load_input_as_lines()

    def part_one(self):
        om = OrbitMap(self._input)
        return sum([om.total_orbit(t[1]) for t in om.objects.items()])

    def part_two(self):
        om = OrbitMap(self._input)
        you = om.orbits(om.objects['YOU'])
        santa = om.orbits(om.objects['SAN'])

        while you.popleft() == santa.popleft():
            pass

        return len(you) + len(santa)
