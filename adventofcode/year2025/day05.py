from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.range import Interval
from functools import reduce


class Day05(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._fresh_ranges = []
        self._ingredients = []
        reading_ingredients = False
        for line in self._load_input_as_lines():
            if not line:
                reading_ingredients = True
                continue
            if reading_ingredients:
                self._ingredients.append(int(line))
            else:
                self._fresh_ranges.append(Interval(int(line.split('-')[0]), int(line.split('-')[1])))

    def part_one(self):
        fresh = []
        for ingredient in self._ingredients:
            for fresh_range in self._fresh_ranges:
                if fresh_range.contains(ingredient):
                    fresh.append(ingredient)
                    print(f"ingredient {ingredient} is fresh because it falls into range {fresh_range}")
                    break
            else:
                print(f"ingredient {ingredient} is spoiled")
        return len(fresh)

    def part_two(self):
        unique_ranges = []
        current = None
        for candidate in sorted(self._fresh_ranges):
            if not current:
                current = candidate
            else:
                if current.overlaps(candidate):
                    current = current.union(candidate)
                else:
                    unique_ranges.append(current)
                    current = candidate
        unique_ranges.append(current)
        for ur in unique_ranges:
            print(f"{ur} is a unique range")
        return reduce(lambda t, r: t + r.right - r.left + 1, unique_ranges, 0)