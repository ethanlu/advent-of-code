from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.graph import LinkedListNode, LLN
from functools import reduce
from typing import Dict, List


class Lens(LinkedListNode):
    def __init__(self, label: str, focal_length: int):
        super().__init__(f"{label} {focal_length}")
        self._label = label
        self._focal_length = focal_length

    def __str__(self) -> str:
        return f"[{self.label} {self.focal_length}]"

    @property
    def label(self) -> str:
        return self._label

    @property
    def focal_length(self) -> int:
        return self._focal_length

    @focal_length.setter
    def focal_length(self, focal_length: int) -> None:
        self._focal_length = focal_length


class LensBox():
    def __init__(self, n: int):
        self._box_number = n
        self._head = None
        self._tail = None
        self._lenses: Dict[str, Lens] = {}

    def __str__(self) -> str:
        return f"Box {self._box_number}: {' '.join((str(l) for l in self._lenses.values()))}"

    def empty(self) -> bool:
        return len(self._lenses) == 0

    def upsert(self, label: str, focal_length: int) -> None:
        if label in self._lenses.keys():
            self._lenses[label].focal_length = focal_length
        else:
            lens = Lens(label, focal_length)
            if self._tail:
                lens.next = self._tail
                if self._tail:
                    self._tail.previous = lens
            if not self._head:
                self._head = lens
            if self._head == self._tail:
                self._head.previous = lens
            self._tail = lens
            self._lenses[label] = lens

    def remove(self, label: str) -> None:
        if label in self._lenses:
            if self._lenses[label].previous:
                self._lenses[label].previous.next = self._lenses[label].next if self._lenses[label].next else None
            if self._lenses[label].next:
                self._lenses[label].next.previous = self._lenses[label].previous if self._lenses[label].previous else None
            if self._lenses[label] == self._head:
                self._head = self._head.previous
            if self._lenses[label] == self._tail:
                self._tail = self._tail.next
            self._lenses.pop(label)

    def focusing_power(self) -> int:
        slot = 1
        power = 0
        current = self._head
        while current:
            power += (self._box_number + 1) * slot * current.focal_length
            current = current.previous
            slot += 1
        return power

class LensConfiguration(object):
    def __init__(self, steps: List[str]):
        self._steps = steps
        self._boxes = [LensBox(i) for i in range(256)]

    def _hash(self, s: str) -> int:
        return reduce(lambda total, c: ((total + ord(c)) * 17) % 256, list(s), 0)

    def checksum(self) -> int:
        return reduce(lambda total, step: total + self._hash(step), self._steps, 0)

    def show(self):
        for lb in self._boxes:
            if not lb.empty():
                print(str(lb))

    def focusing_power(self) -> int:
        for i, step in enumerate(self._steps):
            if '-' in step:
                label = step[:-1]
                self._boxes[self._hash(label)].remove(label)
            elif '=' in step:
                t = step.split('=')
                label = t[0]
                focal_length = t[1]
                self._boxes[self._hash(label)].upsert(label, int(focal_length))
            else:
                raise Exception(f"Unexpected step : {step}")

        return reduce(lambda total, box: total + box.focusing_power(), self._boxes, 0)

class Day15(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._lc = LensConfiguration(self._load_input_as_string().split(','))

    def part_one(self):
        return self._lc.checksum()

    def part_two(self):
        focus_power = self._lc.focusing_power()
        self._lc.show()
        return focus_power