from adventofcode.common import Solution
from itertools import permutations

import re


class Day09(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)

        # set of all cities
        self._cities = set()

        # distances between two cities as a city1-city2 and city2-city1 pair
        self._distances = {}

        # populate the set of cities and distances between each one as a lookup table
        for l in self._load_input_as_lines():
            r = re.match(r'^(.+) to (.+) = (\d+)$', l)

            if r is None:
                raise Exception('invalid input : ' + l)

            self._cities.add(r.group(1))
            self._cities.add(r.group(2))
            self._distances[r.group(1) + '-' + r.group(2)] = int(r.group(3))
            self._distances[r.group(2) + '-' + r.group(1)] = int(r.group(3))

    def _get_total_distance(self, path):
        distance = 0
        previous_city = ''
        for current_city in path:
            distance += self._distances[previous_city + '-' + current_city] if previous_city + '-' + current_city in self._distances else 0
            previous_city = current_city
        return distance

    def part_one(self):
        # generate permutation of every path through each city and sum their distances. return the smallest total distance
        shortest_path = 0
        for path in permutations(list(self._cities)):
            distance = self._get_total_distance(path)
            if shortest_path == 0 or shortest_path > distance:
                shortest_path = distance
            #print(str(path) + ' : ' + str(distance))

        return shortest_path

    def part_two(self):
        # generate permutation of every path through each city and sum their distances. return the longest total distance
        longest_path = 0
        for path in permutations(list(self._cities)):
            distance = self._get_total_distance(path)
            if longest_path < distance:
                longest_path = distance
            #print(str(path) + ' : ' + str(distance))

        return longest_path
