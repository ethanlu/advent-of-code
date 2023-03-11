from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.grid import Point2D
from collections import deque
from heapq import heappush, heappop
from itertools import permutations
from math import acos, gcd, sqrt
from typing import Dict, List, Tuple


class MonitoringStation(object):
    def __init__(self, rows: List[str]):
        self._asteroids: Dict[Point2D, Dict[Point2D, List[Tuple[int, Point2D]]]] = {}
        self._best_asteroid = None
        for y, row in enumerate(rows):
            for x, c in enumerate(row):
                if c == '#':
                    self._asteroids[Point2D(x, y)] = {}

    def _clockwise_order(self, a: Point2D):
        # coordinate order can first be bucketed based on the quadrant they are in
        match a.x >= 0, a.y >= 0:
            case True, False:
                # upper right quadrant ((0, -1) up to (1, 0)) are first in priority
                b = Point2D(0, -1)
                priority = 1
            case True, True:
                # lower right quadrant  ((1, 0) up to (0, 1)) are second in priority
                b = Point2D(1, 0)
                priority = 10
            case False, True:
                # lower left quadrant ((0, -1) up to (-1, 0)) are third in priority
                b = Point2D(0, 1)
                priority = 100
            case False, False:
                # upper left quadrant 4 ((-1, 0) up to (0, 1)) are fourth in priority
                b = Point2D(-1, 0)
                priority = 1000
        # points in same quadrant are then ordered based on the angle between them and reference point b
        return priority + acos((a.x * b.x + a.y * b.y) / (sqrt(a.x * a.x + a.y * a.y) * sqrt(b.x * b.x + b.y * b.y)))

    def find_best_asteroid(self) -> int:
        for a, b in permutations(self._asteroids.keys(), 2):
            delta = b - a
            divisor = gcd(delta.x, delta.y)
            unit_delta = Point2D(delta.x // divisor, delta.y // divisor)
            if unit_delta not in self._asteroids[a].keys():
                # asteroids that have the same unit delta can be stored with priority queue with the priority being the distance
                self._asteroids[a][unit_delta] = []
            heappush(self._asteroids[a][unit_delta], (abs(delta.x) + abs(delta.y), b))

        best_count = 0
        for asteroid, sights in self._asteroids.items():
            sight_count = len(sights.keys())
            if best_count < sight_count:
                best_count = sight_count
                self._best_asteroid = asteroid

        return best_count

    def vaporize(self, limit: int) -> Point2D:
        last_asteroid = None
        vaporized = 0

        sorted_asteroids = deque(sorted([(self._clockwise_order(delta), sights) for delta, sights in self._asteroids[self._best_asteroid].items()]))
        while vaporized < limit:
            lined_sights = sorted_asteroids.popleft()
            last_asteroid = heappop(lined_sights[1])[1]
            vaporized += 1
            if len(lined_sights[1]) > 0:
                # there are still asteroids in the line of sight...so add it back to the asteroid list for the next laser sweep
                sorted_asteroids.append(lined_sights)

        return last_asteroid


class Day10(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._monitoring_system = MonitoringStation(self._load_input_as_lines())

    def part_one(self):
        return self._monitoring_system.find_best_asteroid()

    def part_two(self):
        asteroid = self._monitoring_system.vaporize(200)
        return asteroid.x * 100 + asteroid.y