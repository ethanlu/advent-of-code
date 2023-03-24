from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.graph.search import AStar, BFS, DFS, S, SearchState, SearchPath
from adventofcode.common.grid import Point2D
from functools import reduce
from itertools import combinations
from typing import Dict, List, Set, Tuple

import sys


deltas = (Point2D(0, -1), Point2D(1, 0), Point2D(0, 1), Point2D(-1, 0))


class KeyChain(object):
    def __init__(self, keys: int = 0):
        self._keys = keys

    def __str__(self):
        return str(self._keys)

    @property
    def keys(self) -> int:
        return self._keys

    def key_count(self) -> int:
        return int.bit_count(self._keys)

    def add_key(self, key: str) -> KeyChain:
        self._keys |= pow(2, ord(key.lower()) - 97)
        return self

    def has_key(self, key: str) -> bool:
        return self._keys & pow(2, ord(key.lower()) - 97) > 0

    def can_unlock(self, lock: str) -> bool:
        return self._keys & pow(2, ord(lock.upper()) - 65) > 0


class ShortestKeySearchState(SearchState):
    def __init__(self, maze: NeptuneMaze, position: Point2D, locks: List[str], gain: int, cost: int):
        super().__init__(f"{position}", gain, cost)
        self._maze = maze
        self._position = position
        self._locks = locks

    @property
    def locks(self) -> List[str]:
        return self._locks

    def next_search_states(self) -> List[S]:
        states = []
        for delta in deltas:
            next_position = self._position + delta
            if not self._maze.is_wall(next_position):
                # only proceed if position is an open passage, unlockable lock, or a key that we already have
                states.append(ShortestKeySearchState(
                    self._maze, next_position,
                    self._locks + ([self._maze.locks[next_position]] if self._maze.is_lock(next_position) else []),
                    self.gain, self.cost + 1
                ))
        return states


class BestKeyPathSearchState(SearchState):
    def __init__(self, maze: NeptuneMaze, lookup: Dict[str, Tuple], position: str, keys: KeyChain, remaining_keys: Set[str], gain: int, cost: int):
        super().__init__(f"{position}:{sorted(remaining_keys)}", gain, cost)
        self._maze = maze
        self._lookup = lookup
        self._position = position
        self._keys = keys
        self._remaining_keys = remaining_keys

    @property
    def potential_gain(self) -> int:
        return len(self._remaining_keys)

    def next_search_states(self) -> List[S]:
        states = []

        for key in self._remaining_keys:
            if sum((1 for lock in self._lookup[f"{self._position}{key}"][1] if not self._keys.can_unlock(lock))) == 0:
                # all locks in this path can be unlocked...proceed
                remaining = set(self._remaining_keys)
                remaining.remove(key)

                s = BestKeyPathSearchState(
                    self._maze, self._lookup, key,
                    KeyChain(self._keys.keys).add_key(key),
                    remaining,
                    self.gain + 1,
                    self.cost + self._lookup[f"{self._position}{key}"][0]
                )
                if len(remaining) == 0:
                    s.complete()
                states.append(s)
        return states


class Best4KeyPathSearchState(SearchState):
    def __init__(self, mazes: List[NeptuneMaze], lookup: List[Dict[str, Tuple]], positions: List[str], keys: KeyChain, remaining_keys: Set[str], gain: int, cost: int):
        super().__init__(f"{sorted(positions)}:{sorted(remaining_keys)}", gain, cost)
        self._mazes = mazes
        self._lookup = lookup
        self._positions = positions
        self._keys = keys
        self._remaining_keys = remaining_keys

    @property
    def potential_gain(self) -> int:
        return len(self._remaining_keys)

    def next_search_states(self) -> List[S]:
        states = []

        for key in self._remaining_keys:
            for i, position in enumerate(self._positions):
                if key in self._mazes[i].keys.values() and \
                        sum((1 for lock in self._lookup[i][f"{position}{key}"][1] if not self._keys.can_unlock(lock))) == 0:
                    # all locks in this part of maze path can be unlocked...proceed
                    remaining = set(self._remaining_keys)
                    remaining.remove(key)

                    next_positions = list(self._positions)
                    next_positions[i] = key
                    s = Best4KeyPathSearchState(
                        self._mazes, self._lookup, next_positions,
                        KeyChain(self._keys.keys).add_key(key),
                        remaining,
                        self.gain + 1,
                        self.cost + self._lookup[i][f"{position}{key}"][0]
                    )
                    if len(remaining) == 0:
                        s.complete()
                    states.append(s)
        return states


