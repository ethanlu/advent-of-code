from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.grid import Point2D
from adventofcode.common.range import Box2D
from adventofcode.common.util import show_dict_grid
from itertools import combinations, pairwise
from typing import List, Tuple


def area(p1: Point2D, p2: Point2D) -> int:
    return (abs(p1.x - p2.x) + 1) * (abs(p1.y - p2.y) + 1)


def show(corners, maxx, maxy, p1, p2):
    grid = {}
    for y in range(maxy):
        for x in range(maxx):
            grid[(x, y)] = '.'
    for p in corners:
        grid[(p.x, p.y)] = 'O'
    grid[(p1.x, p1.y)] = 'X'
    grid[(p2.x, p2.y)] = 'X'
    show_dict_grid(grid, maxx, maxy)


class Day09(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._maxy = 0
        self._maxx = 0
        self._corners = []
        for line in self._load_input_as_lines():
            x, y = [int(s) for s in line.split(',')]
            self._corners.append(Point2D(x, y))
            self._maxy = y if y > self._maxy else self._maxy
            self._maxx = x if x > self._maxx else self._maxx
        self._maxy += 3
        self._maxx += 3

    def part_one(self):
        largest = sorted(combinations(self._corners, 2), key=lambda p: area(p[0], p[1]))[-1]
        print(f"largest rectangle formed with {largest[0]} and {largest[1]}")
        return area(largest[0], largest[1])

    def part_two(self):
        # not a general solution
        # assumes the input file forms a large circle with a long thing gap that is cut out from the center to one of the edge
        # this means the largest rectangle would not contain any other corner within itself
        boundaries = [Box2D(Point2D(min(p1.x, p2.x), min(p1.y, p2.y)), Point2D(max(p1.x, p2.x), max(p1.y, p2.y))) for p1, p2 in pairwise(self._corners)]
        boundaries.append(Box2D(
            Point2D(min(self._corners[0].x, self._corners[-1].x), min(self._corners[0].y, self._corners[-1].y)),
            Point2D(max(self._corners[0].x, self._corners[-1].x), max(self._corners[0].y, self._corners[-1].y))))
        largest = None
        i = 0
        for p1, p2 in reversed(sorted(combinations(self._corners, 2), key=lambda p: area(p[0], p[1]))):
            if i % 1000 == 0:
                print(f"{i} processed")
            candidate = Box2D(Point2D(min(p1.x, p2.x), min(p1.y, p2.y)), Point2D(max(p1.x, p2.x), max(p1.y, p2.y)))
            # candidate rectangle is valid if all corners are either outside or only along the edge of the rectangle. it is invalid if there is any corners inside the rectangle
            for b in boundaries:
                if candidate.overlaps(b):
                    delta = Point2D(1 if b.top_left.x != b.bottom_right.x else 0, 1 if b.top_left.y != b.bottom_right.y else 0)
                    current = b.top_left
                    intersects = False
                    while current != b.bottom_right:
                        if candidate.top_left.x < current.x < candidate.bottom_right.x and candidate.top_left.y < current.y < candidate.bottom_right.y:
                            # boundary points are inside the rectangle
                            intersects = True
                            break
                        current = current + delta
                    if intersects:
                        # found an intersection with a boundary and the rectangle
                        break
            else:
                # rectangle is valid because no corners were inside it
                largest = (p1, p2)
                break
            i += 1
        #show(self._corners, self._maxx, self._maxy, largest[0], largest[1])
        return area(largest[0], largest[1])
