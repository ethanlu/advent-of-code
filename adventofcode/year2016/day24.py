from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.graph.search import AStar, BFS, SearchPath, SearchState, S
from itertools import combinations
from typing import Dict, List


class DuctMaze(object):
    def __init__(self, map: List[str]):
        self._map = map
        self._maxX = len(self._map[0])
        self._maxY = len(self._map)

        self._locations = {}
        for y, row in enumerate(self._map):
            for x, c in enumerate(row):
                if c not in ('.', '#'):
                    self._locations[c] = (x, y)

    @property
    def locations(self):
        return self._locations

    def position(self, x: int, y: int) -> str:
        if 0 <= x <= self._maxX and 0 <= y <= self._maxY:
            return self._map[y][x]
        else:
            return '#'


class LocationSearchState(SearchState):
    def __init__(self, maze: DuctMaze, x: int, y: int, gain: int, cost: int):
        super().__init__(f"({x},{y}):{maze.position(x, y)}", gain, cost)
        self._maze = maze
        self._x = x
        self._y = y

    def next_search_states(self) -> List[S]:
        states = []

        if self._maze.position(self._x + 1, self._y) != '#':
            states.append(LocationSearchState(self._maze, self._x + 1, self._y, self.gain, self.cost + 1))
        if self._maze.position(self._x - 1, self._y) != '#':
            states.append(LocationSearchState(self._maze, self._x - 1, self._y, self.gain, self.cost + 1))
        if self._maze.position(self._x, self._y + 1) != '#':
            states.append(LocationSearchState(self._maze, self._x, self._y + 1, self.gain, self.cost + 1))
        if self._maze.position(self._x, self._y - 1) != '#':
            states.append(LocationSearchState(self._maze, self._x, self._y - 1, self.gain, self.cost + 1))

        return states


class EveryLocationSearchState(SearchState):
    def __init__(self, maze: DuctMaze, shortest_lookup: Dict[str, int], remaining: List[str], current_location: str, gain: int, cost: int):
        super().__init__(f"[{gain}]:{current_location}", gain, cost)
        self._maze = maze
        self._shortest_lookup = shortest_lookup
        self._remaining = remaining
        self._current_location = current_location

    @property
    def potential_gain(self) -> int:
        #  assume potential gain is the shortest path from current location to next multiplied by remaining locations
        return -(len(self._remaining) * (min([self._shortest_lookup[f"{self._current_location}-{location}"] for location in self._remaining]) if len(self._remaining) > 0 else 0))

    def next_search_states(self) -> List[S]:
        states = []

        for target_location in self._remaining:
            s = EveryLocationSearchState(
                self._maze, self._shortest_lookup,
                [location for location in self._remaining if location != target_location],
                target_location,
                self.gain - self._shortest_lookup[f"{self._current_location}-{target_location}"], self.cost + 1
            )
            if len(self._remaining) <= 1:
                s.complete()
            states.append(s)
        return states


class EveryLocationAndBackSearchState(EveryLocationSearchState):
    @property
    def potential_gain(self) -> int:
        #  assume potential gain is the shortest path from current location to next multiplied by remaining locations
        return -((len(self._remaining) + 1) * (min([self._shortest_lookup[f"{self._current_location}-{location}"] for location in self._remaining]) if len(self._remaining) > 0 else 0))

    def next_search_states(self) -> List[S]:
        states = []

        if len(self._remaining) == 0:
            states.append(EveryLocationAndBackSearchState(
                self._maze, self._shortest_lookup,
                [],
                '0',
                self.gain - self._shortest_lookup[f"{self._current_location}-0"], self.cost + 1
            ).complete())
        else:
            for target_location in self._remaining:
                states.append(EveryLocationAndBackSearchState(
                    self._maze, self._shortest_lookup,
                    [location for location in self._remaining if location != target_location],
                    target_location,
                    self.gain - self._shortest_lookup[f"{self._current_location}-{target_location}"], self.cost + 1
                ))

        return states


class Day24(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._maze = DuctMaze(self._load_input_as_lines())

        # build lookup of the shortest paths between all locations
        self._shortest_lookup = {}
        for (start, end) in combinations(sorted(self._maze.locations.keys()), 2):
            astar = AStar(
                LocationSearchState(self._maze, self._maze.locations[start][0], self._maze.locations[start][1], 0, 0),
                LocationSearchState(self._maze, self._maze.locations[end][0], self._maze.locations[end][1], 0, 0)
            )
            shortest = astar.find_path().cost

            print(f"shortest from location {start} to location {end} : {shortest}")

            # the shortest path between two locations should be the same in both directions
            self._shortest_lookup[f"{start}-{end}"] = shortest
            self._shortest_lookup[f"{end}-{start}"] = shortest

    def part_one(self):
        start_state = EveryLocationSearchState(self._maze, self._shortest_lookup, [location for location in self._maze.locations.keys() if location != '0'], '0', 0, 0)
        bfs = BFS(SearchPath(start_state))
        bfs.verbose(True, 1000)

        shortest = bfs.find_path()
        print(shortest)

        return -shortest.gain

    def part_two(self):
        start_state = EveryLocationAndBackSearchState(self._maze, self._shortest_lookup, [location for location in self._maze.locations.keys() if location != '0'], '0', 0, 0)
        bfs = BFS(SearchPath(start_state))
        bfs.verbose(True, 1000)

        shortest = bfs.find_path()
        print(shortest)

        return -shortest.gain
