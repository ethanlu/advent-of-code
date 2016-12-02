from itertools import permutations

import re

class Day13(object):
    def __init__(self, input_file):
        self.guests = set()
        self.happiness = {}

        # build set of guests and their paired happiness
        with open(input_file) as f:
            for l in f.readlines():
                r = re.match('^(\w+) would (gain|lose) (\d+) happiness units by sitting next to (\w+)\.$', l)

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

            #print str(seating_arrangement) + ' : ' + str(seating_happiness)

        return best_happiness

    def part_one(self):
        return self._find_best_arrangement(permutations(list(self.guests)))

    def part_two(self):
        return self._find_best_arrangement(permutations(list(self.guests) + ['You']))


if __name__ == '__main__':
    p = Day13('../../input/2015/day13.txt')

    print '-----part one-----'
    print p.part_one()

    print '-----part two-----'
    print p.part_two()
