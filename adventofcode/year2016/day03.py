from itertools import chain, islice
from adventofcode import Solution

import re


class Day03(Solution):
    def _init(self):
        self._input = [(re.sub(' +', ' ', l)).strip().split(' ') for l in self._load_input_as_lines()]

    def _valid_triangle(self, l, w, h):
        return l + w > h and w + h > l and l + h > w

    def part_one(self):
        # O(n) time complexity (n is number of lines in input)
        # O(c) space complexity
        return len([1 for l, w, h in self._input if self._valid_triangle(int(l), int(w), int(h))])

    def part_two(self):
        # O(n) time complexity (n is length of movements in entire file)
        # O(c) space complexity
        def next_n(it, n):
            r = []
            for i, v in enumerate(it):
                r.append(v)
                if (i + 1) % n == 0:
                    yield r
                    r = []

        t = list(map(list, zip(*self._input)))
        return len([1 for l, w, h in next_n(list(chain(*t)), 3) if self._valid_triangle(int(l), int(w), int(h))])
