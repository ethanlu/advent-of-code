from adventofcode.common import Solution

import re


class Day19(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)

        self._transformations = []

        lines = self._load_input_as_lines()

        self._final_molecule = lines[-1]

        for t in lines[0:len(lines)-3]:
            tmp = t.split('=>')
            self._transformations.append((tmp[0].strip(), tmp[1].strip()))

    def _transform(self, molecule):
        possible_molecules = set()

        for source, destination in self._transformations:
            i = 0
            while i >= 0:
                i = molecule.find(source, i)

                if i >= 0:
                    possible_molecules.add(molecule[0:i] + molecule[i:i+len(source)].replace(source, destination) + molecule[i+len(source):])
                    i += 1

        return possible_molecules

    def _molecule_closeness(self,m1, m2):
        i = 0
        while i < min(len(m1), len(m2)):
            if m1[i] != m2[i]:
                break
            i += 1
        return i

    def part_one(self):
        return len(self._transform(self._final_molecule))

    def part_two(self):
        # don't think this solution will always find the "shortest" steps to ANY molecule. it just happens to reverse engineer the algorithm
        # the question used to generate the target molecule
        starting_molecule = 'e'
        target_molecule = self._final_molecule
        repl_r = {destination:source for source, destination in self._transformations}
        molecules = [target_molecule]
        while molecules[-1] != starting_molecule:
            molecules.append(re.sub('^(.*)(' + '|'.join(repl_r.keys()) + ')(.*?)$',
                                lambda x: x.group(1) + repl_r[x.group(2)] + x.group(3),
                                molecules[-1]))
        return len(molecules) - 1
