from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.range import Interval
from functools import reduce
from typing import List


def doubles(items: List):
    for i in range(0, len(items), 2):
        if i + 2 < len(items):
            yield items[i:i + 2]
        else:
            yield items[i:]


class ContiguousBlock(object):
    def __init__(self, start: int, end: int, value: int):
        self._range = Interval(start, end)
        self._value = value

    def __lt__(self, other):
        return self.range.left < other.range.left

    def __le__(self, other):
        return self.range.left <= other.range.left

    def __gt__(self, other):
        return self.range.left > other.range.left

    def __ge__(self, other):
        return self.range.left >= other.range.left

    @property
    def range(self) -> Interval:
        return self._range

    @property
    def indices(self) -> List[int]:
        return list(range(self.range.left, self.range.left + self.length))

    @property
    def length(self) -> int:
        return self.range.right - self.range.left + 1

    def is_free(self) -> bool:
        return self._value == -1

    def is_neighbor(self, candidate: ContiguousBlock) -> bool:
        return self.range.overlaps(candidate.range)


class Disk(object):
    def __init__(self, data: List[int]):
        self._disk = []
        for file_id, blocks in enumerate(list(doubles(data))):
            file_size, free_space = blocks + [0] * (2 - len(blocks))
            self._disk += [file_id] * file_size + [-1] * free_space

    def show(self) -> None:
        print("".join(('.' if v == -1 else '◼' for v in self._disk)))

    def compact(self) -> None:
        for space_index, data_index in zip([i for i, v in enumerate(self._disk) if v == -1], list(reversed([i for i, v in enumerate(self._disk) if v != -1]))):
            if space_index < data_index:
                # keep swapping free space block index with data block index until their indices cross or meet
                self._disk[data_index], self._disk[space_index] = self._disk[space_index], self._disk[data_index]
            else:
                break

    def checksum(self) -> int:
        return reduce(lambda total, block: total + block[0] * block[1] if block[1] != -1 else total, enumerate(self._disk), 0)


class ContiguousDisk(Disk):
    def __init__(self, data: List[int]):
        super().__init__(data)
        self._data_blocks = []
        self._free_blocks = []
        value = self._disk[0]
        start = 0
        for i, v in enumerate(self._disk):
            if value == v:
                continue
            # start of new contiguous block
            if value == -1:
                # current block is free
                self._free_blocks.append(ContiguousBlock(start, i - 1, -1))

            else:
                # current block is data
                self._data_blocks.append(ContiguousBlock(start, i - 1, value))
            value = v
            start = i
        if value == -1:
            # last block is free
            self._free_blocks.append(ContiguousBlock(start, len(self._disk) - 1, -1))
        else:
            # last block is data
            self._data_blocks.append(ContiguousBlock(start, len(self._disk) - 1, value))

    def compact(self) -> None:
        for db in reversed(self._data_blocks):
            free_blocks = []
            remaining_free_blocks = []
            for i, fb in enumerate(self._free_blocks):
                if fb.range.left > db.range.left:
                    # exhausted all free blocks to the left of the data block, cannot move data block
                    free_blocks += self._free_blocks[i:]
                    break
                if fb.length < db.length:
                    # free block too small, skip to next free block
                    free_blocks.append(fb)
                    continue
                # free block found...swap
                for space_index, data_index in zip(fb.indices, db.indices):
                    self._disk[data_index], self._disk[space_index] = self._disk[space_index], self._disk[data_index]
                if fb.length > db.length:
                    free_blocks.append(ContiguousBlock(fb.range.left + db.length, fb.range.right, -1))
                free_blocks += self._free_blocks[i + 1:]
                break
            self._free_blocks = free_blocks


class Day09(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._disk = Disk([int(c) for c in self._load_input_as_string()])
        self._contiguous_disk = ContiguousDisk([int(c) for c in self._load_input_as_string()])

    def part_one(self):
        self._disk.compact()
        self._disk.show()
        return self._disk.checksum()

    def part_two(self):
        self._contiguous_disk.compact()
        self._contiguous_disk.show()
        return self._contiguous_disk.checksum()
