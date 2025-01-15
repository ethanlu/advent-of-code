from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.grid import Point2D
from adventofcode.common.graph.search import AStar, SearchState, S, P
from adventofcode.common.util import show_dict_grid
from typing import List


directions = (
    Point2D(0, -1),
    Point2D(1, 0),
    Point2D(0, 1),
    Point2D(-1, 0)
)


class ShortestPathSearchState(SearchState):
    def __init__(self, memory_grid: MemoryGrid, position: Point2D, cost: int):
        super().__init__(f"{position}", 0, cost)
        self._memory_grid = memory_grid
        self._position = position

    @property
    def position(self) -> Point2D:
        return self._position

    def next_search_states(self) -> List[S]:
        states = []
        for d in directions:
            next_p = self._position + d
            if self._memory_grid.is_safe(next_p) and not self._memory_grid.is_corrupted(next_p):
                states.append(ShortestPathSearchState(self._memory_grid, next_p, self._cost + 1))
        return states


class MemoryGrid(object):
    def __init__(self, size: int, falling_bytes: List[Point2D]):
        self._maxx = size + 1
        self._maxy = size + 1
        self._start = Point2D(0, 0)
        self._end = Point2D(size, size)
        self._falling_bytes = set(falling_bytes)

    @property
    def start(self) -> Point2D:
        return self._start

    @property
    def end(self) -> Point2D:
        return self._end

    def is_safe(self, position: Point2D) -> bool:
        return self._start.x <= position.x <= self._end.x and self._start.y <= position.y <= self._end.y

    def is_corrupted(self, position: Point2D) -> bool:
        return position in self._falling_bytes

    def show(self, path: P = None) -> None:
        grid = {}

        for y in range(self._maxy):
            for x in range(self._maxx):
                grid[(x, y)] = '.'
        for falling_byte in self._falling_bytes:
            grid[(falling_byte.x, falling_byte.y)] = '#'
        if path:
            for s in path.search_states:
                grid[(s.position.x, s.position.y)] = 'O'
        grid[(self._start.x, self._start.y)] = 'S'
        grid[(self._end.x, self._end.y)] = 'E'
        show_dict_grid(grid, self._maxx, self._maxy)


class Day18(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._input = []
        for line in self._load_input_as_lines():
            x, y = line.split(',')
            self._input.append(Point2D(int(x), int(y)))

    def part_one(self):
        memory_space = 70
        falling_memory_limit = 1024
        mg = MemoryGrid(memory_space, self._input[:falling_memory_limit])
        ss = ShortestPathSearchState(mg, mg.start, 0)
        es = ShortestPathSearchState(mg, mg.end, 0)
        astar = AStar(ss, es)
        astar.verbose(True, 10000)
        p = astar.find_path()
        mg.show(p)
        return len(p.search_states) - 1

    def part_two(self):
        memory_space = 70
        starting_memory_limit = 1024
        for falling_memory_limit in range(starting_memory_limit, len(self._input)):
            mg = MemoryGrid(memory_space, self._input[:falling_memory_limit])
            ss = ShortestPathSearchState(mg, mg.start, 0)
            es = ShortestPathSearchState(mg, mg.end, 0)
            astar = AStar(ss, es)
            p = astar.find_path()

            if p.search_states[-1].position == mg.end:
                print(f"byte #{str(falling_memory_limit)} ({self._input[falling_memory_limit - 1]}) has a path")
            else:
                print(f"byte #{str(falling_memory_limit)} ({self._input[falling_memory_limit - 1]}) has no path")
                mg.show()
                return f"{self._input[falling_memory_limit - 1].x},{self._input[falling_memory_limit - 1].y}"
