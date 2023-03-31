from __future__ import annotations
from adventofcode.common import Solution
from typing import List


class SpaceCardShuffler(object):
    def __init__(self, size: int):
        self._size: int = size
        self._deck: List[int] = list(range(self._size))

    @property
    def deck(self) -> List[int]:
        return self._deck

    def deal(self) -> None:
        self._deck = list(reversed(self._deck))

    def cut(self, n: int) -> None:
        self._deck = self._deck[n:] + self._deck[0:n]

    def increment(self, n: int) -> None:
        tmp = list(range(self._size))
        for i in range(self._size):
            j = (i * n) % self._size
            tmp[j] = self._deck[i]
        self._deck = tmp


class Day22(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._input = self._load_input_as_lines()

    def part_one(self):
        scf = SpaceCardShuffler(10007)

        for action in self._input:
            match action.split(' '):
                case "deal", "into", "new", "stack":
                    scf.deal()
                case "cut", n:
                    scf.cut(int(n))
                case "deal", "with", "increment", n:
                    scf.increment(int(n))
                case _:
                    raise Exception(f"Unrecognized action : {action}")

        return scf.deck.index(2019)

    def part_two(self):
        size = 119315717514047
        repeat = 101741582076661
        position = 2020

        # https://www.reddit.com/r/adventofcode/comments/ee0rqi/comment/fbtugcu
        a, b = 1, 0
        for action in self._input:
            match action.split(' '):
                case "deal", "into", "new", "stack":
                    a = -a % size
                    b = (size - 1 - b) % size
                case "cut", n:
                    a = a
                    b = (b - int(n)) % size
                case "deal", "with", "increment", n:
                    a = (a * int(n)) % size
                    b = (b * int(n)) % size
                case _:
                    raise Exception(f"Unrecognized action : {action}")

        remainder = (b * pow(1 - a, size - 2, size)) % size

        return ((position - remainder) * pow(a, repeat * (size - 2), size) + remainder) % size
