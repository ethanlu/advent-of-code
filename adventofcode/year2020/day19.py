from __future__ import annotations
from adventofcode.common import Solution
from functools import cache
from itertools import product
from typing import Dict, List, Set, Union


class RegularExpressionRule(object):
    def __init__(self, s: str):
        self._rules = []

        if '"' in s:        # is a character
            self._rules.append(s.strip('"'))
        else:               # is reference to other rule(s)
            if "|" in s:    # is a piped reference
                for ss in s.split(" | "):
                    self._rules.append([int(r) for r in ss.split(" ")])
            else:           # is sequence of references
                self._rules.append([int(r) for r in s.split(" ")])

    @property
    def rules(self) -> Union[str, int, List[int], List[List[int]]]:
        return self._rules


class RegularExpression(object):
    def __init__(self, rules: List[str]):
        self._rules: Dict[int, RegularExpressionRule] = {}

        for r in rules:
            tmp = r.split(": ")
            self._rules[int(tmp[0])] = RegularExpressionRule(tmp[1])

    @cache
    def _fetch(self, r: int) -> List[str]:
        match len(self._rules[r].rules), self._rules[r].rules[0]:
            case 1, str():
                return [self._rules[r].rules[0]]
            case 1, list():
                seqrules = [self._fetch(seqrule) for seqrule in self._rules[r].rules[0]]
                return ["".join(r) for r in product(*seqrules)]
            case _, list():
                subrules = []
                for subrule in self._rules[r].rules:
                    seqrules = [self._fetch(seqrule) for seqrule in subrule]
                    subrules = subrules + ["".join(r) for r in product(*seqrules)]
                return subrules
            case _:
                raise Exception(f"Invalid rule type : {self._rules[r].rules}")

    def exact_match(self, s: str) -> bool:
        for rule in self._fetch(0):
            if s == rule:
                return True
        else:
            return False


class Day19(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._rules = []
        self._tests = []

        rules = True
        for line in self._load_input_as_lines():
            if line:
                if rules:
                    self._rules.append(line)
                else:
                    self._tests.append(line)
            else:
                rules = False

    def part_one(self):
        r = RegularExpression(self._rules)
        return sum(1 for t in self._tests if r.exact_match(t))

    def part_two(self):
        return ""
        self._rules[8] = "42 | 42 8"
        self._rules[11] = "42 31 | 42 11 31"

        r = RegularExpression(self._rules)
        return sum(1 for t in self._tests if r.exact_match(t))
