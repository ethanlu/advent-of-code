from __future__ import annotations
from adventofcode.common import Solution
from collections import deque
from itertools import permutations
from typing import Any, List, Union, Optional
from math import ceil, floor


class SnailfishNumber(object):
    def __init__(self, parent: Optional[SnailfishNumber], data: List[Any]):
        self._parent = parent
        if len(data) != 2:
            raise Exception(f"unexpected pair {data} with length {len(data)}")
        match data[0], data[1]:
            case int(), int():
                self._left = data[0]
                self._right = data[1]
            case int(), list():
                self._left = data[0]
                self._right = SnailfishNumber(self, data[1])
            case int(), SnailfishNumber():
                self._left = data[0]
                self._right = data[1]
                data[1].parent = self
            case list(), int():
                self._left = SnailfishNumber(self, data[0])
                self._right = data[1]
            case SnailfishNumber(), int():
                self._left = data[0]
                data[0].parent = self
                self._right = data[1]
            case list(), list():
                self._left = SnailfishNumber(self, data[0])
                self._right = SnailfishNumber(self, data[1])
            case SnailfishNumber(), SnailfishNumber():
                self._left = data[0]
                data[0].parent = self
                self._right = data[1]
                data[1].parent = self
            case _:
                raise Exception(f"unexpected pair {data} with types {type(data[0])} and {type(data[1])}")

    def __str__(self):
        return f"[{str(self._left)}, {self._right}]"

    def __repr__(self):
        return self.__str__()

    def __add__(self, other):
        match other:
            case SnailfishNumber():
                return SnailfishNumber(None, [self, other])
            case _:
                raise Exception(f"Unsupported SnailfishNumber::add type : {type(other)}")

    @property
    def parent(self) -> Optional[SnailfishNumber]:
        return self._parent

    @parent.setter
    def parent(self, value: Optional[SnailfishNumber]):
        self._parent = value

    @property
    def left(self) -> Union[int, SnailfishNumber]:
        return self._left

    @left.setter
    def left(self, value: Union[int, SnailfishNumber]):
        self._left = value

    @property
    def right(self) -> Union[int, SnailfishNumber]:
        return self._right

    @right.setter
    def right(self, value: Union[int, SnailfishNumber]):
        self._right = value

    @property
    def magnitude(self) -> int:
        match self.left, self.right:
            case int(), int():
                return 3 * self.left + 2 * self.right
            case int(), SnailfishNumber():
                return 3 * self.left + 2 * self.right.magnitude
            case SnailfishNumber(), int():
                return 3 * self.left.magnitude + 2 * self.right
            case SnailfishNumber(), SnailfishNumber():
                return 3 * self.left.magnitude + 2 * self.right.magnitude
            case _:
                raise Exception(f"unexpected pair types : {self}")

    def _regular_left_of(self) -> Optional[SnailfishNumber]:
        root = self
        while root.parent is not None:
            root = root.parent
        found = None
        remaining = deque([root])
        while len(remaining) > 0:
            current = remaining.pop()
            while isinstance(current.left, SnailfishNumber):
                remaining.append(current)
                current = current.left
            if current is self:
                return found
            found = current
            while isinstance(current.right, int) and len(remaining) > 0:
                found = current
                current = remaining.pop()
            if isinstance(current.right, SnailfishNumber):
                remaining.append(current.right)
        return found

    def _regular_right_of(self) -> Optional[SnailfishNumber]:
        root = self
        while root.parent is not None:
            root = root.parent
        found = None
        remaining = deque([root])
        while len(remaining) > 0:
            current = remaining.pop()
            while isinstance(current.right, SnailfishNumber):
                remaining.append(current)
                current = current.right
            if current is self:
                return found
            found = current
            while isinstance(current.left, int) and len(remaining) > 0:
                found = current
                current = remaining.pop()
            if isinstance(current.left, SnailfishNumber):
                remaining.append(current.left)
        return found

    def explodable(self, depth: int = 0) -> Optional[SnailfishNumber]:
        if depth >= 4 and isinstance(self.left, int) and isinstance(self.right, int):
            return self
        if isinstance(self.left, SnailfishNumber):
            found = self.left.explodable(depth + 1)
            if found:
                return found
        if isinstance(self.right, SnailfishNumber):
            found = self.right.explodable(depth + 1)
            if found:
                return found
        return None

    def explode(self) -> None:
        lsn = self._regular_left_of()
        if lsn:
            if isinstance(lsn.right, int):
                lsn.right = lsn.right + self.left
            else:
                lsn.left = lsn.left + self.left
        rsn = self._regular_right_of()
        if rsn:
            if isinstance(rsn.left, int):
                rsn.left = rsn.left + self.right
            else:
                rsn.right = rsn.right + self.right
        if self.parent.left is self:
            self.parent.left = 0
        else:
            self.parent.right = 0

    def splittable(self) -> Optional[SnailfishNumber]:
        if isinstance(self.left, int) and self.left > 9:
            return self
        if isinstance(self.left, SnailfishNumber):
            found = self.left.splittable()
            if found:
                return found
        if isinstance(self.right, int) and self.right > 9:
            return self
        if isinstance(self.right, SnailfishNumber):
            found = self.right.splittable()
            if found:
                return found
        return None

    def split(self) -> None:
        if isinstance(self.left, int) and self.left > 9:
            self.left = SnailfishNumber(self, [floor(self.left / 2), ceil(self.left / 2)])
        else:
            self.right = SnailfishNumber(self, [floor(self.right / 2), ceil(self.right / 2)])

    def reduce(self) -> None:
        while True:
            ex = self.explodable()
            if ex:
                ex.explode()
                continue
            sp = self.splittable()
            if sp:
                sp.split()
                continue
            break


class Day18(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._data = self._load_input_as_lines()

    def part_one(self):
        total = None
        for sn in (SnailfishNumber(None, eval(line)) for line in self._data):
            print(f"{sn}:")
            sn.reduce()
            print(f"\tafter reduction: {sn}")
            if total is None:
                total = sn
            else:
                total += sn
                total.reduce()
            print(f"\tafter addition and reduction : {total}")
        return total.magnitude

    def part_two(self):
        largest = 0
        for a, b in permutations(self._data, 2):
            sna = SnailfishNumber(None, eval(a))
            snb = SnailfishNumber(None, eval(b))
            sna.reduce()
            snb.reduce()
            candidate = sna + snb
            candidate.reduce()
            m = candidate.magnitude
            if m > largest:
                print(f"{a} and {b} yields new largest : {m}")
                largest = m
        return largest
