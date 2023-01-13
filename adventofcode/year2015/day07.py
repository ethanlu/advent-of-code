from collections import deque
from adventofcode.common import Solution

import re


class Day07(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)

        self._circuits = list(map(lambda l: self._parse_circuit(l), self._load_input_as_lines()))

        self._wires = {}
        self._overrides = {}

    def _reset(self):
        self._wires = {}
        self._overrides = {}

    def _parse_circuit(self, x):
        unitary = re.match(r"(NOT\s)?([a-z0-9]+) \-> ([a-z]+)", x)
        binary = re.match(r"([a-z0-9]+) (AND|OR|RSHIFT|LSHIFT) ([a-z0-9]+) \-> ([a-z]+)", x)

        if unitary:
            operator = '_assign' if unitary.group(1) is None else '_inverted_assign'
            wire = unitary.group(3)
            sources = (unitary.group(2),)
        elif binary:
            operator = '_' + binary.group(2).lower()
            wire = binary.group(4)
            sources = (binary.group(1), binary.group(3))
        else:
            raise Exception('invalid circuit : ' + x)

        # parse input wiring into tuple of an operation command, the target wire, and source values
        return operator, wire, sources

    def _value_of_sources(self, sources):
        values = []
        for s in sources:
            if re.match(r"^\d+$", s):
                # source is a constant signal
                values.append(int(s))
            elif s in self._wires:
                # source is a wire and it has a value
                if s in self._overrides:
                    # use override value if it exists
                    values.append(self._overrides[s])
                else:
                    values.append(self._wires[s])
            else:
                # source is a wire, but it is currently undefined
                raise Exception('wire undefined')

        return tuple(values)

    def _assign(self, wire, sources):
        self._wires[wire] = sources[0]

    def _inverted_assign(self, wire, sources):
        self._wires[wire] = ~sources[0]

    def _and(self, wire, sources):
        self._wires[wire] = sources[0] & sources[1]

    def _or(self, wire, sources):
        self._wires[wire] = sources[0] | sources[1]

    def _rshift(self, wire, sources):
        self._wires[wire] = sources[0] >> sources[1]

    def _lshift(self, wire, sources):
        self._wires[wire] = sources[0] << sources[1]

    def _run_circuit(self):
        # use queue to go through each wire and evaluate each circuit
        circuits = deque('')
        list(map(lambda c: circuits.append(c), self._circuits))
        while len(circuits) > 0:
            (operator, wire, sources) = circuits.popleft()

            try:
                getattr(self, operator)(wire, self._value_of_sources(sources))
            except Exception as e:
                circuits.append((operator, wire, sources))

    def part_one(self):
        self._reset()
        self._run_circuit()

        return self._wires['a']

    def part_two(self):
        # run the circuit to get value of wire a
        self._reset()
        self._run_circuit()
        value = self._wires['a']

        # reset the entire thing, but set the override and run the circuit again to get new wire a value
        self._reset()
        self._overrides['b'] = value
        self._run_circuit()

        # rerun circuits to get new wire a
        return self._wires['a']
