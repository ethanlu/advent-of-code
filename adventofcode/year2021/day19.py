from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.grid import Point3D
from collections import deque
from itertools import combinations
from typing import List, Set, Tuple


def manhattan_distance(p1: Point3D, p2: Point3D) -> int:
    return abs(p1.x - p2.x) + abs(p1.y - p2.y) + abs(p1.z - p2.z)


def orientations(p: Point3D):
    # https://stackoverflow.com/questions/16452383/how-to-get-all-24-rotations-of-a-3-dimensional-array
    def roll(p: Point3D) -> Point3D: return Point3D(p.x, p.z, -p.y)
    def turn(p: Point3D) -> Point3D: return Point3D(-p.y, p.x, p.z)
    for i in range(2):
        for s in range(3):
            p = roll(p)
            yield p
            for j in range(3):
                p = turn(p)
                yield p
        p = roll(turn(roll(p)))


def fit_scanner(target_beacons: Set[Point3D], candidate: Scanner) -> Tuple[bool, Point3D, Set[Point3D]]:
    for origin in target_beacons:
        for orientated_beacons in candidate.orientated_beacons():
            for ob in orientated_beacons:
                delta = origin - ob
                translated_beacons = set((b + delta for b in orientated_beacons))
                if len(target_beacons.intersection(translated_beacons)) >= 12:
                    return True, delta, target_beacons.union(translated_beacons)
    return False, Point3D(0, 0, 0), target_beacons


class Scanner(object):
    def __init__(self, id: str, data: List[str]):
        self._id = id
        self._beacons = []
        for line in data:
            self._beacons.append(Point3D(*(int(n) for n in line.split(','))))

    @property
    def id(self) -> str:
        return self._id

    @property
    def beacons(self) -> List[Point3D]:
        return self._beacons

    def orientated_beacons(self):
        o = []
        for beacon in self.beacons:
            o.append(orientations(beacon))
        return zip(*o)


class Day19(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._scanners = []
        beacons = []
        name = ''
        for line in self._load_input_as_lines():
            if not line:
                self._scanners.append(Scanner(name, beacons))
                name = ''
                beacons = []
                continue
            if line[0:12] == '--- scanner ':
                name = line[12:-4]
                continue
            beacons.append(line)
        self._scanners.append(Scanner(name, beacons))
        self._fitted_deltas = []

    def part_one(self):
        final_beacons = set(self._scanners[0].beacons)
        remaining = deque(self._scanners[1:])
        while len(remaining) > 0:
            scanner = remaining.popleft()
            fit, delta, new_final_beacons = fit_scanner(final_beacons, scanner)
            if fit:
                final_beacons = new_final_beacons
                self._fitted_deltas.append(delta)
                print(f"scanner #{scanner.id} matched with delta {delta} -> final beacons {len(final_beacons)} with {len(remaining)} scanners remaining")
            else:
                remaining.append(scanner)
        return len(final_beacons)

    def part_two(self):
        largest = 0
        for d1, d2 in combinations(self._fitted_deltas, 2):
            distance = manhattan_distance(d1, d2)
            if distance > largest:
                largest = distance
        return largest
