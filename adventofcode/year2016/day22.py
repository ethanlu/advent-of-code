from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.graph.search import AStar, SearchState, S
from adventofcode.common.util import show_grid
from functools import reduce
from itertools import permutations
from typing import Iterable, List, Optional, Tuple

import re


class DataNode(object):
    def __init__(self, x: int, y: int, size: int, used: int, available: int, use_percent: int):
        self._x = x
        self._y = y
        self._size = size
        self._used = used
        self._available = available
        self._use_percent = use_percent

    def __str__(self):
        return f"[{self.x}, {self.y}] {self.used}/{self.size} ({self.use_percent}%)"

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def size(self):
        return self._size

    @property
    def used(self):
        return self._used

    @property
    def available(self):
        return self._available

    @property
    def use_percent(self):
        return self._use_percent


class DataCluster(object):
    def __init__(self, nodes: Iterable[DataNode]):
        self._nodes = {f"{node.x},{node.y}": node for node in nodes}
        self._maxX = reduce(lambda acc, n: acc if acc > n.x else n.x, self._nodes.values(), 0)
        self._maxY = reduce(lambda acc, n: acc if acc > n.y else n.y, self._nodes.values(), 0)

    @property
    def max_x(self):
        return self._maxX

    @property
    def empty_node(self) -> DataNode:
        for node in self._nodes.values():
            if node.use_percent == 0:
                return node

    @property
    def grid(self):
        grid = []
        for y in range(self._maxY + 1):
            row = []
            for x in range(self._maxX + 1):
                node = self._nodes[f"{x},{y}"]
                if node.use_percent == 0:
                    row.append('_')
                elif node.use_percent > 90:
                    row.append('#')
                else:
                    row.append('.')
            grid.append(row)
        grid[0][0] = 'S'
        grid[0][self._maxX] = 'G'

        return grid

    def node_at(self, x: int, y: int) -> Optional[DataNode]:
        return self._nodes[f"{x},{y}"] if 0 <= x <= self._maxX and 0 <= y <= self._maxY else None

    def viable_pairs(self) -> List[Tuple[DataNode, DataNode]]:
        return [(a, b) for (a, b) in permutations(self._nodes.values(), 2) if 0 < a.used <= b.available]


class DataSearchState(SearchState):
    def __init__(self, data_cluster: DataCluster, x: int, y: int, gain: int, cost: int, max_cost: int):
        super().__init__(f"{x},{y}", gain, cost, max_cost)
        self._data_cluster = data_cluster
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def next_search_states(self) -> List[S]:
        states = []

        if self._data_cluster.node_at(self._x, self._y - 1) is not None and self._data_cluster.node_at(self._x, self._y - 1).use_percent < 90:
            states.append(DataSearchState(self._data_cluster, self._x, self._y - 1, self.gain, self.cost + 1, self.max_cost))
        if self._data_cluster.node_at(self._x, self._y + 1) is not None and self._data_cluster.node_at(self._x, self._y + 1).use_percent < 90:
            states.append(DataSearchState(self._data_cluster, self._x, self._y + 1, self.gain, self.cost + 1, self.max_cost))
        if self._data_cluster.node_at(self._x - 1, self._y) is not None and self._data_cluster.node_at(self._x - 1, self._y).use_percent < 90:
            states.append(DataSearchState(self._data_cluster, self._x - 1, self._y, self.gain, self.cost + 1, self.max_cost))
        if self._data_cluster.node_at(self._x + 1, self._y) is not None and self._data_cluster.node_at(self._x + 1, self._y).use_percent < 90:
            states.append(DataSearchState(self._data_cluster, self._x + 1, self._y, self.gain, self.cost + 1, self.max_cost))

        return states


class Day22(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._regex = re.compile(r'/dev/grid/node-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T\s+(\d+)T\s+(\d+)%')
        self._nodes = [DataNode(int(m.groups()[0]), int(m.groups()[1]), int(m.groups()[2]), int(m.groups()[3]), int(m.groups()[4]), int(m.groups()[5]))
                       for m in (self._regex.match(line) for line in self._load_input_as_lines()) if m is not None]

    def part_one(self):
        dc = DataCluster(self._nodes)
        viable_pairs = dc.viable_pairs()

        for (a, b) in viable_pairs:
            print(f"{a} fits in {b}")

        return len(viable_pairs)

    def part_two(self):
        dc = DataCluster(self._nodes)
        empty_node = dc.empty_node
        start = DataSearchState(dc, empty_node.x, empty_node.y, 0, 0, 99999)
        end = DataSearchState(dc, dc.max_x - 1, 0, 0, 0, 99999)
        astar = AStar(start, end)
        astar.verbose(True, 1000)

        # shortest path to move the empty data node to the left of the G node
        shortest = astar.find_path()

        grid = dc.grid
        for state in shortest.search_states:
            grid[state.y][state.x] = 'x'
        grid[empty_node.y][empty_node.x] = '_'
        show_grid(grid)

        # once the empty node is to the left of the G node, can just cycle the empty node in a clockwise motion to move the G node left one step
        # ._G -> .G_ -> _G. -> G_. = 5 steps to move G one step left
        # ...    ...    ...    ...
        return shortest.cost + end.x * 5 + 1