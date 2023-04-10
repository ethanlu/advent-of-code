from __future__ import annotations
from adventofcode.common import Solution

import re


class Day04(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._input = self._load_input_as_lines()

    def part_one(self):
        required = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid'}

        valid = 0
        provided = set([])
        for line in self._input:
            if line == "":
                missing = required - provided
                valid += 1 if len(required.intersection(provided)) == len(required) or (len(missing) == 1 and 'cid' in missing) else 0
                provided = set([])
            else:
                for d in line.split(' '):
                    provided.add(d.split(':')[0])
        missing = required - provided
        valid += 1 if len(required.intersection(provided)) == len(required) or (len(missing) == 1 and 'cid' in missing) else 0

        return valid

    def part_two(self):
        required = {
            'byr': lambda x: 1920 <= int(x) <= 2002,
            'iyr': lambda x: 2010 <= int(x) <= 2020,
            'eyr': lambda x: 2020 <= int(x) <= 2030,
            'hgt': lambda x: (150 <= int(x[0:-2]) <= 193 if x[-2:] == 'cm' else 59 <= int(x[0:-2]) <= 76) if x[-2:] in {'cm', 'in'} else False,
            'hcl': lambda x: re.match(r"^#[0-9a-f]{6}$", x),
            'ecl': lambda x: x in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'},
            'pid': lambda x: re.match(r"^\d{9}$", x)
        }

        valid = 0
        provided = {}
        for line in self._input:
            if line == "":
                for field, validate in required.items():
                    if field not in provided.keys() or not validate(provided[field]):
                        break
                else:
                    valid += 1
                provided = {}
            else:
                for d in line.split(' '):
                    p = d.split(':')
                    provided[p[0]] = p[1]
        for field, validate in required.items():
            if field not in provided.keys() or not validate(provided[field]):
                break
        else:
            valid += 1

        return valid
