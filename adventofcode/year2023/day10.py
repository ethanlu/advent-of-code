from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.grid import Point2D
from adventofcode.common.util import show_dict_grid
from random import choice
from typing import Dict, List, Optional, Set, Tuple


directions = {'N': Point2D(0, -1), 'S': Point2D(0, 1), 'E': Point2D(1, 0), 'W': Point2D(-1, 0)}


# Dict[pipe_type, Dict[ingress, egress]]
pipe_ingress_egress = {
    '|': {'N': 'N', 'S': 'S'},
    '-': {'W': 'W', 'E': 'E'},
    'J': {'S': 'W', 'E': 'N'},
    'L': {'S': 'E', 'W': 'N'},
    '7': {'N': 'W', 'E': 'S'},
    'F': {'N': 'E', 'W': 'S'}
}


class PipeMaze(object):
    def __init__(self, pipes: List[List[str]]):
        self._maxy = len(pipes)
        self._maxx = len(pipes[0])
        self._maze: Dict[Point2D, str] = {}
        for y, row in enumerate(pipes):
            for x, cell in enumerate(row):
                p = Point2D(x, y)
                self._maze[p] = cell
                if cell == 'S':
                    self._start = p

        # convert starting pipe from S to correct pipe representation
        if self.cell(self.start + directions['N']) in ('|', '7', 'F') and self.cell(self.start + directions['S']) in ('|', 'J', 'L'):
            self._maze[self.start] = '|'
        if self.cell(self.start + directions['W']) in ('-', 'F', 'L') and self.cell(self.start + directions['E']) in ('-', 'J', '7'):
            self._maze[self.start] = '-'
        if self.cell(self.start + directions['N']) in ('|', '7', 'F') and self.cell(self.start + directions['W']) in ('-', 'F', 'L'):
            self._maze[self.start] = 'J'
        if self.cell(self.start + directions['N']) in ('|', '7', 'F') and self.cell(self.start + directions['E']) in ('-', '7', 'J'):
            self._maze[self.start] = 'L'
        if self.cell(self.start + directions['S']) in ('|', 'J', 'L') and self.cell(self.start + directions['W']) in ('-', 'F', 'L'):
            self._maze[self.start] = '7'
        if self.cell(self.start + directions['S']) in ('|', 'J', 'L') and self.cell(self.start + directions['E']) in ('-', '7', 'J'):
            self._maze[self.start] = 'F'

    @property
    def maxy(self) -> int:
        return self._maxy

    @property
    def maxx(self) -> int:
        return self._maxx

    @property
    def start(self) -> Point2D:
        return self._start

    @property
    def start_faces(self) -> List[str]:
        return list(pipe_ingress_egress[self._maze[self._start]].values())

    def cell(self, p: Point2D) -> Optional[str]:
        return self._maze[p] if p in self._maze else None

    def move(self, position: Point2D, facing: str) -> Tuple[Point2D, str]:
        if position not in self._maze:
            raise Exception(f"Unexpected position {position} ")
        next_position = position + directions[facing]
        if self._maze[next_position] in pipe_ingress_egress.keys():
            next_facing = pipe_ingress_egress[self._maze[next_position]][facing]
        else:
            raise Exception(f"Next position {next_position} contains unexpected pipe state : {self._maze[next_position]}")
        return next_position, next_facing

    def clean(self, pipe_path: Set[Point2D]) -> None:
        for p in self._maze.keys():
            if p not in pipe_path:
                self._maze[p] = "."

    def crossed(self, position: Point2D, direction: str) -> int:
        crossed = 0
        if position in self._maze:
            encounters = {'|': 0, '-': 0, 'J': 0, 'L': 0, '7': 0, 'F': 0, '.': 0}
            match direction:
                case 'N':
                    points = (Point2D(position.x, y) for y in reversed(range(position.y)))
                case 'S':
                    points = (Point2D(position.x, y) for y in range(position.y + 1, self._maxy))
                case 'W':
                    points = (Point2D(x, position.y) for x in reversed(range(position.x)))
                case 'E':
                    points = (Point2D(x, position.y) for x in range(position.x + 1, self._maxx))
                case _:
                    raise Exception(F"Invalid direction {direction} encountered")
            for p in points:
                encounters[self.cell(p)] += 1
            if direction in ('N', 'S'):
                # when checking vertical directions, any - pipe is considered a cross and if there are any unpaired F, L or 7, J pipes
                crossed = encounters['-']
                if abs(encounters['F'] - encounters['L']) % 2 == 1 or abs(encounters['7'] - encounters['J']) % 2 == 1:
                    crossed += 1
            if direction in ('W', 'E'):
                # when checking horizontal directions, any | pipe is considered a cross and if there are any unpaired F, 7 or L, J pipes
                crossed = encounters['|']
                if abs(encounters['F'] - encounters['7']) % 2 == 1 or abs(encounters['L'] - encounters['J']) % 2 == 1:
                    crossed += 1
        return crossed

class Day10(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._pm = PipeMaze([list(l) for l in self._load_input_as_lines()])

    def part_one(self):
        steps = 1
        position, facing = self._pm.move(self._pm.start, self._pm.start_faces[0])
        while position != self._pm.start:
            position, facing = self._pm.move(position, facing)
            steps += 1
        print(f"pipe loop is {steps} steps long")
        return steps // 2

    def part_two(self):
        pipe_path = {self._pm.start}
        position, facing = self._pm.move(self._pm.start, self._pm.start_faces[0])
        while position != self._pm.start:
            pipe_path.add(position)
            position, facing = self._pm.move(position, facing)

        # convert all tiles that are not part of pipe path to .
        self._pm.clean(pipe_path)

        inside = 0
        grid = {}
        for y in range(self._pm.maxy):
            for x in range(self._pm.maxx):
                p = Point2D(x, y)
                if p in pipe_path:  # cell in pipe maze is part of pipe path...skip
                    grid[(p.x, p.y)] = self._pm.cell(p)
                    continue
                else:               # cell in pipe maze is not part of pipe path...determine if it is inside or outside
                    cross_count = self._pm.crossed(p, choice(list(directions.keys())))
                    if (cross_count % 2) == 1:
                        grid[(p.x, p.y)] = 'I'
                        inside += 1
                    else:
                        grid[(p.x, p.y)] = 'O'
        show_dict_grid(grid, self._pm.maxx, self._pm.maxy)
        return inside
