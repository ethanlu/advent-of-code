from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.grid import Point3D
from itertools import combinations
from typing import List

import math


class Moon(object):
    def __init__(self, position: Point3D):
        self._position = position
        self._velocity = Point3D(0, 0, 0)

    @property
    def position(self) -> Point3D:
        return self._position

    @property
    def velocity(self) -> Point3D:
        return self._velocity

    def apply_gravity(self, other: Moon) -> Moon:
        delta = other.position - self._position
        x = 0
        if delta.x != 0:
            x = 1 if delta.x > 0 else -1
        y = 0
        if delta.y != 0:
            y = 1 if delta.y > 0 else -1
        z = 0
        if delta.z != 0:
            z = 1 if delta.z > 0 else -1

        self._velocity += Point3D(x, y, z)
        return self

    def apply_velocity(self):
        self._position += self._velocity

    def potential_energy(self) -> int:
        return abs(self._position.x) + abs(self._position.y) + abs(self._position.z)

    def kinetic_energy(self) -> int:
        return abs(self._velocity.x) + abs(self._velocity.y) + abs(self._velocity.z)


class NBodySystem(object):
    def __init__(self, moons: List[Moon]):
        self._moons = moons
        self._steps = 0

    @property
    def moons(self) -> List[Moon]:
        return self._moons

    @property
    def steps(self) -> int:
        return self._steps

    def step(self) -> NBodySystem:
        for (a, b) in combinations(self._moons, 2):
            a.apply_gravity(b)
            b.apply_gravity(a)
        for m in self._moons:
            m.apply_velocity()
        self._steps += 1
        return self


class Day12(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._moons: List[Moon] = []
        for line in self._load_input_as_lines():
            x, y, z = line.strip('<').strip('>').split(', ')
            self._moons.append(Moon(Point3D(int(x.strip('x=')), int(y.strip('y=')), int(z.strip('z=')))))

    def part_one(self):
        nbs = NBodySystem(self._moons)
        while nbs.steps < 1000:
            nbs.step()

        return sum((m.kinetic_energy() * m.potential_energy() for m in nbs.moons))

    def part_two(self):
        nbs = NBodySystem(self._moons)
        properties = ('x', 'y', 'z')
        repeats = [False, False, False]
        periods = [0, 0, 0]
        states = [[(getattr(m.position, properties[0]), getattr(m.velocity, properties[0])) for m in nbs.moons],
                  [(getattr(m.position, properties[1]), getattr(m.velocity, properties[1])) for m in nbs.moons],
                  [(getattr(m.position, properties[2]), getattr(m.velocity, properties[2])) for m in nbs.moons]]

        while not repeats[0] or not repeats[1] or not repeats[2]:
            nbs.step()
            for i in range(3):
                if not repeats[i]:
                    state = [(getattr(m.position, properties[i]), getattr(m.velocity, properties[i])) for m in nbs.moons]
                    if state == states[i]:
                        periods[i] = nbs.steps
                        repeats[i] = True

        print(f"x period = {periods[0]}, y period = {periods[1]}, z period = {periods[2]}")

        return math.lcm(periods[0], periods[1], periods[2])
