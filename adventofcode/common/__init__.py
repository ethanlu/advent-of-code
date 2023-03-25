from typing import List

import os


class Solution(object):
    def __init__(self, year: str, day: str):
        self._year = year
        self._day = day

    def _load_input_as_string(self, strip: bool = True) -> str:
        file_path = f"{os.environ['ADVENT_OF_CODE_INPUT']}/{self._year}/day{self._day}.txt"
        with open(file_path) as f:
            if strip:
                return f.read().replace('\n', '').strip()
            else:
                return f.read().replace('\n', '')

    def _load_input_as_lines(self, strip: bool = True) -> List[str]:
        file_path = f"{os.environ['ADVENT_OF_CODE_INPUT']}/{self._year}/day{self._day}.txt"
        with open(file_path) as f:
            if strip:
                return [line.strip() for line in f.readlines()]
            else:
                return [line for line in f.readlines()]

    def _init(self):
        raise Exception("_init not implemented!")

    def part_one(self):
        raise Exception("part 1 not implemented!")

    def part_two(self):
        raise Exception("part 2 not implemented!")
