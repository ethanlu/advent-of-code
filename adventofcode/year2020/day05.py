from __future__ import annotations
from adventofcode.common import Solution


def binary_space_partition(s: str) -> int:
    a = 0
    b = pow(2, len(s)) - 1
    for c in s:
        match c:
            case 'F' | 'L':
                b = b - (b - a) // 2 - 1
            case 'B' | 'R':
                a = a + (b - a) // 2 + 1
            case _:
                raise Exception(f"Unexpected value : {c}")
    return a


class Day05(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._input = self._load_input_as_lines()

    def part_one(self):
        highest_seat_id = 0
        for boarding_pass in self._input:
            row = binary_space_partition(boarding_pass[0:7])
            col = binary_space_partition(boarding_pass[-3:])
            seat_id = row * 8 + col
            if seat_id > highest_seat_id:
                highest_seat_id = seat_id

        return highest_seat_id

    def part_two(self):
        seats = []
        for boarding_pass in self._input:
            row = binary_space_partition(boarding_pass[0:7])
            col = binary_space_partition(boarding_pass[-3:])
            seats.append(row * 8 + col)
        seats = sorted(seats)

        seat = 0
        for i in range(1, len(seats)):
            if seats[i] - seats[i - 1] != 1:
                seat = (seats[i] + seats[i - 1]) // 2
                break

        return seat