class NeptuneMaze(object):
    def __init__(self, input: Dict[Point2D, str]):
        self._maze: Dict[Point2D, str] = input
        self._keys: Dict[Point2D, str] = {}
        self._key_positions: Dict[str, Point2D] = {}
        self._locks: Dict[Point2D, str] = {}
        self._position = None
        self._all_keys = KeyChain(0)

        for p, c in self._maze.items():
            match c:
                case '#' | '.':
                    continue
                case '@':
                    self._position = p
                case _:
                    if 65 <= ord(c) <= 90:
                        self._locks[p] = c
                    if 97 <= ord(c) <= 122:
                        self._keys[p] = c
                        self._key_positions[c] = p
                        self._all_keys.add_key(c)

    @property
    def position(self) -> Point2D:
        return self._position

    @property
    def key_positions(self) -> Dict[str, Point2D]:
        return self._key_positions

    @property
    def keys(self) -> Dict[Point2D, str]:
        return self._keys

    @property
    def locks(self) -> Dict[Point2D, str]:
        return self._locks

    @property
    def all_keys(self) -> KeyChain:
        return self._all_keys

    def is_passage(self, position: Point2D) -> bool:
        return self._maze[position] == '.'

    def is_wall(self, position: Point2D) -> bool:
        return self._maze[position] == '#'

    def is_key(self, position: Point2D) -> bool:
        return position in self._keys.keys()

    def is_lock(self, position: Point2D) -> bool:
        return position in self._locks.keys()

    def show(self) -> None:
        minx = reduce(lambda acc, p: acc if acc < p.x else p.x, self._maze.keys(), sys.maxsize)
        maxx = reduce(lambda acc, p: acc if acc > p.x else p.x, self._maze.keys(), -sys.maxsize)
        miny = reduce(lambda acc, p: acc if acc < p.y else p.y, self._maze.keys(), sys.maxsize)
        maxy = reduce(lambda acc, p: acc if acc > p.y else p.y, self._maze.keys(), -sys.maxsize)
        for y in range(miny, maxy + 1):
            row = []
            for x in range(minx, maxx + 1):
                p = Point2D(x, y)
                if p == self._position:
                    row.append('@')
                else:
                    row.append(self._maze[p])
            print("".join(row))


class Day18(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._input: Dict[Point2D, str] = {}
        for y, line in enumerate(self._load_input_as_lines()):
            for x, c in enumerate(line):
                p = Point2D(x, y)
                self._input[p] = c

    def _find_shortest_path(self, maze: NeptuneMaze) -> Dict[str, Tuple[int, List[str]]]:
        shortest_paths = {}

        # find shortest path from start position to each key and store the steps between them and locks encountered
        for k in maze.keys.values():
            astar = AStar(
                ShortestKeySearchState(maze, maze.position, [], 0, 0),
                ShortestKeySearchState(maze, maze.key_positions[k], [], 0, 0)
            )
            path = astar.find_path()
            shortest_paths[f"@{k}"] = (path.cost, path.last.locks)

        # find shortest path from every pair of keys and store the steps between them and locks encountered
        for a, b in combinations(maze.keys.values(), 2):
            astar = AStar(
                ShortestKeySearchState(maze, maze.key_positions[a], [], 0, 0),
                ShortestKeySearchState(maze, maze.key_positions[b], [], 0, 0)
            )
            path = astar.find_path()
            shortest_paths[f"{a}{b}"] = (path.cost, path.last.locks)
            shortest_paths[f"{b}{a}"] = (path.cost, path.last.locks)

        return shortest_paths


    def part_one(self):
        maze = NeptuneMaze(self._input)
        maze.show()

        shortest_paths = self._find_shortest_path(maze)

        dfs = DFS(SearchPath(BestKeyPathSearchState(maze, shortest_paths, '@', KeyChain(0), set(maze.keys.values()), 0, 0)))
        dfs.verbose(True, 100000)

        path = dfs.find_path()
        print(path)

        return path.cost

    def part_two(self):
        size = len(self._load_input_as_lines())
        maze_center = Point2D(size // 2, size // 2)
        self._input[Point2D(maze_center.x - 1, maze_center.y - 1)] = '@'
        self._input[Point2D(maze_center.x, maze_center.y - 1)] = '#'
        self._input[Point2D(maze_center.x + 1, maze_center.y - 1)] = '@'
        self._input[Point2D(maze_center.x - 1, maze_center.y)] = '#'
        self._input[Point2D(maze_center.x, maze_center.y)] = '#'
        self._input[Point2D(maze_center.x + 1, maze_center.y)] = '#'
        self._input[Point2D(maze_center.x - 1, maze_center.y + 1)] = '@'
        self._input[Point2D(maze_center.x, maze_center.y + 1)] = '#'
        self._input[Point2D(maze_center.x + 1, maze_center.y + 1)] = '@'

        mazes = [
            NeptuneMaze({p:c for p, c in self._input.items() if p.x <= maze_center.x and p.y <= maze_center.y}),  # upper left
            NeptuneMaze({p:c for p, c in self._input.items() if p.x >= maze_center.x and p.y <= maze_center.y}),  # upper right
            NeptuneMaze({p:c for p, c in self._input.items() if p.x <= maze_center.x and p.y >= maze_center.y}),  # lower left
            NeptuneMaze({p:c for p, c in self._input.items() if p.x >= maze_center.x and p.y >= maze_center.y}),  # lower right
        ]
        shortest_paths = [
            self._find_shortest_path(mazes[0]),
            self._find_shortest_path(mazes[1]),
            self._find_shortest_path(mazes[2]),
            self._find_shortest_path(mazes[3])
        ]

        dfs = DFS(SearchPath(Best4KeyPathSearchState(
            mazes, shortest_paths,
            ['@', '@', '@', '@'],
            KeyChain(0),
            reduce(lambda acc, x: acc.union(x), (set(m.keys.values()) for m in mazes)),
            0, 0)))
        dfs.verbose(True, 100000)

        path = dfs.find_path()
        print(path)

        return path.cost