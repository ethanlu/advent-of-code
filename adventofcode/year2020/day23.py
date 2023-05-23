from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.graph import LinkedListNode, LLN
from collections import deque
from typing import Dict, List

import sys


class CrabCup(object):
    def __init__(self, cups: List[int]):
        self._cups: Dict[str, LinkedListNode] = {}
        self._current = None
        self._min = sys.maxsize
        self._max = 0

        current = None
        for c in cups:
            cup = LinkedListNode(str(c))
            self._cups[cup.id] = cup

            if current:
                current.next = cup
            current = cup
            self._min = c if c < self._min else self._min
            self._max = c if c > self._max else self._max
        self._current = self._cups[str(cups[0])]
        current.next = self._current

    def cup(self, c: int) -> LinkedListNode:
        return self._cups[str(c)]

    def move(self) -> None:
        # pickup next 3 from current
        pickups = (int(self._current.next.id), int(self._current.next.next.id), int(self._current.next.next.next.id))

        # determine next valid destination
        destination = int(self._current.id) - 1 if int(self._current.id) > self._min else self._max
        while destination in pickups:
            destination -= 1
            if destination < self._min:
                destination = self._max

        # remove pickups from the list
        self._current.next = self._cups[str(pickups[2])].next

        # insert pickups in new position after destination
        self._cups[str(pickups[2])].next = self._cups[str(destination)].next
        self._cups[str(destination)].next = self._cups[str(pickups[0])]

        # move current
        self._current = self._current.next


class Day23(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._input = [int(n) for n in list(self._load_input_as_string())]

    def part_one(self):
        cc = CrabCup(self._input)

        for _ in range(100):
            cc.move()

        cups = []
        cup = cc.cup(1).next
        while cup.id != "1":
            cups.append(cup.id)
            cup = cup.next

        return "".join(cups)

    def part_two(self):
        cc = CrabCup(self._input + list(range(10, 1000001)))

        for _ in range(10000000):
            cc.move()

        cup = cc.cup(1)

        return int(cup.next.id) * int(cup.next.next.id)
