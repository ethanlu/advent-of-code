from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.grid import Point3D
from functools import reduce
from itertools import combinations, islice
from typing import List, Set


def take(n, iterable):
    # https://docs.python.org/3.11/library/itertools.html#itertools-recipes
    return list(islice(iterable, n))


def distance(p1: Point3D, p2: Point3D) -> int:
    return abs(p1.x - p2.x)**2 + abs(p1.y - p2.y)**2 + abs(p1.z - p2.z)**2


def combine(circuits: List[Set[Point3D]]) -> List[Set[Point3D]]:
    combined = []
    for candidate in circuits:
        merged = False
        for existing in combined:
            if existing.intersection(candidate):
                merged = True
                existing.update(candidate)
        if not merged:
            combined.append(candidate)
    return combined


class Day08(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._junction_boxes = set([])
        for line in self._load_input_as_lines():
            t = line.split(',')
            self._junction_boxes.add(Point3D(int(t[0]), int(t[1]), int(t[2])))
        self._pairs = sorted([(p1, p2) for p1, p2 in combinations(self._junction_boxes, 2)], key=lambda pair: distance(pair[0], pair[1]))

    def part_one(self):
        current = [{p1, p2} for p1, p2 in take(1000, self._pairs)]
        while True:
            next_current = combine(current)
            if len(next_current) != len(current):
                current = next_current
            else:
                break
        circuits = reversed(sorted(next_current, key=lambda circuit: len(circuit)))
        return reduce(lambda t, c: t * len(c), take(3, circuits), 1)

    def part_two(self):
        starting_pairs = []
        output_threshold = 1
        for p1, p2 in self._pairs:
            starting_pairs.append({p1, p2})
            if len(starting_pairs) == output_threshold:
                output_threshold *= 2
                print(f"searching using {len(starting_pairs)} pairs")

            current = starting_pairs
            while True:
                next_current = combine(current)
                if len(next_current) != len(current):
                    current = next_current
                else:
                    break
            if len(next_current) == 1 and len(next_current[0]) == len(self._junction_boxes):
                target_pair = (p1, p2)
                print(f"using {len(starting_pairs)} pairs forms a completed circuit with pair : {p1} and {p2}")
                break
        else:
            raise Exception('exhausted all possible pairs')
        return target_pair[0].x * target_pair[1].x
