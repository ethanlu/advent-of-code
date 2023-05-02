from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.grid import Point3D
from functools import reduce
from typing import Dict


class ConwayCube(object):
    def __init__(self, initial: Dict[Point3D, str]):
        self._cubes = initial
        self._minx = 0
        self._maxx = reduce(lambda acc, p: acc if acc > p.x else p.x, self._cubes.keys(), 0)
        self._miny = 0
        self._maxy = reduce(lambda acc, p: acc if acc > p.y else p.x, self._cubes.keys(), 0)
        self._minz = 0
        self._maxz = 0

    @property
    def active(self) -> int:
        return sum([1 for s in self._cubes.values() if s == '#'])

    def _active_neighbors(self, p: Point3D) -> int:
        return reduce(
            lambda acc, p: acc + (1 if p in self._cubes and self._cubes[p] == '#' else 0),
            (
                # layer below
                Point3D(p.x - 1, p.y - 1, p.z - 1), Point3D(p.x, p.y - 1, p.z - 1), Point3D(p.x + 1, p.y - 1, p.z - 1),
                Point3D(p.x - 1, p.y, p.z - 1), Point3D(p.x, p.y, p.z - 1), Point3D(p.x + 1, p.y, p.z - 1),
                Point3D(p.x - 1, p.y + 1, p.z - 1), Point3D(p.x, p.y + 1, p.z - 1), Point3D(p.x + 1, p.y + 1, p.z - 1),
                # same layer
                Point3D(p.x - 1, p.y - 1, p.z), Point3D(p.x, p.y - 1, p.z), Point3D(p.x + 1, p.y - 1, p.z),
                Point3D(p.x - 1, p.y, p.z), Point3D(p.x + 1, p.y, p.z),
                Point3D(p.x - 1, p.y + 1, p.z), Point3D(p.x, p.y + 1, p.z), Point3D(p.x + 1, p.y + 1, p.z),
                # layer above
                Point3D(p.x - 1, p.y - 1, p.z + 1), Point3D(p.x, p.y - 1, p.z + 1), Point3D(p.x + 1, p.y - 1, p.z + 1),
                Point3D(p.x - 1, p.y, p.z + 1), Point3D(p.x, p.y, p.z + 1), Point3D(p.x + 1, p.y, p.z + 1),
                Point3D(p.x - 1, p.y + 1, p.z + 1), Point3D(p.x, p.y + 1, p.z + 1), Point3D(p.x + 1, p.y + 1, p.z + 1),
            ),
            0
        )

    def cycle(self) -> None:
        minx = None
        maxx = None
        miny = None
        maxy = None
        minz = None
        maxz = None
        cubes = {}
        for z in range(self._minz - 1, self._maxz + 2):
            for y in range(self._miny - 1, self._maxy + 2):
                for x in range(self._minx - 1, self._maxx + 2):
                    p = Point3D(x, y, z)
                    active_neighbors = self._active_neighbors(p)
                    if p in self._cubes and self._cubes[p] == '#':
                        # active cube
                        cubes[p] = '#' if 2 <= active_neighbors <= 3 else '.'
                    else:
                        # inactive cube
                        cubes[p] = '#' if active_neighbors == 3 else '.'

                    if cubes[p] == '#':
                        # update tracking of min and max ranges whenever an active cube is encountered
                        minx = p.x if minx is None or minx > p.x else minx
                        maxx = p.x if maxx is None or maxx < p.x else maxx
                        miny = p.y if miny is None or miny > p.y else miny
                        maxy = p.y if maxy is None or maxy < p.y else maxy
                        minz = p.z if minz is None or minz > p.z else minz
                        maxz = p.z if maxz is None or maxz < p.z else maxz

        self._cubes = cubes
        self._minx = minx
        self._maxx = maxx
        self._miny = miny
        self._maxy = maxy
        self._minz = minz
        self._maxz = maxz

    def show(self) -> None:
        for z in range(self._minz, self._maxz + 1):
            print(f"\nz={z}")
            for y in range(self._miny, self._maxy + 1):
                row = []
                for x in range(self._minx, self._maxx + 1):
                    p = Point3D(x, y, z)
                    row.append(self._cubes[p])
                print("".join(row))


