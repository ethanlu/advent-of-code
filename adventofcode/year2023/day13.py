from __future__ import annotations
from adventofcode.common import Solution
from collections import Counter
from functools import reduce
from typing import Iterable, List, Set, Tuple

class TerrainPattern(object):
    def __init__(self, s: str):
        self._pattern = s
        self._reflection_points = set([])

        # manacher's algo from https://en.wikipedia.org/wiki/Longest_palindromic_substring
        ss = "|".join(list(s))
        max_len = len(ss)
        radii = [0] * len(ss)

        center = 0
        radius = 0
        while center < max_len:
            while center < max_len and (center + radius + 1) < max_len and ss[(center - radius - 1)] == ss[(center + radius + 1)]:
                radius += 1
            radii[center] = radius

            previous_center = center
            previous_radius = radius
            center += 1
            radius = 0
            while center <= (previous_center + previous_radius):
                mirrored_center = previous_center * 2 - center
                max_mirrored_radius = previous_center + previous_radius - center

                if radii[mirrored_center] < max_mirrored_radius:
                    radii[center] = radii[mirrored_center]
                    center += 1
                    continue

                if radii[mirrored_center] > max_mirrored_radius:
                    radii[center] = max_mirrored_radius
                    center += 1
                    continue

                radius = max_mirrored_radius
                break

        for c, r in enumerate(radii):
            if r >= 1 and ss[c] == '|' and ((c - r) == 0 or (c + r ) == (len(ss) - 1)):
                self._reflection_points.add(c // 2)

    @property
    def pattern(self) -> str:
        return self._pattern

    @property
    def reflection_points(self) -> Set[int]:
        return self._reflection_points

class Terrain(object):
    def __init__(self, data: List[str]):
        self._horizontals = [TerrainPattern(d) for d in data]
        self._verticals = []
        for column in range(len(data[0])):
            s = []
            for row in range(len(data)):
                s.append(data[row][column])
            self._verticals.append(TerrainPattern("".join(s)))

    @property
    def horizontals(self) -> List[TerrainPattern]:
        return self._horizontals

    @property
    def verticals(self) -> List[TerrainPattern]:
        return self._verticals

    def _perfect_reflection_line_index(self, data: Iterable[Set[int]]) -> int:
        perfects = reduce(lambda x, y: x.intersection(y), data)
        if len(perfects) > 1:
            raise Exception(f"More than 1 perfect reflection line found!")
        return list(perfects)[0] if len(perfects) else -1

    def _imperfect_reflection_line_index(self, data: Iterable[Set[int]]) -> int:
        tally = Counter()
        data_length = 0
        for reflection_points in data:
            data_length += 1
            for i in reflection_points:
                tally[i] += 1
        imperfect = -1
        for t in tally.most_common(2):
            if t[1] == (data_length - 1):
                imperfect = t[0]
                break
        return imperfect

    def perfect_vertical_reflection_line_index(self) -> int:
        return self._perfect_reflection_line_index((h.reflection_points for h in self._horizontals))

    def perfect_horizontal_reflection_line_index(self) -> int:
        return self._perfect_reflection_line_index((h.reflection_points for h in self._verticals))

    def imperfect_vertical_reflection_line_index(self) -> int:
        return self._imperfect_reflection_line_index((h.reflection_points for h in self._horizontals))

    def imperfect_horizontal_reflection_line_index(self) -> int:
        return self._imperfect_reflection_line_index((h.reflection_points for h in self._verticals))


class Day13(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._terrains = []
        data = []
        for l in self._load_input_as_lines():
            if not l:
                self._terrains.append(Terrain(data))
                data = []
            else:
                data.append(l)
        self._terrains.append(Terrain(data))

    def part_one(self):
        total = 0
        for i, t in enumerate(self._terrains):
            pr_index = t.perfect_vertical_reflection_line_index()
            if pr_index >= 0:
                column = pr_index + 1
                print(f"terrain {i} has a perfect vertical reflection line at column {column}")
                total += column

            pr_index = t.perfect_horizontal_reflection_line_index()
            if pr_index >= 0:
                row = pr_index + 1
                print(f"terrain {i} has a perfect horizontal reflection line at row {row}")
                total += row * 100
        return total

    def part_two(self):
        total = 0
        for i, t in enumerate(self._terrains):
            pr_index = t.imperfect_vertical_reflection_line_index()
            if pr_index >= 0:
                column = pr_index + 1
                print(f"terrain {i} has an imperfect vertical reflection line at column {column}")
                total += column

            pr_index = t.imperfect_horizontal_reflection_line_index()
            if pr_index >= 0:
                row = pr_index + 1
                print(f"terrain {i} has an imperfect horizontal reflection line at row {row}")
                total += row * 100
        return total
