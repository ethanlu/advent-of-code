from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.grid import Point2D
from typing import List, Set

import re


space_regex = re.compile(r"\s+")


class BingoCard(object):
    def __init__(self, id: str, data: List[str]):
        self._id = id
        self._marked_rows = {i: 0 for i in range(5)}
        self._marked_columns = {i: 0 for i in range(5)}
        self._unmarked_numbers = set()
        self._numbers = {}
        for y, row in enumerate(data):
            for x, cell in enumerate(re.split(space_regex, row)):
                p = Point2D(x, y)
                n = int(cell)
                if n not in self._numbers:
                    self._numbers[n] = set()
                self._numbers[n].add(p)
                self._unmarked_numbers.add(n)

    @property
    def id(self) -> str:
        return self._id

    @property
    def score(self) -> int:
        return sum((n for n in self._unmarked_numbers))

    def mark(self, number: int):
        if number in self._unmarked_numbers:
            self._unmarked_numbers.remove(number)
            for position in self._numbers[number]:
                self._marked_rows[position.y] += 1
                self._marked_columns[position.x] += 1

    def bingo(self) -> bool:
        return any([v == 5 for v in self._marked_rows.values()]) or any([v == 5 for v in self._marked_columns.values()])


class Day04(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._numbers = None
        self._cards = []
        card = []
        for i, line in enumerate(self._load_input_as_lines()):
            if i == 0:
                self._numbers = [int(n) for n in line.split(',')]
            elif i > 1:
                if not line:
                    self._cards.append(BingoCard(str(len(self._cards)), card))
                    card = []
                else:
                    card.append(line)
        self._cards.append(BingoCard(str(len(self._cards)), card))

    def part_one(self):
        for drawn_number in self._numbers:
            print(f"drawn : {drawn_number}")
            for card in self._cards:
                card.mark(drawn_number)
                if card.bingo():
                    print(f"\tcard {card.id} has bingo with score of {card.score}")
                    return card.score * drawn_number
        return 0

    def part_two(self):
        remaining_cards = [c for c in self._cards]
        for drawn_number in self._numbers:
            print(f"drawn : {drawn_number} with {len(remaining_cards)} cards remaining...")
            next_remaining = []
            for card in remaining_cards:
                card.mark(drawn_number)
                if card.bingo():
                    if len(remaining_cards) == 1:
                        print(f"\tcard {card.id} has bingo and it is the last card with score of {card.score}")
                        return card.score * drawn_number
                    else:
                        print(f"\tcard {card.id} has bingo...")
                else:
                    next_remaining.append(card)
            remaining_cards = next_remaining
        return 0