class ConwayHyperCube(object):
    def __init__(self, initial: Dict[Point3D, str]):
        self._cubes = {0: initial}
        self._minx = 0
        self._maxx = reduce(lambda acc, p: acc if acc > p.x else p.x, self._cubes[0].keys(), 0)
        self._miny = 0
        self._maxy = reduce(lambda acc, p: acc if acc > p.y else p.x, self._cubes[0].keys(), 0)
        self._minz = 0
        self._maxz = 0
        self._minw = 0
        self._maxw = 0

    @property
    def active(self) -> int:
        active = 0
        for w in range(self._minw, self._maxw + 1):
            active += sum([1 for s in self._cubes[w].values() if s == '#'])
        return active

    def _active_neighbors(self, pw: int, p: Point3D) -> int:
        active = 0
        for w in range(pw - 1, pw + 2):
            if w != pw:
                # different hyper layer
                active += reduce(
                    lambda acc, p: acc + (1 if w in self._cubes and p in self._cubes[w] and self._cubes[w][p] == '#' else 0),
                    (
                        # layer below
                        Point3D(p.x - 1, p.y - 1, p.z - 1), Point3D(p.x, p.y - 1, p.z - 1), Point3D(p.x + 1, p.y - 1, p.z - 1),
                        Point3D(p.x - 1, p.y, p.z - 1), Point3D(p.x, p.y, p.z - 1), Point3D(p.x + 1, p.y, p.z - 1),
                        Point3D(p.x - 1, p.y + 1, p.z - 1), Point3D(p.x, p.y + 1, p.z - 1), Point3D(p.x + 1, p.y + 1, p.z - 1),
                        # same layer
                        Point3D(p.x - 1, p.y - 1, p.z), Point3D(p.x, p.y - 1, p.z), Point3D(p.x + 1, p.y - 1, p.z),
                        Point3D(p.x - 1, p.y, p.z), Point3D(p.x, p.y, p.z), Point3D(p.x + 1, p.y, p.z),
                        Point3D(p.x - 1, p.y + 1, p.z), Point3D(p.x, p.y + 1, p.z), Point3D(p.x + 1, p.y + 1, p.z),
                        # layer above
                        Point3D(p.x - 1, p.y - 1, p.z + 1), Point3D(p.x, p.y - 1, p.z + 1), Point3D(p.x + 1, p.y - 1, p.z + 1),
                        Point3D(p.x - 1, p.y, p.z + 1), Point3D(p.x, p.y, p.z + 1), Point3D(p.x + 1, p.y, p.z + 1),
                        Point3D(p.x - 1, p.y + 1, p.z + 1), Point3D(p.x, p.y + 1, p.z + 1), Point3D(p.x + 1, p.y + 1, p.z + 1),
                    ),
                    0
                )
            else:
                # same hyper layer (exclude own cube)
                active += reduce(
                    lambda acc, p: acc + (1 if w in self._cubes and p in self._cubes[w] and self._cubes[w][p] == '#' else 0),
                    (
                        # layer below
                        Point3D(p.x - 1, p.y - 1, p.z - 1), Point3D(p.x, p.y - 1, p.z - 1), Point3D(p.x + 1, p.y - 1, p.z - 1),
                        Point3D(p.x - 1, p.y, p.z - 1), Point3D(p.x, p.y, p.z - 1), Point3D(p.x + 1, p.y, p.z - 1),
                        Point3D(p.x - 1, p.y + 1, p.z - 1), Point3D(p.x, p.y + 1, p.z - 1), Point3D(p.x + 1, p.y + 1, p.z - 1),
                        # same layer
                        Point3D(p.x - 1, p.y - 1, p.z), Point3D(p.x, p.y - 1, p.z), Point3D(p.x + 1, p.y - 1, p.z),
                        Point3D(p.x - 1, p.y, p.z), Point3D(p.x + 1, p.y, p.z),
                        Point3D(p.x - 1, p.y + 1, p.z), Point3D(p.x, p.y + 1, p.z), Point3D(p.x + 1, p.y + 1, p.z),
                        # layer above
                        Point3D(p.x - 1, p.y - 1, p.z + 1), Point3D(p.x, p.y - 1, p.z + 1), Point3D(p.x + 1, p.y - 1, p.z + 1),
                        Point3D(p.x - 1, p.y, p.z + 1), Point3D(p.x, p.y, p.z + 1), Point3D(p.x + 1, p.y, p.z + 1),
                        Point3D(p.x - 1, p.y + 1, p.z + 1), Point3D(p.x, p.y + 1, p.z + 1), Point3D(p.x + 1, p.y + 1, p.z + 1),
                    ),
                    0
                )
        return active

    def cycle(self) -> None:
        minx = None
        maxx = None
        miny = None
        maxy = None
        minz = None
        maxz = None
        minw = None
        maxw = None
        cubes = {}
        for w in range(self._minw - 1, self._maxw + 2):
            cubes[w] = {}
            for z in range(self._minz - 1, self._maxz + 2):
                for y in range(self._miny - 1, self._maxy + 2):
                    for x in range(self._minx - 1, self._maxx + 2):
                        p = Point3D(x, y, z)
                        active_neighbors = self._active_neighbors(w, p)
                        if w in self._cubes and p in self._cubes[w] and self._cubes[w][p] == '#':
                            # active cube
                            cubes[w][p] = '#' if 2 <= active_neighbors <= 3 else '.'
                        else:
                            # inactive cube
                            cubes[w][p] = '#' if active_neighbors == 3 else '.'

                        if cubes[w][p] == '#':
                            # update tracking of min and max ranges whenever an active cube is encountered
                            minx = p.x if minx is None or minx > p.x else minx
                            maxx = p.x if maxx is None or maxx < p.x else maxx
                            miny = p.y if miny is None or miny > p.y else miny
                            maxy = p.y if maxy is None or maxy < p.y else maxy
                            minz = p.z if minz is None or minz > p.z else minz
                            maxz = p.z if maxz is None or maxz < p.z else maxz
                            minw = w if minw is None or minw > w else minw
                            maxw = w if maxw is None or maxw < w else maxw

        self._cubes = cubes
        self._minx = minx
        self._maxx = maxx
        self._miny = miny
        self._maxy = maxy
        self._minz = minz
        self._maxz = maxz
        self._minw = minw
        self._maxw = maxw


class Day17(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._input = {}
        for y, line in enumerate(self._load_input_as_lines()):
            for x, s in enumerate(list(line)):
                p = Point3D(x, y, 0)
                self._input[p] = s

    def part_one(self):
        cc = ConwayCube(self._input)
        for _ in range(6):
            cc.cycle()

        cc.show()
        print("")

        return cc.active

    def part_two(self):
        cc = ConwayHyperCube(self._input)
        for _ in range(6):
            cc.cycle()

        return cc.active
