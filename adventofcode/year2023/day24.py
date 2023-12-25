from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.grid import Point3D
from adventofcode.common.range import Interval
from itertools import combinations
from random import choice
from typing import Callable, Optional, List, Union


class Hail(object):
    def __init__(self, name: str, position: Point3D, velocity: Point3D):
        self._name = name
        self._position = position
        self._velocity = velocity
        # position (PX, PY, PZ) and velocity (VX, VY, VZ) are x, y, and z variables that form parametric equations in the form:
        # FX(t) = PX + VXt
        # FY(t) = PY + VYt
        # FZ(t) = PZ + VZt
        #
        # rearranged the equation to express t as a function of FX(t), FY(t), and FZ(t) yields:
        # t = (FX(t) - PX) / VX
        # t = (FY(t) - PY) / VY
        # t = (FZ(t) - PZ) / VZ
        self._tx = lambda x: (x - self._position.x) / self._velocity.x
        self._ty = lambda y: (y - self._position.y) / self._velocity.y
        self._tz = lambda z: (z - self._position.z) / self._velocity.z

        # pairs of the above 3 equations yields standard equations in the form Ax + By = C. store the A and B as coefficients and C as constants
        self._xy_coefficients = (self._velocity.y, -self.velocity.x, self._velocity.y * self._position.x - self._velocity.x * self._position.y)
        self._xz_coefficients = (self._velocity.z, -self.velocity.x, self._velocity.z * self._position.x - self._velocity.x * self._position.z)
        self._yz_coefficients = (self._velocity.z, -self.velocity.y, self._velocity.z * self._position.y - self._velocity.y * self._position.z)

    @property
    def name(self) -> str:
        return self._name

    @property
    def position(self) -> Point3D:
        return self._position

    @property
    def velocity(self) -> Point3D:
        return self._velocity

    @property
    def tx(self) -> Callable:
        return self._tx

    @property
    def ty(self) -> Callable:
        return self._ty

    @property
    def tz(self) -> Callable:
        return self._tz

    @property
    def xy_coefficients(self) -> List[int]:
        return list(self._xy_coefficients)

    @property
    def xz_coefficients(self) -> List[int]:
        return list(self._xz_coefficients)

    @property
    def yz_coefficients(self) -> List[int]:
        return list(self._yz_coefficients)


class Day24(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._hails: List[Hail] = []
        for i, l in enumerate(self._load_input_as_lines()):
            t = l.split(' @ ')
            self._hails.append(Hail(
                str(i + 1),
                Point3D(*(int(p) for p in t[0].split(', '))),
                Point3D(*(int(p) for p in t[1].split(', ')))
            ))

    def _solve_matrix_equations(self, matrix: List[List[Union[int, float]]]) -> Optional[List[float]]:
        # gaussian elimination
        for i in range(len(matrix)):
            if matrix[i][i] == 0:
                return None
            matrix[i] = [matrix[i][k] / matrix[i][i] for k in range(len(matrix[i]))]
            for j in range(i + 1, len(matrix)):
                matrix[j] = [matrix[j][k] - matrix[i][k] * matrix[j][i] for k in range(len(matrix[i]))]

        # back substituion
        for i in reversed(range(len(matrix))):
            for j in range(i):
                matrix[j] = [matrix[j][k] - matrix[i][k] * matrix[j][i] for k in range(len(matrix[i]))]

        return [round(r[-1], 2) for r in matrix]

    def part_one(self):
        xy_range = Interval(200000000000000, 400000000000000)
        collisions = 0
        print(f"xy test area : {xy_range}")
        for h1, h2 in combinations(self._hails, 2):
            # for each pair of hail, get their xy coefficients and constants and solve using linear algebra
            solution = self._solve_matrix_equations([h1.xy_coefficients, h2.xy_coefficients])

            if solution is None:
                print(f"{h1.name} and {h2.name} never intersect")
                continue

            x, y = solution
            if not xy_range.contains(x) or not xy_range.contains(y):
                print(f"{h1.name} and {h2.name} intersect at {(x, y)}, but it is outside the test area")
                continue

            if h1.tx(x) < 0 or h1.ty(y) < 0 or h2.tx(x) < 0 or h2.ty(y) < 0:
                print(f"{h1.name} and {h2.name} intersect at {(x, y)}, but in the past")
                continue

            print(f"{h1.name} and {h2.name} solutions at : x = {x}, y = {y}")
            collisions += 1
        return collisions

    def part_two(self):
        def xy_coefficients(h: Hail) -> List[int]:
            return [h.velocity.x, -h.velocity.y, h.position.x, h.position.y, h.position.y * h.velocity.x - h.position.x * h.velocity.y]

        def yz_coefficients(h: Hail) -> List[int]:
            return [h.velocity.y, -h.velocity.z, h.position.y, h.position.z, h.position.z * h.velocity.y - h.position.y * h.velocity.z]

        # solve for xy and yz using 4 hails and a randomly selected hail to calculate the difference the 4 hailstones from the random one
        solution = 0
        for batch in combinations(self._hails, 4):
            random_hail = choice(self._hails)
            xy_matrix = [[a - b for a, b in zip(c, xy_coefficients(random_hail))] for c in [xy_coefficients(h) for h in batch]]
            xy_solve = self._solve_matrix_equations(xy_matrix)
            if xy_solve is None:
                continue

            yz_matrix = [[a - b for a, b in zip(c, yz_coefficients(random_hail))] for c in [yz_coefficients(h) for h in batch]]
            yz_solve = self._solve_matrix_equations(yz_matrix)
            if yz_solve is None:
                continue

            solution = xy_solve[0] + xy_solve[1] + yz_solve[0]
            if solution % 1 == 0.0:
                break

        return int(solution)
