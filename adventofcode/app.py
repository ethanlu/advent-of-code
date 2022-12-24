from argparse import ArgumentParser, ArgumentError
from adventofcode import Solution

import importlib
import re


class App(object):
    def __init__(self):
        self._solution = None

    def run(self, year: str, day: str):
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
        print(str(self._solution.part_one()))

        print('-----part two-----')
        print(str(self._solution.part_two()))


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
