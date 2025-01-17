from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.grid import Point2D
from adventofcode.common.graph.search import AStar, SearchState, S
from adventofcode.common.util import show_dict_grid
from typing import Iterable, List


directions = (
    Point2D(0, -1),
    Point2D(1, 0),
    Point2D(0, 1),
    Point2D(-1, 0)
)


class HonestPathSearchState(SearchState):
    def __init__(self, racetrack: RaceTrack, position: Point2D, gain: int, cost: int):
        super().__init__(f"{position}", gain + 1, cost + 1)
        self._racetrack = racetrack
        self._position = position

    @property
    def position(self) -> Point2D:
        return self._position

    def next_search_states(self) -> List[S]:
        states = []
        for d in directions:
            next_p = self._position + d
            if self._racetrack.is_track(next_p):
                states.append(self.__class__(self._racetrack, next_p, self.gain, self.cost))
        return states


class RaceTrack(object):
    def __init__(self, data: List[str]):
        self._grid = {}
        self._maxy = len(data)
        self._maxx = len(data[0])
        self._start = None
        self._end = None

        for y, row in enumerate(data):
            for x, cell in enumerate(row):
                p = Point2D(x, y)
                match cell:
                    case 'S':
                        self._start = p
                        self._grid[p] = '.'
                    case 'E':
                        self._end = p
                        self._grid[p] = '.'
                    case _:
                        self._grid[p] = cell

    @property
    def start(self) -> Point2D:
        return self._start

    @property
    def end(self) -> Point2D:
        return self._end

    def is_track(self, position: Point2D) -> bool:
        return position in self._grid and self._grid[position] == '.'

    def show(self, cheats: List[Point2D]) -> None:
        grid = {}
        for p, c in self._grid.items():
            grid[(p.x, p.y)] = c
        for p in cheats:
            grid[(p.x, p.y)] = '*'
        grid[(self._start.x, self._start.y)] = 'S'
        grid[(self._end.x, self._end.y)] = 'E'
        show_dict_grid(grid, self._maxx, self._maxy)

    def reachable_tracks(self, position: Point2D, radius: int) -> Iterable[Point2D]:
        for y in range(-radius, radius + 1):
            for x in range(-radius - y, radius - y + 1):
                p = position + Point2D(x, y)
                if abs(x) + abs(y) <= radius and p != position and self.is_track(p):
                    yield p


class Day20(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._rt = RaceTrack(self._load_input_as_lines())
        self._par_path = {}
        astar = AStar(
            HonestPathSearchState(self._rt, self._rt.start, 0, 0),
            HonestPathSearchState(self._rt, self._rt.end, 0, 0)
        )
        astar.verbose(True, 10000)
        for s in astar.find_path().search_states:
            self._par_path[s.position] = s

    def part_one(self):
        radius = 2
        cheats = {}
        for p, s in self._par_path.items():
            # for each position p, see if the cheat can be applied to save some time
            for candidate_p in self._rt.reachable_tracks(p, radius):
                time_saved = self._par_path[candidate_p].cost - s.cost - (abs(p.x - candidate_p.x) + abs(p.y - candidate_p.y))
                if time_saved > 0:
                    # cheat can occur here
                    if time_saved not in cheats:
                        cheats[time_saved] = 0
                    cheats[time_saved] += 1
        for time_saved, amount in sorted(cheats.items()):
            print(f"there are {amount} cheats that save {time_saved} picoseconds.")
        return sum((amount for time_saved, amount in cheats.items() if time_saved >= 100))

    def part_two(self):
        radius = 20
        cheats = {}
        for p, s in self._par_path.items():
            # for each position p, see if the cheat can be applied to save some time
            for candidate_p in self._rt.reachable_tracks(p, radius):
                time_saved = self._par_path[candidate_p].cost - s.cost - (abs(p.x - candidate_p.x) + abs(p.y - candidate_p.y))
                if time_saved > 0:
                    # cheat can occur here
                    if time_saved not in cheats:
                        cheats[time_saved] = 0
                    cheats[time_saved] += 1
        # for time_saved, amount in sorted(cheats.items()):
        #     print(f"there are {amount} cheats that save {time_saved} picoseconds.")
        return sum((amount for time_saved, amount in cheats.items() if time_saved >= 100))
