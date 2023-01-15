from __future__ import annotations
from functools import total_ordering
from typing import Union


@total_ordering
class Interval(object):
    def __init__(self, left: int, right: int):
        self._left = left
        self._right = right

    def __hash__(self):
        return self.left * 13 + self.right * 37

    def __str__(self):
        return f"({self.left}..{self.right})"

    def __eq__(self, other):
        return self.left == other.left and self.right == other.right if issubclass(type(other), Interval) else False

    def __ne__(self, other):
        return self.left != other.left or self.right != other.right if issubclass(type(other), Interval) else False

    def __lt__(self, other):
        return self.left < other.left

    def __le__(self, other):
        return self.left <= other.left

    def __gt__(self, other):
        return self.left > other.left

    def __ge__(self, other):
        return self.left >= other.left

    @property
    def left(self) -> int:
        return self._left

    @property
    def right(self) -> int:
        return self._right

    def overlaps(self, other: Interval):
        return not (self.right < other.left or self._left > other.right)

    def contains(self, other: Union[Interval, int]):
        match other:
            case Interval():
                return (self.left <= other.left and self.right >= other.right) or (other.left <= self._left and other.right >= self.right)
            case int():
                return self.left <= other <= self.right
            case _:
                raise Exception(f"Unsupported type for Interval::contains : {type(other)}")

    def union(self, other: Interval) -> Interval:
        if self.overlaps(other):
            return Interval(min(self.left, other.left), max(self.right, other.right))
        else:
            raise Exception(f"Intervals do not overlap for Interval::union : {self} and {other}")

    def intersect(self, other: Interval) -> Interval:
        if self.overlaps(other):
            return Interval(min(self.left, other.left), max(self.right, other.right))
        else:
            raise Exception(f"Intervals do not overlap for Interval::intersect : {self} and {other}")
