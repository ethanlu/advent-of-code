from __future__ import annotations
from adventofcode.common import Solution
from functools import cache, lru_cache
from itertools import product
from typing import Dict, List, Union


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
        self._rules_length: Dict[int, int] = {}

        for r in rules:
            tmp = r.split(": ")
            self._rules[int(tmp[0])] = RegularExpressionRule(tmp[1])

        for i in self._rules.keys():
            self._rules_length[i] = len(self._fetch(i)[0])

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
        if len(s) != self._rules_length[0]:     # optimization to fail immediately if the length of s does not match the length of the rule #0 before resorting to string matching all possibilities
            return False

        for pattern in self._fetch(0):
            if s == pattern:
                return True
        else:
            return False


class RegularExpressionWithLoop(RegularExpression):
    def __init__(self, rules: List[str]):
        super().__init__(rules)

    def exact_match(self, s: str) -> bool:
        # - only rule 0 uses rule 8 and 11
        # - the modifications to rule 8 and 11 allow rule 42 to repeat in the beginning and rule 31 to repeat at the end
        # - the regex pattern is basically ({rule-42})+({rule-42}){n,}({rule-31}){n,}
        # - the number of times rule 42 matches must be greater than number of times rule 31 matches
        # - only need to run this modified match against inputs that failed the non-looping rule
        if super().exact_match(s):
            return True
        else:
            rule42 = 0
            rule31 = 0
            # must match rule 42 at least twice
            for _ in range(2):
                if len(s) < self._rules_length[42]:
                    return False
                for pattern in self._fetch(42):
                    if s[:self._rules_length[42]] == pattern:
                        break
                else:
                    return False
                s = s[self._rules_length[42]:]
                rule42 += 1

            # then can match rule 42 any number of times
            while True:
                if len(s) < self._rules_length[42]:
                    break
                for pattern in self._fetch(42):
                    if s[:self._rules_length[42]] == pattern:
                        break
                else:
                    break
                s = s[self._rules_length[42]:]
                rule42 += 1

            # then must match rule 31 once
            for _ in range(1):
                if len(s) < self._rules_length[31]:
                    return False
                for pattern in self._fetch(31):
                    if s[:self._rules_length[31]] == pattern:
                        break
                else:
                    return False
                s = s[self._rules_length[31]:]
                rule31 += 1

            # finally can match rule 31 any number of times
            while True:
                if len(s) < self._rules_length[31]:
                    break
                for pattern in self._fetch(31):
                    if s[:self._rules_length[31]] == pattern:
                        break
                else:
                    break
                s = s[self._rules_length[42]:]
                rule31 += 1

            # string is exact match if remaining is 0
            return len(s) == 0 and rule42 > rule31


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
        re = RegularExpression(self._rules)
        return sum(1 for t in self._tests if re.exact_match(t))

    def part_two(self):
        re = RegularExpressionWithLoop(self._rules)
        return sum(1 for t in self._tests if re.exact_match(t))
