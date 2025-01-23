from __future__ import annotations
from adventofcode.common import Solution


class KeyLock(object):
    def __init__(self, data: str):
        self._data = data
        self._is_lock = self._data[:5] == '#' * 5
        self._id = int(self._data[5:-5].replace('#', '1').replace('.', '0'), 2)

    @property
    def id(self) -> int:
        return self._id

    @property
    def is_lock(self) -> bool:
        return self._is_lock


class Day25(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._keys = []
        self._locks = []
        data = ''
        for line in self._load_input_as_lines():
            if not line:
                keylock = KeyLock(data)
                if keylock.is_lock:
                    self._locks.append(keylock)
                else:
                    self._keys.append(keylock)
                data = ''
                continue
            data += line
        keylock = KeyLock(data)
        if keylock.is_lock:
            self._locks.append(keylock)
        else:
            self._keys.append(keylock)

    def part_one(self):
        matches = 0
        for key in self._keys:
            for lock in self._locks:
                matches += 1 if (key.id & lock.id) == 0 else 0
        return matches

    def part_two(self):
        pass