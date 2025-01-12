from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.grid import Point2D
from adventofcode.common.util import show_dict_grid
from collections import deque
from functools import reduce
from typing import List

directions = {
    '^': Point2D(0, -1),
    '>': Point2D(1, 0),
    'v': Point2D(0, 1),
    '<': Point2D(-1, 0)
}


class Warehouse(object):
    def __init__(self, layout: List[str]):
        self._movements = ''
        self._boxes = {}
        self._walls = set([])
        self._robot = None
        self._width = len(layout[0])
        self._height = len(layout)

        for y, line in enumerate(layout):
            for x, cell in enumerate(line):
                p = Point2D(x, y)
                match cell:
                    case '@':
                        self._robot = p
                    case 'O' | '[' | ']':
                        self._boxes[p] = cell
                    case '#':
                        self._walls.add(p)

    @property
    def boxes(self) -> List[Point2D]:
        return [k for k, v in self._boxes.items()]

    def show(self) -> None:
        grid = {}
        for y in range(self._height):
            for x in range(self._width):
                p = Point2D(x, y)
                match (p in self._walls, p in self._boxes, p == self._robot):
                    case (True, False, False):
                        grid[(p.x, p.y)] = '#'
                    case (False, True, False):
                        grid[(p.x, p.y)] = self._boxes[p]
                    case (False, False, True):
                        grid[(p.x, p.y)] = '@'
                    case _:
                        grid[(p.x, p.y)] = '.'
        show_dict_grid(grid, self._width, self._height)

    def move(self, direction: str) -> None:
        boxes = []
        remaining = deque([self._robot])
        while len(remaining) > 0:
            next_p = remaining.pop() + directions[direction]
            match next_p in self._walls, next_p in self._boxes:
                case True, _:
                    # encountered a wall
                    break
                case False, True:
                    # encountered a box that might have to be moved
                    boxes.append(next_p)
                    remaining.appendleft(next_p)
        else:
            # encountered a free space before seeing a wall, so can move robot and all boxes in its way
            if boxes:
                # shifting all boxes in the way can be done by just moving the first box in the path to the end
                v = self._boxes.pop(boxes[0])
                self._boxes[(boxes[-1] + directions[direction])] = v
            self._robot += directions[direction]


class WideWarehouse(Warehouse):
    def __init__(self, layout: List[str]):
        expanded_layout = []
        for y, line in enumerate(layout):
            expanded_line = ''
            for c in line:
                match c:
                    case '#':
                        expanded_line += '##'
                    case 'O':
                        expanded_line += '[]'
                    case '.':
                        expanded_line += '..'
                    case '@':
                        expanded_line += '@.'
            expanded_layout.append(expanded_line)
        super().__init__(expanded_layout)

    @property
    def boxes(self) -> List[Point2D]:
        return [k for k, v in self._boxes.items() if v == '[']

    def move(self, direction: str) -> None:
        boxes = set([])
        remaining = deque([self._robot])
        while len(remaining) > 0:
            next_p = remaining.pop() + directions[direction]
            match next_p in self._walls, next_p in self._boxes:
                case True, _:
                    # encountered a wall
                    break
                case False, True:
                    # encountered a box that might have to be moved
                    boxes.add(next_p)
                    match direction:
                        case '^' | 'v':
                            # when moving vertically and encountering a box, will have to add either left or right side of the box depending what is encountered
                            remaining.appendleft(next_p)
                            if self._boxes[next_p] == '[':
                                next_p += Point2D(1, 0)
                                boxes.add(next_p)
                                remaining.appendleft(next_p)
                            if self._boxes[next_p] == ']':
                                boxes.add(next_p + Point2D(-1, 0))
                                remaining.appendleft(next_p + Point2D(-1, 0))
                        case '<' | '>':
                            # when moving horizontally and encountering a box, will first encounter either [ or ] of a box and then the other side...so can move twice
                            next_p += directions[direction]
                            boxes.add(next_p)
                            remaining.appendleft(next_p)
        else:
            # encountered a free space before seeing a wall, so can move robot and all boxes in its way
            if boxes:
                # shift all affected boxes
                new_boxes = {}
                for box in boxes:
                    new_boxes[box + directions[direction]] = self._boxes.pop(box)
                for k, v in new_boxes.items():
                    self._boxes[k] = v
            self._robot += directions[direction]


class Day15(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._layout = []
        self._movements = ''
        read_movements = False
        for line in self._load_input_as_lines():
            if not line:
                read_movements = True
                continue
            if read_movements:
                self._movements += line
            else:
                self._layout.append(line)

    def part_one(self):
        w = Warehouse(self._layout)
        for direction in self._movements:
            w.move(direction)
        w.show()
        return reduce(lambda total, p: total + (p.y * 100 + p.x), w.boxes, 0)

    def part_two(self):
        ww = WideWarehouse(self._layout)
        for direction in self._movements:
            ww.move(direction)
        ww.show()
        return reduce(lambda total, p: total + (p.y * 100 + p.x), ww.boxes, 0)
