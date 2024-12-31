from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.grid import Point2D
from adventofcode.common.util import show_dict_grid
from typing import List, Set


class WordSearch(object):
    def __init__(self, data: List[List[str]]):
        self._grid = {}
        self._maxy = len(data)
        self._maxx = len(data[0])

        for y, row in enumerate(data):
            for x, cell in enumerate(row):
                self._grid[Point2D(x, y)] = cell


    @property
    def maxx(self) -> int:
        return self._maxx

    @property
    def maxy(self) -> int:
        return self._maxy

    def cell(self, p: Point2D) -> str:
        return self._grid[p] if p in self._grid else ''

    def show(self, keep: Set[Point2D]):
        grid = {}
        for y in range(self._maxy):
            for x in range(self._maxx):
                p = Point2D(x, y)
                grid[p] = self._grid[p] if p in keep else '.'
        show_dict_grid({(p.x, p.y): v for p, v in grid.items()}, self._maxx, self._maxy)


class Day04(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._ws = WordSearch([list(line) for line in self._load_input_as_lines()])

    def part_one(self):
        word = 'XMAS'
        found = 0
        keep = set([])
        for y in range(self._ws.maxy):
            for x in range(self._ws.maxx):
                current = Point2D(x, y)
                if self._ws.cell(current) == word[0]:
                    # check all 8 cardinal directions when current cell starts with the first letter of XMAS
                    for delta in (Point2D(-1, -1), Point2D(-1, 0), Point2D(-1, 1), Point2D(0, -1), Point2D(0, 1), Point2D(1, -1), Point2D(1, 0), Point2D(1, 1)):
                        valid = []
                        c = current
                        for i in range(len(word)):
                            if self._ws.cell(c) == word[i]:
                                valid.append(c)
                                c += delta
                            else:
                                break
                        else:
                            found += 1
                            keep.update(set(valid))
        self._ws.show(keep)
        return found

    def part_two(self):
        word = 'MAS'
        found = 0
        keep = set([])
        for y in range(self._ws.maxy):
            for x in range(self._ws.maxx):
                current = Point2D(x, y)
                if self._ws.cell(current) == word[1]:
                    # check diagonal directions when current cell is the middle letter of MAS
                    diagonal1 = [self._ws.cell(current + Point2D(-1, -1)), self._ws.cell(current), self._ws.cell(current + Point2D(1, 1))]
                    diagonal2 = [self._ws.cell(current + Point2D(-1, 1)), self._ws.cell(current), self._ws.cell(current + Point2D(1, -1))]
                    word1 = "".join(diagonal1)
                    word2 = "".join(diagonal2)
                    if (word1 == word or word1 == word[::-1]) and (word2 == word or word2 == word[::-1]):
                        found += 1
                        keep.update(set([current + Point2D(-1, -1), current, current + Point2D(1, 1)]))
                        keep.update(set([current + Point2D(-1, 1), current, current + Point2D(1, -1)]))
        self._ws.show(keep)
        return found
