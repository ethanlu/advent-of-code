from __future__ import annotations
from adventofcode.common import Solution


def largest_joltage(battery_bank: str, num_batteries: int) -> str:
    joltage = []
    largest_index = 0
    max_index = len(battery_bank) - num_batteries
    for b in range(num_batteries):
        largest = '0'
        i = largest_index
        while i <= max_index:
            if battery_bank[i] > largest:
                largest = battery_bank[i]
                largest_index = i
            i += 1
        joltage.append(largest)
        max_index += 1
        largest_index += 1
    return "".join(joltage)


class Day03(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._input = self._load_input_as_lines()

    def part_one(self):
        count = 0
        for battery_bank in self._input:
            joltage = largest_joltage(battery_bank, 2)
            print(f"{battery_bank} -> {joltage}")
            count += int(joltage)
        return count

    def part_two(self):
        count = 0
        for battery_bank in self._input:
            joltage = largest_joltage(battery_bank, 12)
            print(f"{battery_bank} -> {joltage}")
            count += int(joltage)
        return count
