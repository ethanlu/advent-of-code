from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.graph.search import AStar, SearchState, S
from adventofcode.common.grid import Point2D
from adventofcode.common.util import show_grid
from functools import reduce
from typing import Dict, List, Set


class Cubicles(object):
    SPACE = ' '
    WALL = '#'

    def __init__(self, start: Point2D, favorite_number: int):
        self._memoized: Dict[Point2D, str] = {start: self.SPACE}
        self._favorite_number = favorite_number
        self._mx = 0
        self._my = 0

    def grid(self, path: Set[Point2D]):
        return [['O' if Point2D(x, y) in path else self._memoized[Point2D(x, y)] if Point2D(x, y) in self._memoized else '?' for x in range(0, self._mx)] for y in range(0, self._my)]

    def lookup(self, p: Point2D) -> str:
        if p not in self._memoized:
            # calculate the position and memoize for future use
            if reduce(lambda acc, x: acc + int(x), '{n:b}'.format(n=(p.x * p.x + 3 * p.x + 2 * p.x * p.y + p.y + p.y * p.y + self._favorite_number)), 0) % 2 == 0:
                self._memoized[p] = self.SPACE
            else:
                self._memoized[p] = self.WALL

        return self._memoized[p]

    def open_spaces(self, position: Point2D) -> List[Point2D]:
        spaces = []
        for p in (position + (1, 0), position + (-1, 0), position + (0, 1), position + (0, -1)):
            self._mx = self._mx if self._mx > p.x else p.x
            self._my = self._my if self._my > p.y else p.y

            if p.x < 0 or p.y < 0:
                continue

            if self.lookup(p) == self.SPACE:
                spaces.append(p)

        return spaces


class MazeSearchState(SearchState):
    def __init__(self, cubicles: Cubicles, position: Point2D, target: Point2D, gain: int, cost: int):
        super().__init__(str(position), gain, cost)
        self._cubicles = cubicles
        self._position = position
        self._target = target

    @property
    def position(self):
        return self._position

    @property
    def potential_gain(self) -> int:
        return abs(self._position.x - self._target.x) + abs(self._position.y - self._target.y)

    def next_search_states(self) -> List[S]:
        return [MazeSearchState(self._cubicles, p, self._target, self.gain, self.cost + 1) for p in self._cubicles.open_spaces(self._position)]


class Day13(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._input = int(self._load_input_as_string())

    def part_one(self):
        start_point = Point2D(1, 1)
        end_point = Point2D(31, 39)
        cubicles = Cubicles(start_point, self._input)

        astar = AStar(MazeSearchState(cubicles, start_point, end_point, 0, 0), MazeSearchState(cubicles, end_point, end_point, 0, 0))
        astar.verbose(True, 1000)

        shortest = astar.find_path()

        grid = cubicles.grid({state.position for state in shortest.search_states})
        grid[39][31] = "X"
        show_grid(grid)
        print(f"{shortest}")

        return shortest.cost

    def part_two(self):
        start_point = Point2D(1, 1)
        end_point = Point2D(1, 1)
        cubicles = Cubicles(start_point, self._input)
        end_state = MazeSearchState(cubicles, end_point, end_point, 0, 0)

        unique_points = set()
        start_points = {start_point}
        radius = 50
        for y in range(-radius, radius):
            for x in range(-radius, radius):
                start_points.add(end_point + Point2D(x, y))

        for sp in start_points:
            if sp.x < 0 or sp.y < 0 or cubicles.lookup(sp) != cubicles.SPACE:
                continue

            astar = AStar(MazeSearchState(cubicles, sp, end_point, 0, 0), end_state)
            astar.verbose(True, 1000)

            shortest = astar.find_path()

            if shortest.last == end_state and shortest.cost <= radius:
                unique_points.add(sp)
                print(f"{sp} is reachable")

        grid = cubicles.grid(unique_points)
        grid[1][1] = "X"
        show_grid(grid)

        return len(unique_points)
