from __future__ import annotations
from adventofcode.common import Solution
from functools import reduce


class WeirdExpression(object):
    def __init__(self, expression: str):
        self._expression = expression.split(" ")
        self._parts = []

        subexpression = []
        level = 0
        for e in self._expression:
            if e.startswith("("):
                # encountered start of a sub expression
                subexpression.append(e)
                level += e.count("(")
            elif e.endswith(")"):
                # encountered end of a sub expression
                subexpression.append(e)
                level -= e.count(")")

                if level == 0:
                    # this is the end of the sub expression at root expression
                    self._parts.append(WeirdExpression(" ".join(subexpression)[1:-1]))
                    subexpression = []
            else:
                if level > 0:
                    # currently at a sub expression so add it to the list of subexpression parts
                    subexpression.append(e)
                else:
                    # at root expression, so add it to parts list
                    if e in ("+", "*"):
                        self._parts.append(e)
                    else:
                        self._parts.append(int(e))

    def calculate(self) -> int:
        value = 0
        operation = None
        for p in self._parts:
            match p:
                case "+" | "*":
                    operation = p
                case int():
                    if operation:
                        value = (value + p) if operation == '+' else (value * p)
                    else:
                        value = p
                case WeirdExpression():
                    if operation:
                        value = (value + p.calculate()) if operation == '+' else (value * p.calculate())
                    else:
                        value = p.calculate()
                case _:
                    raise Exception(f"Invalid expression part : {p}")
        return value

    def advanced_calculate(self) -> int:
        multiplications = []

        value = 0
        for p in self._parts:
            match p:
                case "+":
                    continue
                case "*":
                    multiplications.append(value)
                    value = 0
                case int():
                    value += p
                case WeirdExpression():
                    value += p.advanced_calculate()
                case _:
                    raise Exception(f"Invalid expression part : {p}")
        multiplications.append(value)

        return reduce(lambda acc, e: acc * e, multiplications)


class Day18(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._input = self._load_input_as_lines()

    def part_one(self):
        total = 0
        for expression in self._input:
            we = WeirdExpression(expression)
            total += we.calculate()

        return total

    def part_two(self):
        total = 0
        for expression in self._input:
            we = WeirdExpression(expression)
            total += we.advanced_calculate()

        return total