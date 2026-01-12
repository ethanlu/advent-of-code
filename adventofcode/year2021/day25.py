from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.grid import Point2D
from adventofcode.common.util import show_dict_grid
from itertools import cycle
from typing import List


processing = cycle('|/-\\')
deltas = {
    'east': Point2D(1, 0),
    'south': Point2D(0, 1)
}


class SeaFloor(object):
    def __init__(self, data: List[str]):
        self._maxy = len(data)
        self._maxx = len(data[0])
        self._east = set()
        self._south = set()
        for y, row in enumerate(data):
            for x, cell in enumerate(row):
                match cell:
                    case '>':
                        self._east.add(Point2D(x, y))
                    case 'v':
                        self._south.add(Point2D(x, y))
                    case '.':
                        pass
                    case _:
                        raise Exception(f"unexpected cell : {cell} at {x}, {y}")

    def show(self):
        grid = {}
        for y in range(self._maxy):
            for x in range(self._maxx):
                grid[(x, y)] = '.'
        for p in self._east:
            grid[(p.x, p.y)] = '>'
        for p in self._south:
            grid[(p.x, p.y)] = 'v'
        show_dict_grid(grid, self._maxx, self._maxy)

    def step(self) -> bool:
        total_moved = 0
        candidates = {(p + deltas['east'] if 0 <= (p + deltas['east']).x < self._maxx else Point2D(0, p.y)) : p for p in self._east}
        moved = set(candidates.keys()) - self._east - self._south
        total_moved += len(moved)
        self._east = (self._east - set((candidates[p] for p in moved))).union(moved)
        candidates = {(p + deltas['south'] if 0 <= (p + deltas['south']).y < self._maxy else Point2D(p.x, 0)): p for p in self._south}
        moved = set(candidates.keys()) - self._south - self._east
        self._south = (self._south - set((candidates[p] for p in moved))).union(moved)
        return total_moved > 0


class Day25(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._sf = SeaFloor(self._load_input_as_lines())

    def part_one(self):
        print(f"initial:")
        self._sf.show()
        i = 0
        print("\nstepping")
        while True:
            i += 1
            if i % 10 == 0:
                print('.', end="", flush=True)
            else:
                print(f"{next(processing)}", end="", flush=True)
                print("\b", end="", flush=True)
            had_movement = self._sf.step()
            if not had_movement:
                break
        print(f"step : {i}")
        self._sf.show()
        return i

    def part_two(self):
        pass
