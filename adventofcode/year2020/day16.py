from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.range import Interval
from typing import Dict, List

import re


class TicketField(object):
    def __init__(self, name: str, range1: Interval, range2: Interval):
        self._name = name
        self._range1 = range1
        self._range2 = range2

    @property
    def name(self) -> str:
        return self._name

    def validate(self, n: int) -> bool:
        return self._range1.contains(n) or self._range2.contains(n)


class Day16(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._fields: Dict[str, TicketField] = {}
        self._my_ticket: List[int] = []
        self._nearby_tickets: List[List[int]] = []

        regex = re.compile(r"^([a-z\s]+): (\d+)-(\d+) or (\d+)-(\d+)$")

        previous = None
        for line in self._load_input_as_lines():
            if line in ("", "your ticket:", "nearby tickets:"):
                previous = line
                continue
            else:
                if "," in line:
                    ticket = [int(n) for n in line.split(",")]
                    if previous == "your ticket:":
                        self._my_ticket = ticket
                    else:
                        self._nearby_tickets.append(ticket)
                else:
                    m = regex.match(line)
                    self._fields[m.groups()[0]] = TicketField(m.groups()[0], Interval(int(m.groups()[1]), int(m.groups()[2])), Interval(int(m.groups()[3]), int(m.groups()[4])))

    def part_one(self):
        error_rate = 0
        for ticket in self._nearby_tickets:
            for value in ticket:
                if sum([1 for f in self._fields.values() if f.validate(value)]) == 0:
                    error_rate += value

        return error_rate

    def part_two(self):
        valid_tickets = [self._my_ticket]
        for ticket in self._nearby_tickets:
            for value in ticket:
                if sum([1 for f in self._fields.values() if f.validate(value)]) == 0:
                    break
            else:
                valid_tickets.append(ticket)

        values = 1
        field_positions = []
        remaining_fields = set(self._fields.keys())
        remaining_positions = set(range(len(self._fields)))
        while len(remaining_positions) > 0:
            # out of remaining fields, only one of these fields can be at one position that is valid for all valid tickets
            for field in remaining_fields:
                valid_positions = []

                for candidate_order in remaining_positions:
                    for ticket in valid_tickets:
                        if not self._fields[field].validate(ticket[candidate_order]):
                            break
                    else:
                        valid_positions.append(candidate_order)

                if len(valid_positions) == 1:
                    print(f"field {field} can only be at position {valid_positions[0]}")

                    # this field can only be in one position for all valid tickets to be valid
                    field_positions.append(valid_positions[0])
                    remaining_fields.remove(field)
                    remaining_positions.remove(valid_positions[0])

                    if "departure" in field:
                        values *= self._my_ticket[valid_positions[0]]
                    break

        return values
