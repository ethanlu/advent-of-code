from argparse import ArgumentParser, ArgumentError
from adventofcode.common import Solution
from datetime import timedelta
from time import perf_counter_ns

import importlib
import re


class App(object):
    def __init__(self):
        self._solution = None

    def _lapsed_time(self, time_ns: int) -> str:
        delta = timedelta(microseconds=(time_ns // 1000))
        return "Elapsed : {h:02d}:{m:02d}:{s:02d}.{ms:03d}".format(h=delta.days*24, m=delta.seconds//60, s=delta.seconds%60, ms=delta.microseconds//1000)

    def run(self, year: str, day: str) -> None:
        if not re.match(r"\d\d\d\d", year):
            raise ArgumentError("year must be YYYY format")
        if not re.match(r"\d\d", day):
            raise ArgumentError("day must be DD format")

        solution_name = f"Day{day}"
        solution_path = f"adventofcode.year{year}.{solution_name.lower()}"
        module = importlib.import_module(solution_path)
        clss = getattr(module, solution_name)
        self._solution: Solution = clss(year, day)

        print('-----part one-----')
        s = perf_counter_ns()
        print(str(self._solution.part_one()))
        print(self._lapsed_time(perf_counter_ns() - s))

        print('-----part two-----')
        s = perf_counter_ns()
        print(str(self._solution.part_two()))
        print(self._lapsed_time(perf_counter_ns() - s))


def main():
    parser = ArgumentParser()
    parser.add_argument('year', type=str, help='year (YYYY)')
    parser.add_argument('day', type=str, help='day (DD)')
    args = parser.parse_args()

    year = args.year
    day = args.day

    app = App()
    app.run(year, day)


if __name__ == '__main__':
    main()
