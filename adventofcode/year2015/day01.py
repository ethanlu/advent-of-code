from adventofcode.common import Solution


class Day01(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)

        self._input = self._load_input_as_string()

    def part_one(self):
        return self._input.count('(') - self._input.count(')')

    def part_two(self):
        floor = 0
        position = 0
        while floor >= 0:
            floor += 1 if self._input[position] == '(' else -1
            position += 1

        return position
