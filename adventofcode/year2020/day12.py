from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.grid import Point2D
from collections import deque
from typing import List


class NavigationSystem(object):
    def __init__(self, actions: List[str]):
        self._actions = actions
        self._position = Point2D(0, 0)
        self._facing = deque(['E', 'S', 'W', 'N'])

    @property
    def position(self) -> Point2D:
        return self._position

    def north(self, steps: int) -> None:
        self._position = Point2D(self._position.x, self._position.y + steps)

    def south(self, steps: int) -> None:
        self._position = Point2D(self._position.x, self._position.y - steps)

    def west(self, steps: int) -> None:
        self._position = Point2D(self._position.x - steps, self._position.y)

    def east(self, steps: int) -> None:
        self._position = Point2D(self._position.x + steps, self._position.y)

    def left(self, degree: int) -> None:
        self._facing.rotate(degree // 90)

    def right(self, degree: int) -> None:
        self._facing.rotate(-(degree // 90))

    def forward(self, steps: int) -> None:
        match self._facing[0]:
            case 'N':
                self.north(steps)
            case 'S':
                self.south(steps)
            case 'W':
                self.west(steps)
            case 'E':
                self.east(steps)
            case _:
                raise Exception(f"Invalid facing : {self._facing[0]}")

    def navigate(self):
        for action in self._actions:
            match action[0], int(action[1:]):
                case 'N', steps:
                    self.north(steps)
                case 'S', steps:
                    self.south(steps)
                case 'W', steps:
                    self.west(steps)
                case 'E', steps:
                    self.east(steps)
                case 'L', degree:
                    self.left(degree)
                case 'R', degree:
                    self.right(degree)
                case 'F', steps:
                    self.forward(steps)
                case _:
                    raise Exception(f"Invalid action : {action}")


class WaypointNavigationSystem(NavigationSystem):
    def __init__(self, actions: List[str]):
        super().__init__(actions)
        self._waypoint = Point2D(10, 1)

    @property
    def waypoint(self) -> Point2D:
        return self._waypoint

    def north(self, steps: int) -> None:
        self._waypoint = Point2D(self._waypoint.x, self._waypoint.y + steps)

    def south(self, steps: int) -> None:
        self._waypoint = Point2D(self._waypoint.x, self._waypoint.y - steps)

    def west(self, steps: int) -> None:
        self._waypoint = Point2D(self._waypoint.x - steps, self._waypoint.y)

    def east(self, steps: int) -> None:
        self._waypoint = Point2D(self._waypoint.x + steps, self._waypoint.y)

    def left(self, degree: int) -> None:
        match degree:
            case 90:
                self._waypoint = Point2D(-self._waypoint.y, self._waypoint.x)
            case 180:
                self._waypoint = Point2D(-self._waypoint.x, -self._waypoint.y)
            case 270:
                self._waypoint = Point2D(self._waypoint.y, -self._waypoint.x)
            case _:
                raise Exception(f"Invalid degree : {degree}")

    def right(self, degree: int) -> None:
        match degree:
            case 90:
                self._waypoint = Point2D(self._waypoint.y, -self._waypoint.x)
            case 180:
                self._waypoint = Point2D(-self._waypoint.x, -self._waypoint.y)
            case 270:
                self._waypoint = Point2D(-self._waypoint.y, self._waypoint.x)
            case _:
                raise Exception(f"Invalid degree : {degree}")

    def forward(self, steps: int) -> None:
        self._position += Point2D(self._waypoint.x * steps, self._waypoint.y * steps)


class Day12(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._input = self._load_input_as_lines()

    def part_one(self):
        ns = NavigationSystem(self._input)
        ns.navigate()
        print(f"position: {ns.position}")
        return abs(ns.position.x) + abs(ns.position.y)

    def part_two(self):
        ns = WaypointNavigationSystem(self._input)
        ns.navigate()
        print(f"waypoint: {ns.waypoint}")
        print(f"position: {ns.position}")
        return abs(ns.position.x) + abs(ns.position.y)
    