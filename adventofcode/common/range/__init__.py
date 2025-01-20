from __future__ import annotations
from adventofcode.common.grid import Point2D
from functools import total_ordering
from typing import Union


@total_ordering
class Interval(object):
    def __init__(self, left: Union[int, float], right: Union[int, float]):
        if type(left) != type(right):
            raise Exception(f"Interval range must be same type. {left} and {right} are incompatible")
        self._left = left
        self._right = right

    def __hash__(self):
        return int(self.left * 13 + self.right * 37)

    def __str__(self):
        return f"({self.left}..{self.right})"

    def __eq__(self, other):
        return self.left == other.left and self.right == other.right if issubclass(type(other), Interval) else False

    def __ne__(self, other):
        return self.left != other.left or self.right != other.right if issubclass(type(other), Interval) else True

    def __lt__(self, other):
        return self.left < other.left

    def __le__(self, other):
        return self.left <= other.left

    def __gt__(self, other):
        return self.left > other.left

    def __ge__(self, other):
        return self.left >= other.left

    @property
    def left(self) -> Union[int, float]:
        return self._left

    @property
    def right(self) -> Union[int, float]:
        return self._right

    def overlaps(self, other: Interval):
        return self._left <= other.right and self.right >= other.left

    def contains(self, other: Union[Interval, int, float]):
        match other:
            case Interval():
                return self.left <= other.left and self.right >= other.right
            case int():
                return self.left <= other <= self.right
            case float():
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
            return Interval(max(self.left, other.left), min(self.right, other.right))
        else:
            raise Exception(f"Intervals do not overlap for Interval::intersect : {self} and {other}")


class Box2D(object):
    def __init__(self, top_left: Point2D, bottom_right: Point2D):
        self._top_left = top_left
        self._bottom_right = bottom_right
        self._top_right = Point2D(self._bottom_right.x, self._top_left.y)
        self._bottom_left = Point2D(self._top_left.x, self._bottom_right.y)

        self._width = abs(self._top_right.x - self._bottom_left.x)
        self._height = abs(self._top_left.y - self._bottom_right.y)

        self._x_interval = Interval(min(self._top_left.x, self._bottom_right.x), max(self._top_left.x, self._bottom_right.x))
        self._y_interval = Interval(min(self._top_left.y, self._bottom_right.y), max(self._top_left.y, self._bottom_right.y))

    def __hash__(self):
        return self._top_left.x * self._top_left.y * 13 + self._bottom_right.x * self._bottom_right.y * 37

    @property
    def top_left(self) -> Point2D:
        return self._top_left

    @property
    def bottom_right(self) -> Point2D:
        return self._bottom_right

    @property
    def bottom_left(self) -> Point2D:
        return self._bottom_left

    @property
    def top_right(self) -> Point2D:
        return self._top_right

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    def overlap(self, other: Box2D) -> bool:
        return self._x_interval.overlaps(other._x_interval) and self._y_interval.overlaps(other._y_interval)

    def contains(self, other: Union[Box2D, Point2D]):
        match other:
            case Box2D():
                return self.contains(other.top_left) and self.contains(other.top_right) and self.contains(other.bottom_right) and self.contains(other.bottom_left)
            case Point2D():
                return self._x_interval.contains(other.x) and self._y_interval.contains(other.y)
            case _:
                raise Exception(f"Unsupported type for Box2D::contains : {type(other)}")
