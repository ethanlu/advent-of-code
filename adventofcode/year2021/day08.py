from __future__ import annotations
from adventofcode.common import Solution
from functools import reduce
from typing import List, Set


seven_segment_layout = {
    '0': ('a', 'b', 'c', 'e', 'f', 'g'),
    '1': ('c', 'f'),
    '2': ('a', 'c', 'd', 'e', 'g'),
    '3': ('a', 'c', 'd', 'f', 'g'),
    '4': ('b', 'c', 'd', 'f'),
    '5': ('a', 'b', 'd', 'f', 'g'),
    '6': ('a', 'b','d', 'e', 'f', 'g'),
    '7': ('a', 'c', 'f'),
    '8': ('a', 'b', 'c', 'd', 'e', 'f', 'g'),
    '9': ('a', 'b', 'c', 'd', 'f', 'g')
}


class SevenSegmentDisplay(object):
    def __init__(self, data: str):
        t = data.split(' | ')
        self._outputs = [set(list(o)) for o in t[1].split(' ')]

        # segment maps can be deduced from the unique segments that form 1, 4, 7, 8 and set operations
        one, seven, four, eight, fives, sixes = set(), set(), set(), set(), [], []
        for s in t[0].split(' '):
            match len(s):
                case 2:
                    one = set(list(s))
                case 3:
                    seven = set(list(s))
                case 4:
                    four = set(list(s))
                case 7:
                    eight = set(list(s))
                case 5: # segments used to make 2, 3, 5
                    fives.append(set(list(s)))
                case 6: # segments used to make 0, 6, 9
                    sixes.append(set(list(s)))
                case _:
                    raise Exception(f"unexpected segment {s} in {data}")
        self._segment_map = {
            'a': seven - one,
            'd': reduce(lambda t, c: t.intersection(c), fives).intersection(four),
            'f': reduce(lambda t, c: t.intersection(c), sixes).intersection(one),
            'g': reduce(lambda t, c: t.intersection(c), fives) - seven - four
        }
        self._segment_map['b'] = four - one - self._segment_map['d']
        self._segment_map['c'] = one - self._segment_map['f']
        self._segment_map['e'] = eight - four - self._segment_map['a'] - self._segment_map['g']

        # map digit to mapped segments
        self._digit_map = {}
        for digit, segments in seven_segment_layout.items():
            self._digit_map[digit] = reduce(lambda t, s: t.union(s), [self._segment_map[segment] for segment in segments])

    @property
    def output_segments(self) -> List[Set[str]]:
        return self._outputs

    @property
    def output_number(self) -> int:
        number = []
        for output_segments in self._outputs:
            for digit, mapped_segments in self._digit_map.items():
                if output_segments == mapped_segments:
                    number.append(digit)
                    break
            else:
                raise Exception(f"unexpected not found digit with {self._outputs}")
        return int(''.join(number))


class Day08(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._displays = [SevenSegmentDisplay(line) for line in self._load_input_as_lines()]

    def part_one(self):
        total = 0
        for display in self._displays:
            total += sum((1 for n in display.output_segments if len(n) in (2, 3, 4, 7)))
        return total

    def part_two(self):
        total = 0
        for display in self._displays:
            total += display.output_number
        return total
