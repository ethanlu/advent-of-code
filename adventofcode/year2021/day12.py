from __future__ import annotations
from adventofcode.common import Solution
from collections import deque


class Cave(object):
    def __init__(self, name: str):
        self._name = name
        self._is_big = all([65 <= ord(c) <= 90 for c in name])

    def __hash__(self):
        return hash(self._name)

    def __eq__(self, other):
        return isinstance(other, Cave) and self._name == other.name

    def __str__(self):
        return self._name

    def __repr__(self):
        return self._name

    @property
    def name(self) -> str:
        return self._name

    @property
    def is_big(self) -> bool:
        return self._is_big


class Day12(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._connections = {}
        for line in self._load_input_as_lines():
            t = line.split('-')
            a = Cave(t[0])
            b = Cave(t[1])
            if a not in self._connections:
                self._connections[a] = set()
            if b not in self._connections:
                self._connections[b] = set()
            self._connections[a].add(b)
            self._connections[b].add(a)

    def part_one(self):
        paths = []
        remaining = deque([(Cave('start'), [Cave('start')], {Cave('start')})])
        while len(remaining) > 0:
            current, path, visited = remaining.popleft()
            for connection in self._connections[current]:
                match connection.is_big, connection in visited:
                    case True, _:
                        remaining.append((connection, path + [connection], visited.union({connection})))
                    case False, False:
                        # connection is small cave and have not been visited yet
                        if connection.name == 'end':
                            paths.append('-'.join((str(c) for c in path)) + f"-{str(connection)}")
                        else:
                            remaining.append((connection, path + [connection], visited.union({connection})))
        return len(paths)

    def part_two(self):
        paths = []
        remaining = deque([(Cave('start'), [Cave('start')], {Cave('start')}, True)])
        while len(remaining) > 0:
            current, path, visited, can_revisit = remaining.popleft()
            for connection in self._connections[current]:
                match connection.is_big, connection in visited, can_revisit:
                    case True, _, _:
                        remaining.append((connection, path + [connection], visited.union({connection}), can_revisit))
                    case False, False, _:
                        # connection is small cave and have not been visited yet
                        if connection.name == 'end':
                            paths.append('-'.join((str(c) for c in path)) + f"-{str(connection)}")
                        else:
                            remaining.append((connection, path + [connection], visited.union({connection}), can_revisit))
                    case False, True, True:
                        # connection is small cave and has been visited, but can be revisited... on only revisit if it has more than one connection
                        if connection.name != 'start':
                            remaining.append((connection, path + [connection], visited.union({connection}), False))
        return len(paths)
