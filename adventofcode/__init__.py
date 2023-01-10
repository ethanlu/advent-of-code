from typing import List

import os


class Solution(object):
    def __init__(self, year: str, day: str):
        self._year = year
        self._day = day

    def _load_input_as_string(self) -> str:
        file_path = os.path.join(os.path.dirname(__file__), f"../input/{self._year}/day{self._day}.txt")
        with open(file_path) as f:
            return f.read().replace('\n', '').strip()

    def _load_input_as_lines(self) -> List[str]:
        file_path = os.path.join(os.path.dirname(__file__), f"../input/{self._year}/day{self._day}.txt")
        with open(file_path) as f:
            return f.readlines()

    def _init(self):
        raise Exception("_init not implemented!")

    def part_one(self):
        raise Exception("part 1 not implemented!")

    def part_two(self):
        raise Exception("part 2 not implemented!")
