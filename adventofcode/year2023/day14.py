from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.grid import Point2D
from adventofcode.common.util import show_dict_grid
from typing import List, Tuple


shift_deltas = {'N': Point2D(0, 1), 'E': Point2D(-1, 0), 'S': Point2D(0, -1), 'W': Point2D(1, 0)}


class ParabolicReflectorDish(object):
    def __init__(self, data: List[List[str]]):
        self._grid = {}
        self._maxy = len(data)
        self._maxx = len(data[0])

        for y, row in enumerate(data):
            for x, cell in enumerate(row):
                self._grid[Point2D(x, y)] = cell

    def __str__(self) -> str:
        return "".join((v for v in self._grid.values()))

    def tilt(self, direction: str) -> None:
        match direction:
            case 'N':
                shift_sequence = ((Point2D(x, y) for y in range(self._maxy)) for x in range(self._maxx))
            case 'S':
                shift_sequence = ((Point2D(x, y) for y in reversed(range(self._maxy))) for x in range(self._maxx))
            case 'W':
                shift_sequence = ((Point2D(x, y) for x in range(self._maxx)) for y in range(self._maxy))
            case 'E':
                shift_sequence = ((Point2D(x, y) for x in reversed(range(self._maxx))) for y in range(self._maxy))
            case _:
                raise Exception(f"Invalid tilt direction {direction}")
        for sequence in shift_sequence:
            next_free_position = None
            for p in sequence:
                match self._grid[p]:
                    case '.':   # set next free position to this if it has not been set yet
                        if not next_free_position:
                            next_free_position = p
                    case '#':   # this square rock will stop any further rolls from round rocks, so must find the next free position
                        next_free_position = None
                    case 'O':   # move this round rock to the next free position if available and move next free position over. otherwise
                        if next_free_position:
                            self._grid[next_free_position], self._grid[p] = self._grid[p], self._grid[next_free_position]
                            next_free_position = next_free_position + shift_deltas[direction]
                            if not (0 <= next_free_position.x < self._maxx and 0 <= next_free_position.y < self._maxy):
                                next_free_position = None
                    case _:
                        raise Exception(f"Unexpected grid cell at {p} with value {self._grid[p]}")

    def load(self, direction: str) -> int:
        match direction:
            case 'N':
                count_sequence = ((self._maxy - y for x in range(self._maxx) if self._grid[Point2D(x,y)] == 'O') for y in range(self._maxy))
            case 'S':
                count_sequence = ((y for x in range(self._maxx) if self._grid[Point2D(x,y)] == 'O') for y in range(self._maxy))
            case 'W':
                count_sequence = ((self._maxx - x for y in range(self._maxy) if self._grid[Point2D(x,y)] == 'O') for x in range(self._maxx))
            case 'E':
                count_sequence = ((x for y in range(self._maxy) if self._grid[Point2D(x,y)] == 'O') for x in range(self._maxx))
            case _:
                raise Exception(f"Invalid tilt direction {direction}")

        load = 0
        for sequence in count_sequence:
            load += sum(sequence)
        return load

    def show(self) -> None:
        show_dict_grid({(p.x, p.y): v for p, v in self._grid.items()}, self._maxx, self._maxy)


class Day14(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._prb = ParabolicReflectorDish([list(l) for l in self._load_input_as_lines()])
        self._prb.show()

    def part_one(self):
        self._prb.tilt('N')
        self._prb.show()
        return self._prb.load('N')

    def part_two(self):
        cycle_fingerprints = {}
        max_cycle = 1000000000
        cycle = 0
        while cycle < max_cycle:
            cycle += 1
            for t in ('N', 'W', 'S', 'E'):
                self._prb.tilt(t)

            fingerprint = str(self._prb)
            if fingerprint not in cycle_fingerprints:
                # arrangement has never been seen....we are in a new cycle so reset cycle jump back to 1 to build cache profile of it
                cycle_fingerprints[fingerprint] = cycle
            else:
                # we have encountered this cycle before, so calculate the difference in cycles from the last time we seen this and use that as the jump interval
                cycle_difference = cycle - cycle_fingerprints[fingerprint]
                if cycle + cycle_difference <= max_cycle:
                    print(f"duplicate rock arrangement @ cycle {cycle} (last cycle @ {cycle_fingerprints[fingerprint]})...jumping to cycle {cycle + cycle_difference}")
                    cycle = cycle + cycle_difference
                cycle_fingerprints[fingerprint] = cycle

        return self._prb.load('N')
