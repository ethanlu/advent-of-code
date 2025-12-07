from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.grid import Point2D
from adventofcode.common.util import show_dict_grid
from typing import List, Set


class TachyonManifold(object):
    def __init__(self, data: List[str]):
        self._maxy = len(data)
        self._maxx = len(data[0])
        self._grid = {}
        self._beam_paths = {}
        self._wavefront = set()
        self._split_count = 0
        for y, row in enumerate(data):
            for x, cell in enumerate(row):
                p = Point2D(x, y)
                self._grid[p] = cell
                if cell == 'S':
                    self._wavefront.add(p)
                    self._beam_paths[p] = 1

    @property
    def split_count(self) -> int:
        return self._split_count

    @property
    def wavefront(self) -> Set[Point2D]:
        return self._wavefront

    @property
    def beams(self) -> int:
        return sum((v for p, v in self._beam_paths.items() if p.y == (self._maxy-1)))

    def _propagate_beam(self, p: Point2D, amount: int) -> None:
        if p not in self._beam_paths:
            self._beam_paths[p] = 0
        self._beam_paths[p] += amount

    def show(self) -> None:
        show_dict_grid({(p.x, p.y): v for p, v in self._grid.items()}, self._maxx, self._maxy)

    def step(self) -> None:
        new_wavefront = set()
        for p in self._wavefront:
            new_p = p + Point2D(0, 1)
            if new_p in self._grid:
                match self._grid[new_p]:
                    case '.' | '|':
                        self._grid[new_p] = '|'
                        new_wavefront.add(new_p)
                        self._propagate_beam(new_p, self._beam_paths[p])
                    case '^':
                        self._split_count += 1
                        new_left_p = new_p + Point2D(-1, 0)
                        if new_left_p in self._grid:
                            self._grid[new_left_p] = '|'
                            new_wavefront.add(new_left_p)
                            self._propagate_beam(new_left_p, self._beam_paths[p])
                        new_right_p = new_p + Point2D(1, 0)
                        if new_right_p in self._grid:
                            self._grid[new_right_p] = '|'
                            new_wavefront.add(new_right_p)
                            self._propagate_beam(new_right_p, self._beam_paths[p])
                    case _:
                        raise Exception(f"unexpected encounter in tachyon manifold at position {new_p} : {self._grid[new_p]}")
        self._wavefront = new_wavefront


class Day07(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._tm = TachyonManifold(self._load_input_as_lines())

    def part_one(self):
        while self._tm.wavefront:
            self._tm.step()
        self._tm.show()
        return self._tm.split_count

    def part_two(self):
        return self._tm.beams
