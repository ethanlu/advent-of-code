from __future__ import annotations
from adventofcode.common import Solution
from typing import Dict, List, Tuple

import math


class Reaction(object):
    def __init__(self, requires: List[Tuple[str, int]], yields: Tuple[str, int]):
        self._requires = requires
        self._yields = yields

    @property
    def yields(self) -> Tuple[str, int]:
        return self._yields

    @property
    def requires(self) -> List[Tuple[str, int]]:
        return self._requires


class ChemicalGauge(object):
    def __init__(self, available: int):
        self._available = available
        self._used = 0

    @property
    def excess(self) -> int:
        return self._available - self._used

    def add(self, amount: int) -> ChemicalGauge:
        self._available += amount
        return self

    def use(self, amount: int) -> ChemicalGauge:
        self._used += amount
        return self


class NanoFactory(object):
    def __init__(self, reactions: List[Reaction]):
        self._reactions: Dict[str, Reaction] = {r.yields[0]: r for r in reactions}
        self._chemical_gauges: Dict[str, ChemicalGauge] = {chemical: ChemicalGauge(0) for chemical in self._reactions.keys()}
        self._ore_required = 0

    def _increment_reaction(self, chemical: str, amount: int):
        self._chemical_gauges[self._reactions[chemical].yields[0]].add(self._reactions[chemical].yields[1] * amount)

        for required_chemical, minimum_amount in self._reactions[chemical].requires:
            amount_needed = minimum_amount * amount
            if required_chemical == 'ORE':
                # needed chemical is a starting reaction, so increment ore requirements
                self._ore_required += amount_needed
            else:
                if self._chemical_gauges[required_chemical].excess >= amount_needed:
                    self._chemical_gauges[required_chemical].use(amount_needed)
                else:
                    # not enough excess of needed chemical is available...determine the amount of reactions needed to yield it and recurse before updating usage
                    self._increment_reaction(
                        required_chemical,
                        math.ceil((amount_needed - self._chemical_gauges[required_chemical].excess) / self._reactions[required_chemical].yields[1])
                    )
                    self._chemical_gauges[required_chemical].use(amount_needed)

    def calculate_ore(self, fuel_amount: int) -> int:
        self._increment_reaction('FUEL', fuel_amount)
        return self._ore_required


class Day14(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._reactions = []
        for line in self._load_input_as_lines():
            tmp = line.split(' => ')

            requirements = []
            for t in tmp[0].split(', '):
                ts = t.split(' ')
                requirements.append((ts[1], int(ts[0])))

            yields = tmp[1].split(' ')
            self._reactions.append(Reaction(requirements, (yields[1], int(yields[0]))))

    def part_one(self):
        nf = NanoFactory(self._reactions)
        return nf.calculate_ore(1)

    def part_two(self):
        available_ore = 1000000000000
        min_fuel = 1
        max_fuel = available_ore
        best_fuel = 1
        while True:
            nf = NanoFactory(self._reactions)
            potential_fuel = (max_fuel + min_fuel) // 2
            used_ore = nf.calculate_ore(potential_fuel)

            print(f"{potential_fuel} fuel needs {used_ore}/{available_ore} ore ---> ", end="")

            if used_ore < available_ore:
                min_fuel = potential_fuel
                print(f"increasing fuel range to {min_fuel} - {max_fuel}")
            if used_ore > available_ore:
                max_fuel = potential_fuel
                print(f"decreasing fuel range to {min_fuel} - {max_fuel}")

            if best_fuel == potential_fuel:
                break

            best_fuel = potential_fuel if min_fuel < max_fuel else best_fuel

        return best_fuel
    