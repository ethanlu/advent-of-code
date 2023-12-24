from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.graph.search import BFS, SearchState, SearchPath, S
from adventofcode.common.grid import Point2D
from adventofcode.common.util import show_dict_grid
from collections import deque
from itertools import pairwise
from typing import Dict, List, Set, Tuple


directions = {'N': Point2D(0, -1), 'S': Point2D(0, 1), 'W': Point2D(-1 ,0), 'E': Point2D(1, 0)}


class HikeTrail(object):
    def __init__(self, grid: Dict[Point2D, str], maxp: Point2D, walkable: int, start: Point2D, end: Point2D, ignore_ice: bool):
        self._grid = grid
        self._maxp = maxp
        self._walkable = walkable
        self._start = start
        self._end = end
        self._ignore_ice = ignore_ice

        # majority of the grid are single cell wide, so there is only one direction to go. only time a direction can `change is when a fork is reached.
        self._forks: Set[Point2D] = set()
        for p, c in self._grid.items():
            if c == '.':
                neighbors = 0
                for delta in directions.values():
                    np = p + delta
                    if np in self._grid and self._grid[np] != '#':
                        neighbors += 1
                if neighbors > 2:
                    self._forks.add(p)

        # with these forks, the grid can be reduced into a directed graph of start, end, and all points that have more than 2 paths leading to it
        # for star, end, and every fork points, see which other points they can reach immediately
        dg_points = set([self._start] + list(self._forks) + [self._end])
        self._neighbors: Dict[Point2D, Dict[Point2D, Tuple[int, List[Point2D]]]] = {}
        for position in dg_points:
            self._neighbors[position] = {}
            visited = {position}
            remaining = deque([(position, [])])
            while len(remaining) > 0:
                p, path = remaining.pop()

                # position is one of the points in the dag, so record amount of steps it took to reach it and end this path
                if path and p in dg_points:
                    self._neighbors[position][p] = (len(path), path)
                    continue

                for direction, delta in directions.items():
                    np = p + delta
                    steps = []
                    if np not in self._grid or np in visited:
                        continue
                    if self._ignore_ice:    # when ignoring slippery slopes, trail can be walked so as long as it is not #
                        if self._grid[p] == '#':
                            continue
                    else:   # trail has slippery slopes means can only go in direction if ice direction matches walk direction
                        match direction, self._grid[np]:
                            case ('N', '^') | ('S', 'v') | ('W', '<') | ('E', '>') | (_, '.'):  # valid steps
                                while self._grid[np] != '.':
                                    visited.add(np)
                                    steps.append(np)
                                    np = np + delta
                            case _: # all others are invalid
                                continue
                    visited.add(p)
                    steps.append(np)
                    remaining.append((np, path + steps))

    @property
    def walkable(self) -> int:
        return self._walkable

    def neighbors(self, p: Point2D) -> Dict[Point2D, Tuple[int, List[Point2D]]]:
        return self._neighbors[p]

    def show(self, path: List[Point2D]) -> None:
        grid = {(p.x, p.y): c for p, c in self._grid.items()}
        for start, end in pairwise(path):
            for p in self._neighbors[start][end][1]:
                grid[(p.x, p.y)] = 'O'
        grid[(self._start.x, self._start.y)] = 'S'
        grid[(self._end.x, self._end.y)] = 'E'
        show_dict_grid(grid, self._maxp.x + 1, self._maxp.y + 1)


class LongestHikeSearchState(SearchState):
    def __init__(self, trail: HikeTrail, visited: Set[Point2D], position: Point2D, target: Point2D, sacrificed: int, gain: int, cost: int):
        super().__init__(f"{position}", gain, cost)
        self._trail = trail
        self._visited = visited
        self._position = position
        self._target = target
        self._sacrificed = sacrificed

    @property
    def position(self) -> Point2D:
        return self._position

    @property
    def potential_gain(self) -> int:
        return self._trail.walkable - self._sacrificed

    def next_search_states(self) -> List[S]:
        states = []
        sacrificed = sum((steps for neighbor, (steps, path) in self._trail.neighbors(self._position).items()))
        for neighbor, (steps, path) in self._trail.neighbors(self._position).items():
            if neighbor not in self._visited:
                state = LongestHikeSearchState(
                    self._trail, self._visited | {neighbor}, neighbor, self._target,
                    self._sacrificed + sacrificed - steps, self.gain + steps, self.cost + steps
                )
                if neighbor == self._target:
                    state.complete()
                states.append(state)
        return states


class Day23(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._grid: Dict[Point2D, str] = {}
        self._start = None
        self._end = None
        self._maxp = Point2D(0, 0)
        self._walkable = 0
        for y, row in enumerate(self._load_input_as_lines()):
            for x, cell in enumerate(row):
                p = Point2D(x, y)
                self._grid[p] = cell
                self._start = p if self._start is None and cell == '.' else self._start
                self._end = p if cell == '.' else self._end
                self._maxp = Point2D(max(self._maxp.x, x), max(self._maxp.y, y))
                self._walkable += 1 if cell != '#' else 0

    def part_one(self):
        ht = HikeTrail(self._grid, self._maxp, self._walkable, self._start, self._end, False)
        bfs = BFS(SearchPath(LongestHikeSearchState(ht, {self._start}, self._start, self._end, 0, 0, 0)))
        bfs.verbose(True, 1000)
        best = bfs.find_path()

        ht.show([s.position for s in best.search_states])
        print(f"best path: {best}")

        return best.gain

    def part_two(self):
        def LongestHikeDFS(p: Point2D, visited: Set[Point2D]) -> Tuple[int, List[Point2D]]:
            if p == self._end:
                return 0, []
            longest = 0
            longest_path = []
            for neighbor, (steps, _) in ht.neighbors(p).items():
                if neighbor not in visited:
                    l, path = LongestHikeDFS(neighbor, visited | {neighbor})
                    l += steps
                    if l > longest:
                        longest = l
                        longest_path = [neighbor] + path
            return longest, longest_path
        ht = HikeTrail(self._grid, self._maxp, self._walkable, self._start, self._end, True)
        ls, lp = LongestHikeDFS(self._start, {self._start})
        lp = [self._start] + lp

        ht.show(lp)
        print(f"best path: {[str(p) for p in lp]}")
        return ls
