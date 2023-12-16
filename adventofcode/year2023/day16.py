from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.grid import Point2D
from adventofcode.common.util import show_dict_grid
from collections import deque
from typing import List, Set, Tuple


directions = {'N': Point2D(0, -1), 'S': Point2D(0, 1), 'W': Point2D(-1, 0), 'E': Point2D(1, 0)}
light_ingress_egress = {
    '.': {'N': ('N', ), 'S': ('S', ), 'W': ('W', ), 'E': ('E', )},
    '/': {'N': ('E', ), 'S': ('W', ), 'W': ('S', ), 'E': ('N', )},
    '\\': {'N': ('W', ), 'S': ('E', ), 'W': ('N', ), 'E': ('S', )},
    '-': {'N': ('W', 'E'), 'S': ('W', 'E'), 'W': ('W', ), 'E': ('E', )},
    '|': {'N': ('N', ), 'S': ('S', ), 'W': ('N', 'S'), 'E': ('N', 'S')},
}


class LightContraption(object):
    def __init__(self, data: List[List[str]]):
        self._maxy = len(data)
        self._maxx = len(data[0])
        self._grid = {}
        for y, row in enumerate(data):
            for x, cell in enumerate(row):
                self._grid[Point2D(x, y)] = cell

    def show(self, energized: Set[Point2D]) -> None:
        show_dict_grid({(p.x, p.y): '#' if p in energized else c for p, c in self._grid.items()}, self._maxx, self._maxy)

    def energize(self, light: Tuple[Point2D, str]) -> Set[Point2D]:
        energized = set()
        visited = set()
        remaining = deque([light])
        while len(remaining):
            light_position, light_direction = remaining.pop()
            if light_position in self._grid:
                energized.add(light_position)
                if (light_position, light_direction) not in visited:
                    visited.add((light_position, light_direction))
                    for next_light_direction in light_ingress_egress[self._grid[light_position]][light_direction]:
                        remaining.append((light_position + directions[next_light_direction], next_light_direction))
        return energized


class Day16(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._input = [list(l) for l in self._load_input_as_lines()]

    def part_one(self):
        lc = LightContraption(self._input)
        energized = lc.energize((Point2D(0, 0), 'E'))
        lc.show(energized)
        return len(energized)

    def part_two(self):
        maxy = len(self._input)
        maxx = len(self._input[0])
        entries = []
        for x in range(maxx):
            entries.append((Point2D(x, 0), 'S'))
            entries.append((Point2D(x, maxy - 1), 'N'))
        for y in range(maxy):
            entries.append((Point2D(0, y), 'E'))
            entries.append((Point2D(maxx - 1, y), 'W'))

        lc = LightContraption(self._input)
        best = None
        best_c = 0
        for entry_point, entry_direction in entries:
            energized = lc.energize((entry_point, entry_direction))
            energized_c = len(energized)
            if energized_c > best_c:
                best = energized
                best_c = energized_c
        lc.show(best)
        return len(best)
