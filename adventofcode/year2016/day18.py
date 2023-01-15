from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.util import show_grid
from itertools import tee
from typing import Iterable, List


def triplets(iterable: Iterable):
    a, b, c = tee(iterable, 3)
    next(b, None)
    next(c, None)
    next(c, None)
    return zip(a, b, c)


class Room(object):
    def __init__(self, initial_tiles: str):
        self._tiles = [[c for c in initial_tiles]]
        self._safe_tiles = sum((1 for c in self._tiles[0] if c == '.'))

    @property
    def safe_tiles(self) -> int:
        return self._safe_tiles

    @property
    def tiles(self) -> List[List[str]]:
        return self._tiles

    def advance(self, rows: int):
        for i in range(rows):
            rows = []
            for (left, center, right) in triplets(['.'] + self._tiles[-1] + ['.']):
                match [left, center, right]:
                    case ['^', '^', '.'] | ['.', '^', '^'] | ['^', '.', '.'] | ['.', '.', '^']:
                        rows.append('^')
                    case _:
                        rows.append('.')
                        self._safe_tiles += 1
            self._tiles.append(rows)


class Day18(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._input = self._load_input_as_string()

    def part_one(self):
        r = Room(self._input)
        r.advance(39)

        show_grid(r.tiles)

        return r.safe_tiles

    def part_two(self):
        r = Room(self._input)
        r.advance(399999)

        show_grid(r.tiles)

        return r.safe_tiles
