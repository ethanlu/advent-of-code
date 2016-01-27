from itertools import permutations

import re

input = ['Alice would gain 54 happiness units by sitting next to Bob.','Alice would lose 81 happiness units by sitting next to Carol.','Alice would lose 42 happiness units by sitting next to David.','Alice would gain 89 happiness units by sitting next to Eric.','Alice would lose 89 happiness units by sitting next to Frank.','Alice would gain 97 happiness units by sitting next to George.','Alice would lose 94 happiness units by sitting next to Mallory.','Bob would gain 3 happiness units by sitting next to Alice.','Bob would lose 70 happiness units by sitting next to Carol.','Bob would lose 31 happiness units by sitting next to David.','Bob would gain 72 happiness units by sitting next to Eric.','Bob would lose 25 happiness units by sitting next to Frank.','Bob would lose 95 happiness units by sitting next to George.','Bob would gain 11 happiness units by sitting next to Mallory.','Carol would lose 83 happiness units by sitting next to Alice.','Carol would gain 8 happiness units by sitting next to Bob.','Carol would gain 35 happiness units by sitting next to David.','Carol would gain 10 happiness units by sitting next to Eric.','Carol would gain 61 happiness units by sitting next to Frank.','Carol would gain 10 happiness units by sitting next to George.','Carol would gain 29 happiness units by sitting next to Mallory.','David would gain 67 happiness units by sitting next to Alice.','David would gain 25 happiness units by sitting next to Bob.','David would gain 48 happiness units by sitting next to Carol.','David would lose 65 happiness units by sitting next to Eric.','David would gain 8 happiness units by sitting next to Frank.','David would gain 84 happiness units by sitting next to George.','David would gain 9 happiness units by sitting next to Mallory.','Eric would lose 51 happiness units by sitting next to Alice.','Eric would lose 39 happiness units by sitting next to Bob.','Eric would gain 84 happiness units by sitting next to Carol.','Eric would lose 98 happiness units by sitting next to David.','Eric would lose 20 happiness units by sitting next to Frank.','Eric would lose 6 happiness units by sitting next to George.','Eric would gain 60 happiness units by sitting next to Mallory.','Frank would gain 51 happiness units by sitting next to Alice.','Frank would gain 79 happiness units by sitting next to Bob.','Frank would gain 88 happiness units by sitting next to Carol.','Frank would gain 33 happiness units by sitting next to David.','Frank would gain 43 happiness units by sitting next to Eric.','Frank would gain 77 happiness units by sitting next to George.','Frank would lose 3 happiness units by sitting next to Mallory.','George would lose 14 happiness units by sitting next to Alice.','George would lose 12 happiness units by sitting next to Bob.','George would lose 52 happiness units by sitting next to Carol.','George would gain 14 happiness units by sitting next to David.','George would lose 62 happiness units by sitting next to Eric.','George would lose 18 happiness units by sitting next to Frank.','George would lose 17 happiness units by sitting next to Mallory.','Mallory would lose 36 happiness units by sitting next to Alice.','Mallory would gain 76 happiness units by sitting next to Bob.','Mallory would lose 34 happiness units by sitting next to Carol.','Mallory would gain 37 happiness units by sitting next to David.','Mallory would gain 40 happiness units by sitting next to Eric.','Mallory would gain 18 happiness units by sitting next to Frank.','Mallory would gain 7 happiness units by sitting next to George.']

class Day13(object):
    def __init__(self, input):
        self.guests = set()
        self.happiness = {}

        # build set of guests and their paired happiness
        for i in input:
            r = re.match('^(\w+) would (gain|lose) (\d+) happiness units by sitting next to (\w+)\.$', i)

            if r is None:
                raise Exception('invalid input : ' + i)

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

            print str(seating_arrangement) + ' : ' + str(seating_happiness)

        return best_happiness

    def part_one(self):
        return self._find_best_arrangement(permutations(list(self.guests)))

    def part_two(self):
        return self._find_best_arrangement(permutations(list(self.guests) + ['You']))
