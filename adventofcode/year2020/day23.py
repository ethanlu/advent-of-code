from __future__ import annotations
from adventofcode.common import Solution
from collections import deque
from typing import List


class CrabCup(object):
    def __init__(self, cups: List[int]):
        self._cups = deque(cups)
        self._min = min(cups)
        self._max = max(cups)

    @property
    def cups(self) -> List[int]:
        return list(self._cups)

    def index(self, c: int) -> int:
        return self._cups.index(c)

    def move(self) -> None:
        current = self._cups.popleft()
        pickups = (self._cups.popleft(), self._cups.popleft(), self._cups.popleft())
        self._cups.appendleft(current)

        destination = current - 1 if current > self._min else self._max
        while destination in pickups:
            destination -= 1
            if destination < self._min:
                destination = self._max

        destination_index = self._cups.index(destination)
        for i, n in enumerate(pickups):
            self._cups.insert(destination_index + 1 + i, n)

        self._cups.rotate(-1)

    def show(self) -> None:
        print(list(self._cups))


class Day23(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._input = [int(n) for n in list(self._load_input_as_string())]

    def part_one(self):
        cc = CrabCup(self._input)

        for _ in range(100):
            cc.move()

        cups = deque(cc.cups)
        cup = cups.popleft()
        while cup != 1:
            cups.append(cup)
            cup = cups.popleft()

        return "".join((str(c) for c in cups))

    def part_two(self):
        return "ᕕ( ᐛ )ᕗ"
