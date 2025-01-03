from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.grid import Point2D
from adventofcode.common.util import show_dict_grid
from typing import List, Tuple


directions = {
    '^': (Point2D(0, -1), '>'),
    '>': (Point2D(1, 0), 'v'),
    'v': (Point2D(0, 1), '<'),
    '<': (Point2D(-1, 0), '^')
}


class Step(object):
    def __init__(self, position: Point2D, direction: str):
        self._position = position
        self._direction = direction

    def __eq__(self, other):
        return self.position == other.position and self.direction == other.direction if issubclass(type(other), Step) else False

    def __ne__(self, other):
        return self.position != other.position or self.direction != other.direction if issubclass(type(other), Step) else True

    def __hash__(self):
        return self.position.__hash__() * ord(self.direction)

    @property
    def position(self) -> Point2D:
        return self._position

    @property
    def direction(self) -> str:
        return self._direction

    def move(self) -> Step:
        return Step(self.position + directions[self.direction][0], self.direction)

    def turn(self) -> Step:
        return Step(self.position, directions[self.direction][1])


class GuardPatrol(object):
    def __init__(self, data: List[List[str]]):
        self._grid = {}
        self._start = None
        self._maxy = len(data)
        self._maxx = len(data[0])

        for y, row in enumerate(data):
            for x, cell in enumerate(row):
                p = Point2D(x, y)
                self._grid[p] = cell
                match cell:
                    case '^' | '>' | 'v' | '<':
                        self._start = Step(p, cell)
                        self._grid[p] = '.'

    def add_obstacle(self, position: Point2D) -> None:
        self._grid[position] = 'O'

    def remove_obstacle(self, position: Point2D) -> None:
        self._grid[position] = '.'

    def show(self, path: List[Step]) -> None:
        grid = {}
        for y in range(self._maxy):
            for x in range(self._maxx):
                p = Point2D(x, y)
                grid[p] = self._grid[p]
        for ps in path:
            match grid[ps.position]:
                case '.':
                    grid[ps.position] = '|' if ps.direction in ('^', 'v') else '-'
                case '|' | '-':
                    grid[ps.position] = '+'
                case _:
                    raise Exception(f"Unexpected path direction encountered : {grid[ps.position]}")
        grid[self._start.position] = self._start.direction
        show_dict_grid({(p.x, p.y): v for p, v in grid.items()}, self._maxx, self._maxy)

    def patrol(self) -> Tuple[bool, List[Step]]:
        path = {}
        step = self._start
        while True:
            path[step] = None
            next_step = step.move()

            if next_step.position not in self._grid:
                # reached edge of map
                looped = False
                break
            if next_step in path:
                # reached a patrol loop
                looped = True
                break

            while self._grid[next_step.position] != '.':
                # if next position is an obstacle, keep turning right until it no longer is
                step = step.turn()
                next_step = step.move()
            step = next_step
        return looped, list(path.keys())


class Day06(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._gp = GuardPatrol([list(line) for line in self._load_input_as_lines()])

    def part_one(self):
        looped, path = self._gp.patrol()
        if looped:
            raise Exception("unexpected patrol loop encountered")
        self._gp.show(path)
        return len(set([ps.position for ps in path]))

    def part_two(self):
        looped, path = self._gp.patrol()
        if looped:
            raise Exception("unexpected patrol loop encountered")
        looped_paths = 0
        processed = set([])
        for s in path[1:]:
            if s.position in processed:
                continue
            processed.add(s.position)
            self._gp.add_obstacle(s.position)
            looped, _ = self._gp.patrol()
            if looped:
                looped_paths += 1
            self._gp.remove_obstacle(s.position)
        return looped_paths
