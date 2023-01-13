from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.graph.search import AStar, SearchPath, SearchState
from copy import copy
from functools import reduce
from itertools import combinations
from typing import Iterable, List, Tuple

import re


class Isotopes(object):
    def __init__(self, isotopes: List[str]):
        self._isotopes = sorted(isotopes)
        self._bitmap = {isotope: 2 ** index for index, isotope in enumerate(self._isotopes)}

    @property
    def ids(self):
        return self._isotopes

    def get_bit(self, isotope: str) -> int:
        return self._bitmap[isotope]


class Floor(object):
    def __init__(self, isotopes: Isotopes, chips: List[str], rtgs: List[str]):
        self._isotopes = isotopes
        self._chips = reduce(lambda a, b: a | b, [self._isotopes.get_bit(chip) for chip in chips], 0)
        self._rtgs = reduce(lambda a, b: a | b, [self._isotopes.get_bit(rtg) for rtg in rtgs], 0)
        self._chips_count = len(chips)
        self._rtgs_count = len(rtgs)

    def __copy__(self):
        cls = self.__class__
        clone = cls.__new__(cls)
        clone._chips = self._chips
        clone._rtgs = self._rtgs
        clone._chips_count = self._chips_count
        clone._rtgs_count = self._rtgs_count
        clone._isotopes = self._isotopes
        return clone

    @property
    def chips_hash(self):
        return self._chips

    @property
    def rtgs_hash(self):
        return self._rtgs

    @property
    def chips_count(self):
        return self._chips_count

    @property
    def rtgs_count(self):
        return self._rtgs_count

    def add_chip(self, isotope: str) -> Floor:
        self._chips |= self._isotopes.get_bit(isotope)
        self._chips_count += 1
        return self

    def remove_chip(self, isotope: str) -> Floor:
        self._chips &= ~self._isotopes.get_bit(isotope)
        self._chips_count -= 1
        return self

    def add_rtg(self, isotope: str) -> Floor:
        self._rtgs |= self._isotopes.get_bit(isotope)
        self._rtgs_count += 1
        return self

    def remove_rtg(self, isotope: str) -> Floor:
        self._rtgs &= ~self._isotopes.get_bit(isotope)
        self._rtgs_count -= 1
        return self

    def has_chip(self, isotope: str) -> bool:
        return self._chips & self._isotopes.get_bit(isotope) != 0

    def has_rtg(self, isotope: str) -> bool:
        return self._rtgs & self._isotopes.get_bit(isotope) != 0

    def can_add_items(self, chips: Iterable[str], rtgs: Iterable[str]):
        resultant_chips = reduce(lambda a, b: a | b, [self._isotopes.get_bit(chip) for chip in chips], self._chips)
        resultant_rtgs = reduce(lambda a, b: a | b, [self._isotopes.get_bit(rtg) for rtg in rtgs], self._rtgs)

        # can add items only if the resulting number of chips are at least paired with their rtg counterpart
        return resultant_rtgs == 0 or resultant_chips & resultant_rtgs == resultant_chips

    def can_remove_items(self, chips: Iterable[str], rtgs: Iterable[str]):
        resultant_chips = reduce(lambda a, b: a & ~b, [self._isotopes.get_bit(chip) for chip in chips], self._chips)
        resultant_rtgs = reduce(lambda a, b: a & ~b, [self._isotopes.get_bit(rtg) for rtg in rtgs], self._rtgs)

        # can remove items only if the resulting number of chips are at least paired with their rtg counterpart
        return resultant_rtgs == 0 or resultant_chips & resultant_rtgs == resultant_chips


