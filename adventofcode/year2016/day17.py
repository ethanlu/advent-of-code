from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.graph.search import AStar, BFS, SearchPath, SearchState, S
from adventofcode.common.grid import Point2D
from typing import List

import hashlib


directions = {'U': 0, 'D': 1, 'L': 2, 'R': 3}
open_doors = ('b', 'c', 'd', 'e', 'f')
maxX = 4
maxY = 4
maxCost = 99999


class ShortestSearchState(SearchState):
    def __init__(self, position: Point2D, sequence: str, gain: int, cost: int, max_cost: int):
        self._position = position
        self._sequence = sequence
        self._door_hash = hashlib.md5(self._sequence.encode('utf-8')).hexdigest()[:len(directions)]
        super().__init__(f"{self._position}" if self._position.x == maxX and self._position.y == maxY else f"{self._position}:{''.join(self._door_hash)}", gain, cost, max_cost)

    @property
    def sequence(self):
        return ''.join((c for c in self._sequence if c in directions.keys()))

    @property
    def potential_gain(self) -> int:
        return self._position.x + self._position.y

    def next_search_states(self, previous_search_state: S) -> List[S]:
        states = []
        for d, i in directions.items():
            if self._door_hash[i] not in open_doors:
                continue
            if d == 'U' and self._position.y > 1:
                states.append(ShortestSearchState(self._position + Point2D(0, -1), self._sequence + d, self.gain + 1, self.cost + 1, self.max_cost))
            if d == 'D' and self._position.y < maxY:
                states.append(ShortestSearchState(self._position + Point2D(0, 1), self._sequence + d, self.gain + 1, self.cost + 1, self.max_cost))
            if d == 'L' and self._position.x > 1:
                states.append(ShortestSearchState(self._position + Point2D(-1, 0), self._sequence + d, self.gain + 1, self.cost + 1, self.max_cost))
            if d == 'R' and self._position.x < maxX:
                states.append(ShortestSearchState(self._position + Point2D(1, 0), self._sequence + d, self.gain + 1, self.cost + 1, self.max_cost))

        return states


class LongestSearchState(ShortestSearchState):
    def next_search_states(self, previous_search_state: S) -> List[S]:
        states = []
        for d, i in directions.items():
            if self._door_hash[i] not in open_doors:
                continue
            if d == 'U' and self._position.y > 1:
                states.append(LongestSearchState(self._position + Point2D(0, -1), self._sequence + d, self.gain + 1, self.cost + 1, self.max_cost))
            if d == 'D' and self._position.y < maxY:
                if self._position.x == maxX and self._position.y == maxY - 1:
                    states.append(LongestSearchState(self._position + Point2D(0, 1), self._sequence + d, self.gain + 1, self.max_cost, self.max_cost))
                else:
                    states.append(LongestSearchState(self._position + Point2D(0, 1), self._sequence + d, self.gain + 1, self.cost + 1, self.max_cost))
            if d == 'L' and self._position.x > 1:
                states.append(LongestSearchState(self._position + Point2D(-1, 0), self._sequence + d, self.gain + 1, self.cost + 1, self.max_cost))
            if d == 'R' and self._position.x < maxX:
                if self._position.x == maxX - 1 and self._position.y == maxY:
                    states.append(LongestSearchState(self._position + Point2D(1, 0), self._sequence + d, self.gain + 1, self.max_cost, self.max_cost))
                else:
                    states.append(LongestSearchState(self._position + Point2D(1, 0), self._sequence + d, self.gain + 1, self.cost + 1, self.max_cost))

        return states


class Day17(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._input = self._load_input_as_string()

    def part_one(self):
        start = Point2D(1, 1)
        end = Point2D(4, 4)
        start_state = ShortestSearchState(start, self._input, 0, 0, maxCost)
        end_state = ShortestSearchState(end, '', 0, 0, maxCost)
        end_state.fingerprint = f"{end}"
        astar = AStar(SearchPath(start_state), end_state)

        astar.verbose(True, 1000)
        shortest = astar.find_path()

        print(f"{shortest}")

        return shortest.last.sequence

    def part_two(self):
        start = Point2D(1, 1)
        start_state = LongestSearchState(start, self._input, 0, 0, maxCost)
        bfs = BFS(SearchPath(start_state))

        bfs.verbose(True, 5000)
        longest = bfs.find_path()

        print(f"{longest}")
        print(f"{longest.last.sequence}")

        return longest.gain
