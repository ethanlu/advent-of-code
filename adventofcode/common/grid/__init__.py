from __future__ import annotations
from typing import List


class Point2D(object):
    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y

    def __eq__(self, other):
        return self._x == other.x and self._y == other.y if issubclass(type(other), Point2D) else False

    def __ne__(self, other):
        return self._x != other.x or self._y != other.y if issubclass(type(other), Point2D) else True

    def __str__(self):
        return "({x}, {y})".format(x=self._x, y=self._y)

    def __hash__(self):
        return self._x * 13 + self._y * 37

    def __add__(self, other):
        match other:
            case Point2D():
                return Point2D(self._x + other.x, self._y + other.y)
            case tuple():
                return Point2D(self._x + int(other[0]) or 0, self._y + int(other[1]) or 0)
            case int():
                return Point2D(self._x + other, self._y + other)
            case _:
                raise Exception(f"Unsupported Point2D::add type : {type(other)}")

    def __sub__(self, other):
        match other:
            case Point2D():
                return Point2D(self._x - other.x, self._y - other.y)
            case tuple():
                return Point2D(self._x - int(other[0]) or 0, self._y - int(other[1]) or 0)
            case int():
                return Point2D(self._x - other, self._y - other)
            case _:
                raise Exception(f"Unsupported Point2D::sub type : {type(other)}")

    def __mul__(self, other):
        match other:
            case Point2D():
                return Point2D(self._x * other.x, self._y * other.y)
            case tuple():
                return Point2D(self._x * int(other[0]) or 0, self._y * int(other[1]) or 0)
            case int():
                return Point2D(self._x * other, self._y * other)
            case _:
                raise Exception(f"Unsupported Point2D::mul type : {type(other)}")

    def __floordiv__(self, other):
        match other:
            case Point2D():
                return Point2D(self._x // other.x, self._y // other.y)
            case tuple():
                return Point2D(self._x // int(other[0]) or 1, self._y // int(other[1]) or 1)
            case int():
                return Point2D(self._x // other, self._y // other)
            case _:
                raise Exception(f"Unsupported Point2D::floordiv type : {type(other)}")

    def __mod__(self, other):
        match other:
            case Point2D():
                return Point2D(self._x % other.x, self._y % other.y)
            case tuple():
                return Point2D(self._x % int(other[0]) or 1, self._y % int(other[1]) or 1)
            case int():
                return Point2D(self._x % other, self._y % other)
            case _:
                raise Exception(f"Unsupported Point2D::mod type : {type(other)}")

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y


class Point3D(object):
    def __init__(self, x: int, y: int, z: int):
        self._x = x
        self._y = y
        self._z = z

    def __eq__(self, other):
        return self._x == other.x and self._y == other.y and self._z == other.z if issubclass(type(other), Point3D) else False

    def __ne__(self, other):
        return self._x != other.x or self._y != other.y or self._z != other.z if issubclass(type(other), Point3D) else True

    def __str__(self):
        return "({x}, {y}, {z})".format(x=self._x, y=self._y, z=self._z)

    def __hash__(self):
        return self._x * 13 + self._y * 37 + self._z * 47

    def __add__(self, other):
        match other:
            case Point3D():
                return Point3D(self._x + other.x, self._y + other.y, self._z + other.z)
            case tuple():
                return Point3D(self._x + int(other[0]) or 0, self._y + int(other[1]) or 0, self._z + int(other[2]) or 0)
            case int():
                return Point3D(self._x + other, self._y + other, self._z + other)
            case _:
                raise Exception(f"Unsupported Point3D::add type : {type(other)}")

    def __sub__(self, other):
        match other:
            case Point3D():
                return Point3D(self._x - other.x, self._y - other.y, self._z - other.z)
            case tuple():
                return Point3D(self._x - int(other[0]) or 0, self._y - int(other[1]) or 0, self._z - int(other[2]) or 0)
            case int():
                return Point3D(self._x - other, self._y - other, self._z - other)
            case _:
                raise Exception(f"Unsupported Point3D::sub type : {type(other)}")

    def __mul__(self, other):
        match other:
            case Point3D():
                return Point3D(self._x * other.x, self._y * other.y, self._z * other.z)
            case tuple():
                return Point3D(self._x * int(other[0]) or 0, self._y * int(other[1]) or 0, self._z * int(other[2]) or 0)
            case int():
                return Point3D(self._x * other, self._y * other, self._z * other)
            case _:
                raise Exception(f"Unsupported Point3D::add type : {type(other)}")

    def __floordiv__(self, other):
        match other:
            case Point2D():
                return Point3D(self._x // other.x, self._y // other.y, self._z // other.z)
            case tuple():
                return Point3D(self._x // int(other[0]) or 1, self._y // int(other[1]) or 1, self._z // int(other[2]) or 1)
            case int():
                return Point3D(self._x // other, self._y // other, self._z // other)
            case _:
                raise Exception(f"Unsupported Point3D::floordiv type : {type(other)}")

    def __mod__(self, other):
        match other:
            case Point2D():
                return Point3D(self._x % other.x, self._y % other.y, self._z % other.z)
            case tuple():
                return Point3D(self._x % int(other[0]) or 1, self._y % int(other[1]) or 1, self._z % int(other[2]) or 1)
            case int():
                return Point3D(self._x % other, self._y % other, self._z % other)
            case _:
                raise Exception(f"Unsupported Point3D::mod type : {type(other)}")

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def z(self):
        return self._z


class Grid2D(object):
    def __init__(self, id: int, data: List[List[str]]):
        self._id = id
        self._data = data.copy()
        self._size = len(data)

    @property
    def id(self) -> int:
        return self._id

    @property
    def size(self) -> int:
        return self._size

    @property
    def data(self) -> List[List[str]]:
        return self._data

    @property
    def top(self) -> str:
        return "".join(self._data[0])

    @property
    def bottom(self) -> str:
        return "".join(self._data[self._size - 1])

    @property
    def left(self) -> str:
        return "".join((self._data[y][0] for y in range(self._size)))

    @property
    def right(self) -> str:
        return "".join((self._data[y][self._size - 1] for y in range(self._size)))

    def flip(self) -> List[List[str]]:
        return [list(reversed(row)) for row in self._data]

    def rotate(self) -> List[List[str]]:
        data = [["?" for x in range(self._size)] for y in range(self._size)]
        for y in range(self._size):
            for x in range(self._size):
                data[y][x] = self._data[self._size - 1 - x][y]
        return [row for row in data]

    def row(self, row: int) -> List[str]:
        return self._data[row]

    def show(self) -> None:
        for row in self._data:
            print("".join(row))
