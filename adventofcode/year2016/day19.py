from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.graph import LinkedListNode


class Elf(LinkedListNode):
    def __init__(self, index: int, presents: int):
        super().__init__(f"{index}")
        self._index = index
        self._presents = presents

    @property
    def index(self) -> int:
        return self._index

    @property
    def presents(self) -> int:
        return self._presents

    @presents.setter
    def presents(self, presents: int):
        self._presents = presents


class WhiteElephantParty(object):
    def __init__(self, elves: int):
        self._start_elf = Elf(1, 1)
        self._halfway_elf = None
        self._current_length = elves

        half = elves // 2
        current_elf = self._start_elf
        for i in range(1, elves):
            elf = Elf(i + 1, 1)
            current_elf.next = elf
            elf.previous = current_elf
            current_elf = elf
            self._halfway_elf = current_elf if i == half else self._halfway_elf
        current_elf.next = self._start_elf
        self._start_elf.previous = current_elf

    def exchange_left(self) -> Elf:
        while self._start_elf.next != self._start_elf:
            # steal presents
            next_elf = self._start_elf.next
            self._start_elf.presents += next_elf.presents

            # update links
            self._start_elf.next = next_elf.next
            next_elf.next.previous = self._start_elf
            next_elf.previous = None

            # move to next
            self._start_elf = self._start_elf.next

        return self._start_elf

    def exchange_across(self):
        while self._start_elf.next != self._start_elf:
            # steal presents
            next_elf = self._halfway_elf
            self._start_elf.presents += next_elf.presents

            # update links
            next_elf.previous.next = next_elf.next
            next_elf.next.previous = next_elf.previous

            # move to next
            self._start_elf = self._start_elf.next

            # adjust halfway elf
            self._current_length -= 1
            self._halfway_elf = next_elf.next.next if self._current_length % 2 == 0 else next_elf.next

        return self._start_elf


class Day19(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._input = self._load_input_as_string()

    def part_one(self):
        party = WhiteElephantParty(int(self._input))
        elf = party.exchange_left()

        print(f"elf {elf.index} has {elf.presents} presents")

        return elf.index

    def part_two(self):
        party = WhiteElephantParty(int(self._input))
        elf = party.exchange_across()

        print(f"elf {elf.index} has {elf.presents} presents")

        return elf.index
