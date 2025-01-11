from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.grid import Point2D
from adventofcode.common.range import Box2D
from adventofcode.common.util import show_dict_grid
from functools import reduce
from typing import List, Optional

import re


regex = re.compile(r'^p=(\d+),(\d+) v=(-?\d+),(-?\d+)$')


class Robot(object):
    def __init__(self, position: Point2D, velocity: Point2D):
        self._position = position
        self._velocity = velocity

    @property
    def position(self) -> Point2D:
        return self._position

    def move(self, width: int, height: int) -> None:
        self._position = Point2D((self._position.x + self._velocity.x) % width, (self._position.y + self._velocity.y) % height)


class Quadrant(object):
    def __init__(self, bound: Box2D):
        self._bound = bound
        self._width = bound.width + 1
        self._height = bound.height + 1
        self._robot_hash = [0] * self._width * self._height

    @property
    def robot_hash(self) -> str:
        return "".join((str(c) for c in self._robot_hash))

    @property
    def safety_factor(self) -> int:
        return sum([c for c in self._robot_hash])

    def _position_index(self, position: Point2D) -> int:
        return self._width * (abs(position.y - self._bound.top_left.y) % self._height) + (abs(position.x - self._bound.top_left.x) % self._width)

    def contains(self, position: Point2D) -> bool:
        return self._bound.contains(position)

    def decrement(self, position: Point2D) -> None:
        self._robot_hash[self._position_index(position)] -= 1

    def increment(self, position: Point2D) -> None:
        self._robot_hash[self._position_index(position)] += 1


class TileFloor(object):
    def __init__(self, width: int, height: int, robots: List[Robot]):
        self._width = width
        self._height = height
        self._robots = robots
        self._mid_x = width // 2
        self._mid_y = height // 2
        self._quadrants = [
            # top left
            Quadrant(Box2D(Point2D(0, 0), Point2D(self._mid_x - 1, self._mid_y - 1))),
            # top right
            Quadrant(Box2D(Point2D(self._mid_x + 1, 0), Point2D(self._width - 1, self._mid_y - 1))),
            # bottom left
            Quadrant(Box2D(Point2D(0, self._mid_y + 1), Point2D(self._mid_x - 1, self._height - 1))),
            # bottom right
            Quadrant(Box2D(Point2D(self._mid_x + 1, self._mid_y + 1), Point2D(self._width - 1, self._height - 1)))
        ]
        for r in self._robots:
            q = self._get_quadrant(r.position)
            if q:
                q.increment(r.position)

    @property
    def quadrants(self) -> List[Quadrant]:
        return self._quadrants

    def _get_quadrant(self, position: Point2D) -> Optional[Quadrant]:
        if 0 <= position.x < self._mid_x and 0 <= position.y < self._mid_y:
            return self._quadrants[0]
        if self._mid_x < position.x < self._width and 0 <= position.y < self._mid_y:
            return self._quadrants[1]
        if 0 <= position.x < self._mid_x and self._mid_y < position.y < self._height:
            return self._quadrants[2]
        if self._mid_x < position.x < self._width and self._mid_y < position.y < self._height:
            return self._quadrants[3]
        return None

    def show(self, show_full: bool) -> None:
        grid = {}
        for y in range(self._height):
            for x in range(self._width):
                grid[(x, y)] = '.'
        occupied = {}
        for r in self._robots:
            if r.position not in occupied:
                occupied[r.position] = 0
            occupied[r.position] += 1
        for position, value in occupied.items():
            grid[(position.x, position.y)] = str(value)
        if not show_full:
            for y in range(self._height):
                grid[(self._mid_x, y)] = ' '
            for x in range(self._width):
                grid[(x, self._mid_y)] = ' '
        show_dict_grid(grid, self._width, self._height)

    def step(self) -> None:
        for r in self._robots:
            current_position = r.position
            r.move(self._width, self._height)
            new_position = r.position
            if self._get_quadrant(current_position):
                self._get_quadrant(current_position).decrement(current_position)
            if self._get_quadrant(new_position):
                self._get_quadrant(new_position).increment(new_position)


class Day14(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._reset()

    def _reset(self):
        self._robots = []
        for line in self._load_input_as_lines():
            m = regex.match(line)
            self._robots.append(Robot(Point2D(int(m.groups()[0]), int(m.groups()[1])), Point2D(int(m.groups()[2]), int(m.groups()[3]))))

    def part_one(self):
        tf = TileFloor(101, 103, self._robots)
        for _ in range(100):
            tf.step()
        tf.show(False)
        return reduce(lambda total, quadrant: total * quadrant.safety_factor, tf.quadrants, 1)

    def part_two(self):
        self._reset()
        tf = TileFloor(101, 103, self._robots)
        safety_scores = {}
        for i in range(10000):
            tf.step()
            if i > 1000:
                score = reduce(lambda total, quadrant: total * quadrant.safety_factor, tf.quadrants, 1)
                if score not in safety_scores:
                    safety_scores[score] = []
                safety_scores[score].append(i + 1)

        safest = min(safety_scores[min(safety_scores.keys())])
        self._reset()
        tf = TileFloor(101, 103, self._robots)
        for i in range(safest):
            tf.step()
        tf.show(True)
        return safest
