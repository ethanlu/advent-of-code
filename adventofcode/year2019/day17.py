from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.grid import Point2D
from adventofcode.year2019.day09 import IntCodeCPUComplete
from typing import Iterable, List, Set, Tuple

import math


orientation_codes = (94, 62, 118, 60)
orientations = ('U', 'R', 'D', 'L')
deltas = (Point2D(0, -1), Point2D(1, 0), Point2D(0, 1), Point2D(-1, 0))


class MovementSplitter(object):
    def __init__(self, path: str, max_size: int):
        self._path = self._chunkify(path)
        self._max_size = max_size

    def _chunkify(self, iterable: Iterable) -> List[str]:
        result = []
        chunks = []
        for c in iterable:
            if c in ('L', 'R') and len(chunks) > 0:
                result.append("".join(chunks))
                chunks = [c]
            else:
                chunks.append(c)
        result.append("".join(chunks))
        return result

    def find_split(self) -> Tuple[str, str, str]:
        # find a split of the path that yields 3 substrings that completely cover the path
        max_moves = math.ceil(len(self._path) / 3)

        path_a = self._path
        for a_end in range(max_moves, 1, -1):
            a = "".join(path_a[0:a_end])
            a_serialized = ",".join(path_a[0:a_end])
            if len(a_serialized) > self._max_size:
                # length of candidate sequence for function A is too big when serialized
                continue

            path_b = self._chunkify("".join(path_a).replace(a, ''))
            for b_end in range(max_moves, 1, -1):
                b = "".join(path_b[0:b_end])
                b_serialized = ",".join(path_b[0:b_end])
                if len(b_serialized) > self._max_size:
                    # length of candidate sequence for function B is too big
                    continue

                path_c = self._chunkify("".join(path_b).replace(b, ''))
                for c_end in range(max_moves, 1, -1):
                    c = "".join(path_c[0:c_end])
                    c_serialized = ",".join(path_c[0:c_end])
                    if len(c_serialized) > self._max_size:
                        # length of candidate sequence for function C is too big
                        continue

                    if len("".join(self._path).replace(a, 'X').replace(b, 'X').replace(c, 'X').replace('X', '')) == 0:
                        # found valid split if a, b, and c completely replaces the original path
                        return a, b, c
        return '', '', ''


class VacuumBot(object):
    def __init__(self, program: List[int], verbose: bool = False):
        self._cpu = IntCodeCPUComplete(program, verbose)
        self._scaffolds: Set[Point2D] = set([])
        self._screen: List[int] = []
        self._orientation_index = 0
        self._position: Point2D = Point2D(0, 0)
        self._path = []

    @property
    def scaffolds(self) -> Set[Point2D]:
        return self._scaffolds

    def _serialize_routine(self, s: str) -> List[int]:
        return [ord(c) for c in ",".join(list(s))] + [10]

    def _serialize_function(self, s: str):
        result = []
        for c in list(s):
            if c in ('L', 'R'):
                result.append(ord(','))
                result.append(ord(c))
                result.append(ord(','))
            else:
                result.append(ord(c))
        result.append(10)
        return result[1:]

    def scan(self) -> None:
        x = y = 0
        while not self._cpu.halted:
            self._cpu.run()
            output = self._cpu.get_output()
            match output:
                case 35:
                    self._scaffolds.add(Point2D(x, y))
                case 60 | 62 | 94 | 118:
                    self._scaffolds.add(Point2D(x, y))
                    self._position = Point2D(x, y)
                    self._orientation_index = orientation_codes.index(output)
                case 10:
                    y += 1
                    x = -1
            x += 1
            self._screen.append(output)

    def notify(self, routine: str, a: str, b: str, c:str) -> int:
        self._cpu.write_memory(0, 2)

        # input main routine
        for n in self._serialize_routine(routine):
            self._cpu.add_input(n)

        # input functions
        for n in self._serialize_function(a):
            self._cpu.add_input(n)
        for n in self._serialize_function(b):
            self._cpu.add_input(n)
        for n in self._serialize_function(c):
            self._cpu.add_input(n)

        # input live feed
        self._cpu.add_input(ord('n'))
        self._cpu.add_input(10)

        while not self._cpu.halted:
            self._cpu.run()
            dusted = self._cpu.get_output()

        return dusted

    def path(self) -> str:
        p = []
        done = False
        position = self._position
        orientation_index = self._orientation_index
        steps = 0
        while not done:
            next_position = position + deltas[orientation_index]
            if next_position in self._scaffolds:
                # can still move forward in the current orientation
                steps += 1
                position = next_position
            else:
                # current orientation reached an end...log steps taken
                if steps > 0:
                    p.append(str(steps))

                # find next orientation
                if (position + deltas[(orientation_index + 1) % 4]) in self._scaffolds:
                    # can turn right
                    orientation_index = (orientation_index + 1) % 4
                    p.append('R')
                elif (position + deltas[(orientation_index - 1) % 4]) in self._scaffolds:
                    # can turn left
                    orientation_index = (orientation_index - 1) % 4
                    p.append('L')
                else:
                    # turning left or right yields dead end as well...reached end
                    done = True
                steps = 0
        return "".join(p)

    def show(self) -> None:
        print("".join((chr(n) for n in self._screen)))

class Day17(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._input = [int(i) for i in self._load_input_as_string().split(',')]

    def part_one(self):
        robot = VacuumBot(self._input)
        robot.scan()
        robot.show()

        alignment = 0
        for scaffold in robot.scaffolds:
            alignment += (scaffold.x * scaffold.y) if sum((1 for t in (scaffold + d for d in deltas) if t in robot.scaffolds)) > 2 else 0

        return alignment

    def part_two(self):
        robot = VacuumBot(self._input)
        robot.scan()
        path = robot.path()
        print(f"path : {path}")

        ms = MovementSplitter(path, 20)
        a, b, c = ms.find_split()
        print(f"functions : A={a}, B={b}, C={c}")

        routine = path.replace(a, 'A').replace(b, 'B').replace(c, 'C')
        print(f"routine : {routine}")

        robot = VacuumBot(self._input)
        return robot.notify(routine, a, b, c)
