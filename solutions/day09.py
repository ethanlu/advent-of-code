from itertools import permutations

import re

input = ['Faerun to Norrath = 129','Faerun to Tristram = 58','Faerun to AlphaCentauri = 13','Faerun to Arbre = 24','Faerun to Snowdin = 60','Faerun to Tambi = 71','Faerun to Straylight = 67','Norrath to Tristram = 142','Norrath to AlphaCentauri = 15','Norrath to Arbre = 135','Norrath to Snowdin = 75','Norrath to Tambi = 82','Norrath to Straylight = 54','Tristram to AlphaCentauri = 118','Tristram to Arbre = 122','Tristram to Snowdin = 103','Tristram to Tambi = 49','Tristram to Straylight = 97','AlphaCentauri to Arbre = 116','AlphaCentauri to Snowdin = 12','AlphaCentauri to Tambi = 18','AlphaCentauri to Straylight = 91','Arbre to Snowdin = 129','Arbre to Tambi = 53','Arbre to Straylight = 40','Snowdin to Tambi = 15','Snowdin to Straylight = 99','Tambi to Straylight = 70']

class Day09(object):
    def __init__(self, input):
        self.cities = set()
        self.distances = {}

        # build set of cities and distances between each one as a lookup table
        for i in input:
            r = re.match('^(.+) to (.+) = (\d+)$', i)

            if r is None:
                raise Exception('invalid input : ' + i)

            source_city = r.group(1)
            destination_city = r.group(2)
            distance = int(r.group(3))

            self.cities.add(source_city)
            self.cities.add(destination_city)

            if source_city not in self.distances:
                self.distances[source_city] = {}

            self.distances[source_city][destination_city] = distance

    def _get_distance(self, city_one, city_two):
        if city_one in self.distances and city_two in self.distances[city_one]:
            return self.distances[city_one][city_two]
        else:
            return self.distances[city_two][city_one]

    def part_one(self):
        # traveling salesman - brute force method
        # generate permutation of every path through each city and sum their distances. the smallest total distance is the shortest path

        shortest_path = 0

        paths = permutations(list(self.cities))
        for path in paths:
            distance = 0
            previous_city = None
            for current_city in path:
                if previous_city:
                    distance += self._get_distance(previous_city, current_city)

                previous_city = current_city

            if shortest_path == 0 or shortest_path > distance:
                shortest_path = distance

            print str(path) + ' : ' + str(distance)

        return shortest_path

    def part_two(self):
        # traveling salesman - brute force method
        # generate permutation of every path through each city and sum their distances. the smallest total distance is the shortest path

        longest_path = 0

        paths = permutations(list(self.cities))
        for path in paths:
            distance = 0
            previous_city = None
            for current_city in path:
                if previous_city:
                    distance += self._get_distance(previous_city, current_city)

                previous_city = current_city

            if longest_path < distance:
                longest_path = distance

            print str(path) + ' : ' + str(distance)

        return longest_path
