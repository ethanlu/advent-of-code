from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.grid import Point2D
from typing import Dict, List


deltas = (
    Point2D(-1, -1), Point2D(0, -1), Point2D(1, -1),
    Point2D(-1, 0), Point2D(1, 0),
    Point2D(-1, 1), Point2D(0, 1), Point2D(1, 1)
)


class SeatSystem(object):
    def __init__(self, seats: List[str]):
        self._seats: Dict[Point2D, str] = {}

        for y, line in enumerate(seats):
            for x, seat in enumerate(line):
                p = Point2D(x, y)
                self._seats[p] = seat

    @property
    def occupied(self) -> int:
        return sum((1 for seat in self._seats.values() if seat == '#'))

    def simulate_adjacent_seat(self) -> None:
        last_occupied = None
        while self.occupied != last_occupied:
            last_occupied = self.occupied

            next_seats = {}
            for position, seat in self._seats.items():
                if seat == '.':
                    next_seats[position] = seat
                    continue

                adjacent_occupied = 0

                for delta in deltas:
                    neighbor = position + delta
                    adjacent_occupied += 1 if neighbor in self._seats and self._seats[neighbor] == '#' else 0

                match seat:
                    case 'L':
                        next_seats[position] = '#' if adjacent_occupied == 0 else 'L'
                    case '#':
                        next_seats[position] = 'L' if adjacent_occupied >= 4 else '#'
                    case _:
                        raise Exception(f"Invalid seat ({seat}) at position {position}")

            self._seats = next_seats

    def simulate_visible_seat(self):
        last_occupied = None
        while self.occupied != last_occupied:
            last_occupied = self.occupied

            next_seats = {}
            for position, seat in self._seats.items():
                if seat == '.':
                    next_seats[position] = seat
                    continue

                adjacent_occupied = 0

                for delta in deltas:
                    neighbor = position + delta
                    while neighbor in self._seats and self._seats[neighbor] == '.':
                        neighbor += delta
                    adjacent_occupied += 1 if neighbor in self._seats and self._seats[neighbor] == '#' else 0

                match seat:
                    case 'L':
                        next_seats[position] = '#' if adjacent_occupied == 0 else 'L'
                    case '#':
                        next_seats[position] = 'L' if adjacent_occupied >= 5 else '#'
                    case '.':
                        next_seats[position] = seat
                    case _:
                        raise Exception(f"Invalid seat ({seat}) at position {position}")

            self._seats = next_seats


class Day11(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._input = self._load_input_as_lines()

    def part_one(self):
        ss = SeatSystem(self._input)
        ss.simulate_adjacent_seat()
        return ss.occupied

    def part_two(self):
        ss = SeatSystem(self._input)
        ss.simulate_visible_seat()
        return ss.occupied
