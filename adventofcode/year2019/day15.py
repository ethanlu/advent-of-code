from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.graph.search import AStar, P, S, SearchState
from adventofcode.common.grid import Point2D
from adventofcode.year2019.day09 import IntCodeCPUComplete
from collections import deque
from functools import reduce
from typing import Dict, List

import sys


directions = [(1, Point2D(0, -1)), (2, Point2D(0, 1)), (3, Point2D(-1, 0)), (4, Point2D(1, 0))]


class OxygenSearchState(SearchState):
    def __init__(self, map: Dict[Point2D, str], position: Point2D, gain: int, cost: int, max_cost: int):
        super().__init__(f"{position}", gain, cost, max_cost)
        self._map = map
        self._position = position

    def next_search_states(self) -> List[S]:
        states = []

        for _, delta in directions:
            p = self._position + delta
            if p in self._map and self._map[p] in ('.', 'X', 'S'):
                states.append(OxygenSearchState(self._map, p, self.gain + 1, self.cost + 1, self.max_cost))

        return states


class RepairBot(object):
    def __init__(self, program: List[int], verbose: bool = False):
        self._cpu = IntCodeCPUComplete(program, verbose)
        self._position = Point2D(0, 0)
        self._oxygen = Point2D(0, 0)
        self._map: Dict[Point2D, str] = {self._position: '.'}

    @property
    def oxygen(self) -> Point2D:
        return self._oxygen

    @property
    def map(self):
        return self._map

    def crawl(self) -> None:
        path = deque([(0, self._position)])
        while len(path) > 0:
            direction_code, self._position = path.pop()

            candidates = [(direction[0], self._position + direction[1]) for direction in directions if (self._position + direction[1]) not in self._map.keys()]
            if len(candidates) > 0:
                # current position has at least 1 direction that has not been explored yet
                path.append((direction_code, self._position))

                # attempt move to first unexplored position in list of candidates
                self._cpu.add_input(candidates[0][0])
                self._cpu.run()
                match self._cpu.get_output():
                    case 0:
                        # hit a wall...mark map and backtrack to last position that has unexplored areas
                        self._map[candidates[0][1]] = '#'
                    case 1 | 2:
                        # successfully moved towards the direction...add new position to path
                        path.append((candidates[0][0], candidates[0][1]))
                        if self._cpu.get_output() == 2:
                            # found oxygen system
                            self._map[candidates[0][1]] = 'X'
                            self._oxygen = candidates[0][1]
                        else:
                            self._map[candidates[0][1]] = '.'
                    case _:
                        raise Exception(f"Invalid response from repair bot : {self._cpu.get_output()}")
            else:
                # current position has no unexplored directions...backtrack to previous position
                match direction_code:
                    case 0:
                        continue
                    case 1:
                        self._cpu.add_input(2)
                    case 2:
                        self._cpu.add_input(1)
                    case 3:
                        self._cpu.add_input(4)
                    case 4:
                        self._cpu.add_input(3)
                self._cpu.run()
                if self._cpu.get_output() != 1:
                    raise Exception(f"Unexpected response from repair bot while backtracking from {self._position} with direction code {direction_code}")

    def show(self) -> None:
        minx = reduce(lambda acc, p: acc if acc < p.x else p.x, self._map.keys(), sys.maxsize)
        maxx = reduce(lambda acc, p: acc if acc > p.x else p.x, self._map.keys(), -sys.maxsize)
        miny = reduce(lambda acc, p: acc if acc < p.y else p.y, self._map.keys(), sys.maxsize)
        maxy = reduce(lambda acc, p: acc if acc > p.y else p.y, self._map.keys(), -sys.maxsize)
        for y in range(miny, maxy + 1):
            row = []
            for x in range(minx, maxx + 1):
                p = Point2D(x, y)
                if x == 0 and y == 0:
                    row.append('S')
                elif p in self._map.keys():
                    row.append(self._map[p])
                else:
                    row.append('?')
            print("".join(row))


class Day15(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._robot = RepairBot([int(i) for i in self._load_input_as_string().split(',')])

    def part_one(self):
        self._robot.crawl()
        self._robot.show()

        astar = AStar(OxygenSearchState(self._robot.map, Point2D(0, 0), 0, 0, sys.maxsize), OxygenSearchState(self._robot.map, self._robot.oxygen, 0, 0, sys.maxsize))
        path = astar.find_path()
        print(path)
        return path.depth - 1

    def part_two(self):
        remaining = set([p for p, v in self._robot.map.items() if v in ('.', 'S')])
        wave_front = [self._robot.oxygen]
        minutes = 0
        while len(remaining) > 0:
            next_wave_front = []
            for position in wave_front:
                for _, delta in directions:
                    next_position = position + delta
                    if next_position in remaining:
                        remaining.remove(next_position)
                        next_wave_front.append(next_position)

            wave_front = next_wave_front
            minutes += 1

        return minutes
    