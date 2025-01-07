from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.grid import Point2D
from adventofcode.common.util import show_dict_grid
from collections import deque
from typing import List, Set


directions = (Point2D(0, -1), Point2D(1, 0), Point2D(0, 1), Point2D(-1, 0))

class GradualUphillTrail(object):
    def __init__(self, trail_map: TrailMap):
        self._trail_map = trail_map
        self._trailheads = set([])
        self._apexes = set([])
        self._visited = set([])

    @property
    def trailheads(self) -> Set[Point2D]:
        return self._trailheads

    @property
    def visited(self) -> Set[Point2D]:
        return self._visited

    @property
    def score(self) -> int:
        return len(self._apexes)

    def hike(self, start: Point2D) -> None:
        positions = deque([start])
        while len(positions) > 0:
            p = positions.pop()
            self._visited.add(p)

            if self._trail_map.cell(p) == 0:
                # reached trailhead
                self._trailheads.add(p)
            if self._trail_map.cell(p) == 9:
                # reached apex
                self._apexes.add(p)

            for d in directions:
                next_p = p + d
                if not self._trail_map.contains(next_p):
                    # next position is out of bounds
                    continue
                if next_p in self._visited:
                    # next position has already been visited
                    continue
                if self._trail_map.cell(next_p) - self._trail_map.cell(p) != 1:
                    # next position does not increase by a height of 1
                    continue
                positions.append(next_p)


class DistinctGradualUphillTrail(GradualUphillTrail):
    def __init__(self, trail_map: TrailMap):
        super().__init__(trail_map)
        self._trails = []

    @property
    def score(self) -> int:
        return len(self._trails)

    def hike(self, start: Point2D) -> None:
        trails = deque([([start], set([]))])
        while len(trails) > 0:
            trail, trail_visited = trails.pop()
            p = trail[-1]
            self._visited.add(p)
            trail_visited.add(p)

            if self._trail_map.cell(p) == 0:
                # reached trailhead
                self._trailheads.add(p)
            if self._trail_map.cell(p) == 9:
                # reached apex
                self._apexes.add(p)
                self._trails.append(trail)

            for d in directions:
                next_p = p + d
                if not self._trail_map.contains(next_p):
                    # next position is out of bounds
                    continue
                if next_p in trail_visited:
                    # next position has already been visited
                    continue
                if self._trail_map.cell(next_p) - self._trail_map.cell(p) != 1:
                    # next position does not increase by a height of 1
                    continue
                trails.append((trail + [next_p], trail_visited.copy()))


class TrailMap(object):
    def __init__(self, data: List[str]):
        self._grid = {}
        self._trailheads = []
        self._maxy = len(data)
        self._maxx = len(data[0])

        for y, row in enumerate(data):
            for x, cell in enumerate(row):
                p = Point2D(x, y)
                self._grid[p] = int(cell)
                if cell == '0':
                    self._trailheads.append(p)

    @property
    def trailheads(self) -> List[Point2D]:
        return self._trailheads

    def contains(self, position: Point2D) -> bool:
        return position in self._grid

    def cell(self, position: Point2D) -> int:
        return self._grid[position]

    def show(self, trails: Set[Point2D]):
        grid = {}
        for p in self._grid:
            grid[(p.x, p.y)] = str(self._grid[p]) if p in trails else '.'
        show_dict_grid(grid, self._maxx, self._maxy)


class Day10(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._tm = TrailMap(self._load_input_as_lines())

    def part_one(self):
        completed_trailheads = {}
        trails = set([])
        total_score = 0
        for trailhead in self._tm.trailheads:
            if trailhead not in completed_trailheads:
                trail = GradualUphillTrail(self._tm)
                trail.hike(trailhead)
                trails.update(trail.visited)
                for tr in trail.trailheads:
                    completed_trailheads[tr] = trail.score
            total_score += completed_trailheads[trailhead]
        self._tm.show(trails)
        return total_score

    def part_two(self):
        completed_trailheads = {}
        trails = set([])
        total_score = 0
        for trailhead in self._tm.trailheads:
            if trailhead not in completed_trailheads:
                trail = DistinctGradualUphillTrail(self._tm)
                trail.hike(trailhead)
                trails.update(trail.visited)
                for tr in trail.trailheads:
                    completed_trailheads[tr] = trail.score
            total_score += completed_trailheads[trailhead]
        return total_score
