from __future__ import annotations
from adventofcode.common import Solution
from itertools import accumulate, chain, cycle, repeat
from typing import List


class FlawedFrequencyTransmission(object):
    def __init__(self, signal: List[int], size: int):
        self._signal_size = size
        self._signal: List[int] = signal

    @property
    def signal(self) -> str:
        return ''.join((str(n) for n in self._signal[0:8]))

    def phase(self, amount: int):
        for _ in range(amount):
            output = []
            for index in range(1, self._signal_size + 1):
                pattern = chain.from_iterable(r for r in (repeat(c, index) for c in cycle([0, 1, 0, -1])))
                next(pattern)
                output.append(abs(sum(n * next(pattern) for n in self._signal)) % 10)
            self._signal = output

    def phase_from_offset(self, amount: int):
        # calculating the digits of the output for positions more than half of the signal length are just a cumulative sum of the remaining digits mod 10
        self._signal = list(reversed(self._signal))
        for _ in range(amount):
            self._signal = [n % 10 for n in accumulate(self._signal)]
        self._signal = list(reversed(self._signal))


class Day16(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._input = [int(s) for s in self._load_input_as_string()]

    def part_one(self):
        fft = FlawedFrequencyTransmission(self._input, len(self._input))
        fft.phase(100)
        return fft.signal

    def part_two(self):
        offset = int("".join((str(n) for n in self._input[0:7])))
        print(f"signal offset : {offset}")
        offset_input = [int(s) for s in (self._load_input_as_string() * 10000)[offset:]]
        fft = FlawedFrequencyTransmission(offset_input, len(offset_input))
        fft.phase_from_offset(100)

        return fft.signal
