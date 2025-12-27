from __future__ import annotations
from abc import abstractmethod
from adventofcode.common import Solution
from adventofcode.common.grid import Point2D
from adventofcode.common.graph.search import AStar, SearchState, S
from adventofcode.common.util import show_dict_grid
from typing import Iterable, List, Protocol


deltas = (Point2D(0, -1), Point2D(1, 0), Point2D(0, 1), Point2D(-1, 0))


class ChitonCave(Protocol):
    @property
    @abstractmethod
    def maxx(self) -> int:
        pass

    @property
    @abstractmethod
    def maxy(self) -> int:
        pass

    def risk(self, position: Point2D) -> int:
        pass

    def neighbors(self, position: Point2D) -> Iterable[Point2D]:
        pass


class SmallChitonCave(object):
    def __init__(self, data: List[str]):
        self._maxy = len(data)
        self._maxx = len(data[0])
        self._chitons = {}
        for y, row in enumerate(data):
            for x, cell in enumerate(row):
                p = Point2D(x, y)
                self._chitons[p] = int(cell)

    @property
    def maxx(self) -> int:
        return self._maxx

    @property
    def maxy(self) -> int:
        return self._maxy

    def show(self, path: List[Point2D] = []):
        grid = {(p.x, p.y): str(v) for p, v in self._chitons.items()}
        for p in path:
            grid[(p.x, p.y)] = f"\033[32m{grid[(p.x, p.y)]}\033[0m"
        show_dict_grid(grid, self._maxx, self._maxy)

    def risk(self, position: Point2D) -> int:
        if position not in self._chitons:
            raise Exception(f"unexpected position : {position}")
        return self._chitons[position]

    def neighbors(self, position: Point2D) -> Iterable[Point2D]:
        return [position + delta for delta in deltas if (position + delta) in self._chitons]


class BigChitonCave(object):
    def __init__(self, cave: SmallChitonCave):
        self._cave = cave
        self._maxx = self._cave.maxx * 5
        self._maxy = self._cave.maxy * 5

    @property
    def maxx(self) -> int:
        return self._maxx

    @property
    def maxy(self) -> int:
        return self._maxy

    def risk(self, position: Point2D) -> int:
        if 0 <= position.x < self._maxx and 0 <= position.y < self._maxy:
            # get risk based on starting cave size via modulo
            final_risk = self._cave.risk(Point2D(position.x % self._cave.maxx, position.y % self._cave.maxy))
            # increase risk if actual x position is multiple of original x position and wrap if needed
            final_risk += position.x // self._cave.maxx
            if final_risk > 9:
                final_risk = final_risk % 9
            # do same risk increment for y position
            final_risk += position.y // self._cave.maxy
            if final_risk > 9:
                final_risk = final_risk % 9
            return final_risk
        else:
            raise Exception(f"unexpected position : {position}")

    def neighbors(self, position: Point2D) -> Iterable[Point2D]:
        for delta in deltas:
            new_position = position + delta
            if 0 <= new_position.x < self._maxx and 0 <= new_position.y < self._maxy:
                yield new_position


class LowestRiskSearchState(SearchState):
    def __init__(self, cave: ChitonCave, position: Point2D, cost: int):
        super().__init__(f"{position}", 0, cost)
        self._cave = cave
        self._position = position

    @property
    def position(self) -> Point2D:
        return self._position

    def next_search_states(self) -> List[S]:
        states = []
        for next_position in self._cave.neighbors(self._position):
            states.append(LowestRiskSearchState(self._cave, next_position, self._cost + self._cave.risk(next_position)))
        return states


class Day15(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._scc = SmallChitonCave(self._load_input_as_lines())

    def part_one(self):
        astar = AStar(
            LowestRiskSearchState(self._scc, Point2D(0, 0), 0),
            LowestRiskSearchState(self._scc, Point2D(self._scc.maxx - 1, self._scc.maxy - 1), 0)
        )
        astar.verbose(True, 10000)
        best = astar.find_path()
        self._scc.show([ss.position for ss in best.search_states])
        return best.cost

    def part_two(self):
        bcc = BigChitonCave(self._scc)
        astar = AStar(
            LowestRiskSearchState(bcc, Point2D(0, 0), 0),
            LowestRiskSearchState(bcc, Point2D(bcc.maxx - 1, bcc.maxy - 1), 0)
        )
        astar.verbose(True, 10000)
        best = astar.find_path()
        return best.cost