class StepSearchState(SearchState):
    def __init__(self, isotopes: Isotopes, floors: List[Floor], current_floor: int, gain: int, cost: int, max_cost: int):
        self._isotopes = isotopes
        self._floors: List[Floor] = floors
        self._current_floor: int = current_floor
        super().__init__(self._hash(), gain, cost, max_cost)

    @property
    def floors(self):
        return self._floors

    @property
    def potential_gain(self) -> int:
        # number of chips and generators remaining on first, second, and third floor with floors further away from 4th counting less
        return (self._floors[0].chips_count + self._floors[0].rtgs_count) * 2 + \
               (self._floors[1].chips_count + self._floors[1].rtgs_count) * 4 + \
               (self._floors[2].chips_count + self._floors[2].rtgs_count) * 8

    def _hash(self) -> str:
        return str(self._current_floor) + ":" + ":".join(["{chip:05b}-{rtg:05b}".format(chip=floor.chips_hash, rtg=floor.rtgs_hash) for floor in self._floors])

    def next_search_states(self, previous_search_state: SearchState) -> List[SearchState]:
        next_states = []

        # possible floors to move to based on current floor
        next_floors = []
        match self._current_floor:
            case 0:
                next_floors.append(1)
            case 1:
                next_floors.append(0)
                next_floors.append(2)
            case 2:
                next_floors.append(1)
                next_floors.append(3)
            case 3:
                next_floors.append(2)
            case _:
                raise Exception(f"Invalid current floor : {self._current_floor}")

        # possible chip and generator combinations that can be moved from current floor
        valid_moves = []
        for next_floor in next_floors:
            # move only single chip and single rtg
            for isotope in self._isotopes.ids:
                if self._floors[self._current_floor].has_chip(isotope) and self._floors[self._current_floor].can_remove_items([isotope], []) and self._floors[next_floor].can_add_items([isotope], []):
                    valid_moves.append((next_floor, (isotope, ), ()))
                if self._floors[self._current_floor].has_rtg(isotope) and self._floors[self._current_floor].can_remove_items([], [isotope]) and self._floors[next_floor].can_add_items([], [isotope]):
                    valid_moves.append((next_floor, (), (isotope, )))
            # move two chips or two rtgs
            for isotopes in combinations(self._isotopes.ids, 2):
                if self._floors[self._current_floor].has_chip(isotopes[0]) and self._floors[self._current_floor].has_chip(isotopes[1]) and \
                        self._floors[self._current_floor].can_remove_items(isotopes, ()) and self._floors[next_floor].can_add_items(isotopes, ()):
                    valid_moves.append((next_floor, isotopes, ()))
                if self._floors[self._current_floor].has_rtg(isotopes[0]) and self._floors[self._current_floor].has_rtg(isotopes[1]) and \
                        self._floors[self._current_floor].can_remove_items((), isotopes) and self._floors[next_floor].can_add_items((), isotopes):
                    valid_moves.append((next_floor, (), isotopes))
            # move a chip-generator pair
            for isotope in self._isotopes.ids:
                if self._floors[self._current_floor].has_chip(isotope) and self._floors[self._current_floor].has_rtg(isotope) and \
                        self._floors[self._current_floor].can_remove_items((isotope, ), (isotope, )) and self._floors[next_floor].can_add_items((isotope, ), (isotope, )):
                    valid_moves.append((next_floor, (isotope, ), (isotope, )))

        for (next_floor, chips, rtgs) in valid_moves:
            floors = [copy(floor) for floor in self.floors]
            for chip in chips:
                floors[next_floor].add_chip(chip)
                floors[self._current_floor].remove_chip(chip)
            for rtg in rtgs:
                floors[next_floor].add_rtg(rtg)
                floors[self._current_floor].remove_rtg(rtg)

            next_states.append(StepSearchState(self._isotopes, floors, next_floor, self.gain, self.cost + 1, self.max_cost))

        return next_states


class Day11(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)

        self._rtg_regex = re.compile(r"(\w+) generator")
        self._chip_regex = re.compile(r"(\w+)-compatible")

    def _build_isotope(self, starting_ids: List = ()) -> Isotopes:
        ids = list(starting_ids)
        for line in self._load_input_as_lines():
            ids += self._rtg_regex.findall(line)
            ids += self._chip_regex.findall(line)
        return Isotopes(list(set(ids)))

    def _build_floors(self, isotopes: Isotopes) -> Tuple[List[Floor], List[Floor]]:
        start_floors = []
        for line in self._load_input_as_lines():
            rtgs = self._rtg_regex.findall(line)
            chips = self._chip_regex.findall(line)
            start_floors.append(Floor(isotopes, chips, rtgs))

        end_floors = [Floor(isotopes, isotopes.ids, isotopes.ids) if i == len(start_floors) - 1 else Floor(isotopes, [], []) for i, floor in enumerate(start_floors)]

        return start_floors, end_floors

    def part_one(self):
        isotopes = self._build_isotope()
        start_floors, end_floors = self._build_floors(isotopes)

        start_state = StepSearchState(isotopes, start_floors, 0, 0, 0, 99999)
        end_state = StepSearchState(isotopes, end_floors, 3, 0, 0, 99999)

        astar = AStar(SearchPath(start_state), end_state)
        astar.verbose(True, 5000)

        shortest = astar.find_path()
        print(f"{shortest}")

        return shortest.cost

    def part_two(self):
        isotopes = self._build_isotope(['elerium', 'dilithium'])
        start_floors, end_floors = self._build_floors(isotopes)
        start_floors[0].add_chip('elerium')
        start_floors[0].add_rtg('elerium')
        start_floors[0].add_chip('dilithium')
        start_floors[0].add_rtg('dilithium')

        start_state = StepSearchState(isotopes, start_floors, 0, 0, 0, 99999)
        end_state = StepSearchState(isotopes, end_floors, 3, 0, 0, 99999)

        astar = AStar(SearchPath(start_state), end_state)
        astar.verbose(True, 50000)

        shortest = astar.find_path()
        print(f"{shortest}")

        return shortest.cost
