from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.range import Interval
from typing import List, Optional, Tuple

import re


regex = re.compile(r"(on|off)\sx=(\-?\d+)\.\.(\-?\d+),y=(\-?\d+)\.\.(\-?\d+),z=(\-?\d+)\.\.(\-?\d+)")


class Cuboid(object):
    def __init__(self, x: Tuple[int, int], y: Tuple[int, int], z: Tuple[int, int], state: bool):
        self._xr = Interval(min(x), max(x))
        self._yr = Interval(min(y), max(y))
        self._zr = Interval(min(z), max(z))
        self._state = state

    @property
    def state(self) -> bool:
        return self._state

    @property
    def within_region(self) -> bool:
        return all((-50 <= i.left <= 50 and -50 <= i.right <= 50 for i in (self._xr, self._yr, self._zr)))

    @property
    def size(self) -> int:
        return (abs(self._xr.right - self._xr.left) + 1) * (abs(self._yr.right - self._yr.left) + 1) * (abs(self._zr.right - self._zr.left) + 1)

    def intersection(self, other: Cuboid, state: bool) -> Optional[Cuboid]:
        try:
            xi, yi, zi = self._xr.intersect(other._xr), self._yr.intersect(other._yr), self._zr.intersect(other._zr)
            return Cuboid((xi.left, xi.right), (yi.left, yi.right), (zi.left, zi.right), state)
        except Exception:
            pass


def net_volume(target: Cuboid, other: List[Cuboid]) -> int:
    intersections = []
    for cuboid in other:
        intersected_cuboid = target.intersection(cuboid, cuboid.state)
        if intersected_cuboid is not None:
            # target cuboid has an intersection
            intersections.append(intersected_cuboid)
    # net volume is the volume of target cuboid minus the net volume of all intersects cuboids
    return target.size - sum(net_volume(ic, intersections[(i + 1):]) for i, ic in enumerate(intersections))


class Day22(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._cuboids = []
        for line in self._load_input_as_lines():
            m = re.match(regex, line)
            if not m:
                raise Exception(f"unexpected pattern : {line}")
            self._cuboids.append(Cuboid(
                (int(m.groups()[1]), int(m.groups()[2])),
                (int(m.groups()[3]), int(m.groups()[4])),
                (int(m.groups()[5]), int(m.groups()[6])),
                True if m.groups()[0] == 'on' else False
            ))

    def part_one(self):
        cuboids = [c for c in self._cuboids if c.within_region]
        return sum([net_volume(c, cuboids[(i + 1):]) for i, c in enumerate(cuboids) if c.state])

    def part_two(self):
        return sum([net_volume(c, self._cuboids[(i + 1):]) for i, c in enumerate(self._cuboids) if c.state])
