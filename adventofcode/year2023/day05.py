from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.range import Interval
from typing import Iterable, List


def paired(l: Iterable) -> Iterable:
    it = iter(l)
    return zip(it, it)


class CategoryMap(object):
    def __init__(self, destination: int, source: int, length: int):
        self._destination = Interval(destination, destination + length - 1)
        self._source = Interval(source, source + length - 1)
        self._length = length

    def contains(self, other: int) -> bool:
        return self._source.contains(other)

    def map(self, other: int) -> int:
        return self._destination.left + other - self._source.left

    def overlaps(self, other: Interval) -> bool:
        return self._source.overlaps(other)

    def interval_map(self, other: Interval) -> List[Interval]:
        destinations = []

        si = self._source.intersect(other)  # segment that intersects gets mapped
        destinations.append(Interval(self.map(si.left), self.map(si.right)))

        if other.left < si.left:    # left portion of input that did not intersect pass through
            destinations.append(Interval(other.left, si.left - 1))
        if other.right > si.right: # right portion of input thta did not intersect pass through
            destinations.append(Interval(si.right + 1, other.right))

        return destinations


class Almanac(object):
    MAP_SIZE = 7

    def __init__(self, seeds: List[int], map_matrix: List[List[CategoryMap], List[CategoryMap], List[CategoryMap], List[CategoryMap], List[CategoryMap], List[CategoryMap], List[CategoryMap]]):
        self._seeds = seeds
        self._category_matrix = map_matrix

    @property
    def seeds(self) -> List[int]:
        return self._seeds

    def location_for_seed(self, i: int) -> int:
        next_i = i
        for mi in range(Almanac.MAP_SIZE):
            for m in self._category_matrix[mi]:
                if m.contains(next_i):
                    next_i = m.map(next_i)
                    break
        return next_i

    def locations_for_seeds(self, i: Interval) -> List[Interval]:
        next_i = [i]
        for mi in range(Almanac.MAP_SIZE):
            for m in self._category_matrix[mi]:
                t = []
                for i in next_i:
                    if m.overlaps(i):
                        t += m.interval_map(i)
                if t:
                    next_i = t
                    break
        return next_i


class Day05(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        seeds = ""
        map_matrix = [[], [], [], [], [], [], []]

        matrix_index = -1
        for l in self._load_input_as_lines():
            if not l:       # skip empty lines
                continue

            if '-to-' in l: # change state when encountering a line label
                matrix_index += 1
                continue

            if matrix_index >= 0:
                map_matrix[matrix_index].append(CategoryMap(*(int(s) for s in l.split(' '))))
            else:
                seeds = l[6:].strip()

        self._almanac = Almanac([int(s) for s in seeds.split(' ')], map_matrix)

    def part_one(self):
        locations = []
        for s in self._almanac.seeds:
            location = self._almanac.location_for_seed(s)
            print(f"seed {s} goes to location {location}")
            locations.append(location)
        return min(locations)

    def part_two(self):
        all_locations = []
        for start, length in paired(self._almanac.seeds):
            si = Interval(start, start + length - 1)
            locations = self._almanac.locations_for_seeds(si)
            print(f"seeds {si} goes to locations {', '.join((str(location) for location in locations))}")
            all_locations += locations
        return (min(all_locations)).left
