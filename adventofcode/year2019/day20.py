from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.graph.search import S, SearchState, AStar
from adventofcode.common.grid import Point2D
from typing import Dict, List


deltas = (Point2D(0, -1), Point2D(1, 0), Point2D(0, 1), Point2D(-1, 0))
hd = ((Point2D(-1, 0), Point2D(1, 0)), (Point2D(1, 0), Point2D(2, 0)))
vd = ((Point2D(0, -1), Point2D(0, 1)), (Point2D(0, 1), Point2D(0, 2)))


class DonutMaze(object):
    def __init__(self, input: List[str]):
        self._maze: Dict[Point2D, str] = {}
        self._portals: Dict[Point2D, Point2D] = {}
        self._start: Point2D = Point2D(0, 0)
        self._end: Point2D = Point2D(0, 0)
        self._maxy = len(input) - 1
        self._maxx = len(input[0]) - 1

        portal_letters = set([])
        y = 0
        for line in input:
            x = 0
            for c in line:
                p = Point2D(x, y)
                self._maze[p] = c
                if c not in (' ', '.', '#'):
                    portal_letters.add(p)
                x += 1
            y += 1

        portal_pairs = {}
        for p in portal_letters:
            # pair portals by looking through all letter positions. one neighbor should be '.' and the other should be another letter
            portal_label = ""
            portal_opening = None
            if (p + hd[0][0]) in self._maze.keys() and self._maze[p + hd[0][0]] == '.' and (p + hd[0][1]) in portal_letters:
                # horizontal variation .pP
                portal_label = f"{self._maze[p]}{self._maze[p + hd[0][1]]}"
                portal_opening = p + hd[0][0]
            elif (p + hd[1][1]) in self._maze.keys() and self._maze[p + hd[1][1]] == '.' and (p + hd[1][0]) in portal_letters:
                # horizontal variation pP.
                portal_label = f"{self._maze[p]}{self._maze[p + hd[1][0]]}"
                portal_opening = p + hd[1][1]
            elif (p + vd[0][0]) in self._maze.keys() and self._maze[p + vd[0][0]] == '.' and (p + vd[0][1]) in portal_letters:
                # vertical variation .pP
                portal_label = f"{self._maze[p]}{self._maze[p + vd[0][1]]}"
                portal_opening = p + vd[0][0]
            elif (p + vd[1][1]) in self._maze.keys() and self._maze[p + vd[1][1]] == '.' and (p + vd[1][0]) in portal_letters:
                # vertical variation pP.
                portal_label = f"{self._maze[p]}{self._maze[p + vd[1][0]]}"
                portal_opening = p + vd[1][1]
            else:
                # neighbor is portal letter but no open passage
                continue

            match portal_label:
                case "AA":
                    self._start = portal_opening
                case "ZZ":
                    self._end = portal_opening
                case _:
                    if portal_label not in portal_pairs.keys():
                        portal_pairs[portal_label] = []
                    portal_pairs[portal_label].append(portal_opening)

        for (a, b) in portal_pairs.values():
            if a == b:
                raise Exception(f"Invalid portal pair {a} and {b}")
            self._portals[a] = b
            self._portals[b] = a

    @property
    def start(self) -> Point2D:
        return self._start

    @property
    def end(self) -> Point2D:
        return self._end

    def is_path(self, p: Point2D) -> bool:
        return p in self._maze.keys() and self._maze[p] == '.'

    def is_portal(self, p: Point2D) -> bool:
        return p in self._portals.keys()

    def is_outer_portal(self, p: Point2D) -> bool:
        return p.x == 2 or p.x == (self._maxx - 3) or p.y == 2 or p.y == (self._maxy - 2)

    def portal_end(self, p: Point2D) -> Point2D:
        return self._portals[p]


class PortalShortestSearchState(SearchState):
    def __init__(self, maze: DonutMaze, position: Point2D, gain: int, cost: int):
        super().__init__(f"{position}", gain, cost)
        self._maze = maze
        self._position = position

    def next_search_states(self) -> List[S]:
        states = []
        for delta in deltas:
            next_p = self._position + delta
            if self._maze.is_path(next_p):
                states.append(PortalShortestSearchState(self._maze, next_p, self.gain, self.cost + 1))
        if self._maze.is_portal(self._position):
            states.append(PortalShortestSearchState(self._maze, self._maze.portal_end(self._position), self.gain, self.cost + 1))
        return states


class RecursivePortalShortestSearchState(SearchState):
    def __init__(self, maze: DonutMaze, position: Point2D, level: int, gain: int, cost: int):
        super().__init__(f"{position}:{level}", gain, cost)
        self._maze = maze
        self._position = position
        self._level = level

    def next_search_states(self) -> List[S]:
        states = []
        for delta in deltas:
            next_p = self._position + delta
            if self._maze.is_path(next_p):
                states.append(RecursivePortalShortestSearchState(self._maze, next_p, self._level, self.gain, self.cost + 1))
        if self._maze.is_portal(self._position):
            if self._maze.is_outer_portal(self._position):
                # can only go to outer portal if not at the outermost level and the portal is not the start or end portal
                if self._level > 0:
                    states.append(RecursivePortalShortestSearchState(
                        self._maze, self._maze.portal_end(self._position), self._level - 1, self.gain, self.cost + 1
                    ))
            else:
                states.append(RecursivePortalShortestSearchState(self._maze, self._maze.portal_end(self._position), self._level + 1, self.gain, self.cost + 1))
        return states


class Day20(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._input = self._load_input_as_lines(False)

    def part_one(self):
        dm = DonutMaze(self._input)
        astar = AStar(
            PortalShortestSearchState(dm, dm.start, 0, 0),
            PortalShortestSearchState(dm, dm.end, 0, 0)
        )
        astar.verbose(True, 1000)
        path = astar.find_path()
        print(path)
        return path.depth - 1

    def part_two(self):
        dm = DonutMaze(self._input)
        astar = AStar(
            RecursivePortalShortestSearchState(dm, dm.start, 0, 0, 0),
            RecursivePortalShortestSearchState(dm, dm.end, 0, 0, 0)
        )
        astar.verbose(True, 100000)
        path = astar.find_path()
        print(path)
        return path.depth - 1