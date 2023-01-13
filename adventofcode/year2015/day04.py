from adventofcode.common import Solution

import hashlib


class Day04(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)

        self._key = self._load_input_as_string()

    def _mine(self, l):
        pattern = '0'*l
        i = 0
        while True:
            i += 1
            if hashlib.md5((self._key + str(i)).encode('utf-8')).hexdigest()[0:l] == pattern:
                break
        return i

    def part_one(self):
        return self._mine(5)

    def part_two(self):
        return self._mine(6)
