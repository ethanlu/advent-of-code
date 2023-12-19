from __future__ import annotations
from abc import abstractmethod
from adventofcode.common import Solution
from adventofcode.common.range import Interval
from collections import deque
from functools import reduce
from typing import Dict, List, Tuple

import re


class Rule(object):
    def __init__(self, part: str, require: str, amount: int, on_pass: str):
        self._part = part
        self._require = require
        self._amount = amount
        self._on_pass = on_pass

    @property
    def on_pass(self) -> str:
        return self._on_pass

    @abstractmethod
    def consider(self, parts: Dict[str, int]) -> bool:
        raise Exception("not implemented")

    @abstractmethod
    def pass_range(self) -> Dict[str, Interval]:
        raise Exception("not implemented")

    @abstractmethod
    def fail_range(self) -> Dict[str, Interval]:
        raise Exception("not implemented")


class ConditionalRule(Rule):
    def __init__(self, part: str, require: str, amount: int, success: str):
        super().__init__(part, require, amount, success)

    def consider(self, parts: Dict[str, int]) -> bool:
        if self._part not in parts:
            return False
        match self._require:
            case '<':
                return parts[self._part] < self._amount
            case '>':
                return parts[self._part] > self._amount
            case _:
                raise Exception(f"Unexpected requirement : {self._require}")

    def pass_range(self) -> Dict[str, Interval]:
        return {self._part: Interval(1, self._amount - 1)} if self._require == '<' else {self._part: Interval(self._amount + 1, 4000)}

    def fail_range(self) -> Dict[str, Interval]:
        return {self._part: Interval(self._amount, 4000)} if self._require == '<' else {self._part: Interval(1, self._amount)}


class UnconditionalRule(Rule):
    def __init__(self, part: str, require: str, amount: int, success: str):
        super().__init__(part, require, amount, success)

    def consider(self, parts: Dict[str, int]) -> bool:
        return True

    def pass_range(self) -> Dict[str, Interval]:
        return {k: Interval(1, 4000) for k in ('x', 'm', 'a', 's')}

    def fail_range(self) -> Dict[str, Interval]:
        return {}


class Workflow(object):
    def __init__(self, rules: List[Rule]):
        self._rules = rules

    def consider(self, parts: Dict[str, int]) -> str:
        for rule in self._rules:
            if rule.consider(parts):
                return rule.on_pass

    def outcomes(self, parts: Dict[str, int]) -> List[Tuple[str, Dict[str, Interval]]]:
        def merge_part_ranges(p1: Dict[str: Interval], p2: Dict[str, Interval]) -> Dict[str, Interval]:
            return {k: p1[k].intersect(p2[k]) if k in p2 else p1[k] for k in p1.keys()}
        outcomes = []
        current_parts = parts
        for rule in self._rules:
            outcomes.append((rule.on_pass, merge_part_ranges(current_parts, rule.pass_range())))
            if issubclass(type(rule), ConditionalRule):
                current_parts = merge_part_ranges(current_parts, rule.fail_range())
        return outcomes


class Day19(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._workflows: Dict[str, Workflow] = {}
        self._part_sets: List[Dict[str, int]] = []
        self._part_ranges: List[Dict[str, int]] = []

        workflow_regex = re.compile(r"^(.*)\{(.*)}$")
        rule_regex = re.compile(r"^([a-z]+)([><])(\d+):(.*)$")

        read_workflow = True
        for l in self._load_input_as_lines():
            if not l:
                read_workflow = False
                continue
            if read_workflow:
                wm = workflow_regex.search(l)
                rules = []
                for r in wm.group(2).split(','):
                    rm = rule_regex.search(r)
                    if rm:
                        rules.append(ConditionalRule(rm.group(1), rm.group(2), int(rm.group(3)), rm.group(4)))
                    else:
                        rules.append(UnconditionalRule("", "", 0, r))
                self._workflows[wm.group(1)] = Workflow(rules)
            else:
                parts = {}
                for p in l[1:-1].split(','):
                    t = p.split('=')
                    parts[t[0]] = int(t[1])
                self._part_sets.append(parts)

    def part_one(self):
        accepted = 0
        for parts in self._part_sets:
            print(f"{parts}", end="")
            workflow = "in"
            while workflow not in ('A', 'R'):
                print(f" -> {workflow}", end="")
                workflow = self._workflows[workflow].consider(parts)
            print(f" -> {workflow}")
            accepted += sum(parts.values()) if workflow == 'A' else 0
        return accepted

    def part_two(self):
        accepted = 0
        remaining = deque([("in", {k: Interval(1, 4000) for k in ('x', 'm', 'a', 's')})])
        while len(remaining) > 0:
            workflow, parts = remaining.pop()
            match workflow:
                case 'R':   # stop search if possible workflow lead to rejection
                    continue
                case 'A':   # tally up the possible values if workflow lead to acceptance
                    accepted += reduce(lambda x, y: x * y, ((i.right - i.left + 1) for i in parts.values()))
                case _:     # get possibilities from workflow and add them to pool
                    for (out_workflow, out_parts) in self._workflows[workflow].outcomes(parts):
                        remaining.append((out_workflow, out_parts))
        return accepted
