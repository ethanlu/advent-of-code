from itertools import permutations
from solution import Solution

import re


class Day13(Solution):
    def _init(self):
        self.guests = set()
        self.happiness = {}

        # build set of guests and their paired happiness
        for l in self._load_input_as_lines():
            r = re.match(r'^(\w+) would (gain|lose) (\d+) happiness units by sitting next to (\w+)\.$', l)

            if r is None:
                raise Exception('invalid input : ' + l)

            guest1 = r.group(1)
            guest2 = r.group(4)
            happiness = int(r.group(3)) * (1 if r.group(2) == 'gain' else -1)

            self.guests.add(guest1)
            self.guests.add(guest2)

            self.happiness[(guest1 + '-' + guest2)] = happiness

    def _get_paired_happiness(self, guest1, guest2):
        if guest1 == 'You' or guest2 == 'You':
            return 0
        else:
            return self.happiness[(guest1 + '-' + guest2)] + self.happiness[(guest2 + '-' + guest1)]

    def _find_best_arrangement(self, seating_arrangements):
        # variation of traveling salesman problem - brute force method
        # generate permutation of every possible seating arrangement and sum the happiness of each pair (including the head and tail). highest sum is best arrangement
        best_happiness = 0
        for seating_arrangement in seating_arrangements:
            seating_happiness = 0
            guest1 = None
            for guest2 in seating_arrangement:
                if guest1:
                    seating_happiness += self._get_paired_happiness(guest1, guest2)

                guest1 = guest2

            # include happiness of head and tail of seating arrangement list
            seating_happiness += self._get_paired_happiness(seating_arrangement[0], seating_arrangement[-1])

            if best_happiness == 0 or best_happiness < seating_happiness:
                best_happiness = seating_happiness

            #print(str(seating_arrangement) + ' : ' + str(seating_happiness))

        return best_happiness

    def part_one(self):
        return self._find_best_arrangement(permutations(list(self.guests)))

    def part_two(self):
        return self._find_best_arrangement(permutations(list(self.guests) + ['You']))
