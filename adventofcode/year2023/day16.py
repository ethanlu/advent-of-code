from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.grid import Point2D
from adventofcode.common.util import show_dict_grid
from collections import deque
from typing import List, Set, Tuple


directions = {'N': Point2D(0, -1), 'S': Point2D(0, 1), 'W': Point2D(-1, 0), 'E': Point2D(1, 0)}
light_ingress_egress = {
    '.': {'N': {'N'}, 'S': {'S'}, 'W': {'W'}, 'E': {'E'}},
    '/': {'N': {'E'}, 'S': {'W'}, 'W': {'S'}, 'E': {'N'}},
    '\\': {'N': {'W'}, 'S': {'E'}, 'W': {'N'}, 'E': {'S'}},
    '-': {'N': {'W', 'E'}, 'S': {'W', 'E'}, 'W': {'W'}, 'E': {'E'}},
    '|': {'N': {'N'}, 'S': {'S'}, 'W': {'N', 'S'}, 'E': {'N', 'S'}},
}


class Cell(object):
    def __init__(self, value: str):
        self._value = value
        self._light_egress = set()

    @property
    def light_egress(self) -> Set[str]:
        return self._light_egress

    @property
    def value(self) -> str:
        return self._value

    def add_light_ingress(self, ingress: str) -> List[str]:
        new_egress = light_ingress_egress[self._value][ingress].difference(self._light_egress)
        if new_egress:
            self._light_egress = self._light_egress.union(new_egress)
            return list(new_egress)
        return []


class LightContraption(object):
    def __init__(self, data: List[List[str]]):
        self._maxy = len(data)
        self._maxx = len(data[0])
        self._grid = {}
        for y, row in enumerate(data):
            for x, cell in enumerate(row):
                self._grid[Point2D(x, y)] = Cell(cell)

    @property
    def energized(self) -> int:
        return sum((1 for cell in self._grid.values() if len(cell.light_egress) > 0))

    def show(self) -> None:
        show_dict_grid({(p.x, p.y): '#' if len(c.light_egress) > 0 else c.value for p, c in self._grid.items()}, self._maxx, self._maxy)

    def energize(self, light: Tuple[Point2D, str]) -> None:
        remaining = deque([light])
        while len(remaining):
            light_position, light_direction = remaining.pop()
            next_light_position = light_position + directions[light_direction]
            if next_light_position in self._grid:
                for light_egress in self._grid[next_light_position].add_light_ingress(light_direction):
                    remaining.append((next_light_position, light_egress))


class Day16(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._input = [list(l) for l in self._load_input_as_lines()]

    def part_one(self):
        lc = LightContraption(self._input)
        lc.energize((Point2D(-1, 0), 'E'))
        lc.show()
        return lc.energized

    def part_two(self):
        maxy = len(self._input)
        maxx = len(self._input[0])
        entries = []
        for x in range(maxx):
            entries.append((Point2D(x, -1), 'S'))
            entries.append((Point2D(x, maxy), 'N'))
        for y in range(maxy):
            entries.append((Point2D(-1, y), 'E'))
            entries.append((Point2D(maxx, y), 'W'))

        best = 0
        best_configuration = None
        for entry_point, entry_direction in entries:
            lc = LightContraption(self._input)
            lc.energize((entry_point, entry_direction))
            e = lc.energized
            if e > best:
                best = e
                best_configuration = lc
        best_configuration.show()
        return best
