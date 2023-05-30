from __future__ import annotations
from adventofcode.common import Solution


class PublicPrivateKeyEncryption(object):
    def __init__(self, subject: int):
        self._subject = subject

    def transform(self, loop_size: int) -> int:
        return pow(self._subject, loop_size, 20201227)


class Day25(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._keys = [int(line) for line in self._load_input_as_lines()]

    def part_one(self):
        ppke = PublicPrivateKeyEncryption(7)

        loop_sizes = []
        for key in self._keys:
            print(f"public key {key}: ")
            loop_size = 1
            i = 0
            while ppke.transform(loop_size) != key:
                loop_size += 1
                i += 1
                if i > 1000:
                    print(".", end="")
                    i = 0
            print(f"loop size of {loop_size} yields {key}")
            loop_sizes.append(loop_size)

        encryption_keys = [
            PublicPrivateKeyEncryption(self._keys[1]).transform(loop_sizes[0]),
            PublicPrivateKeyEncryption(self._keys[0]).transform(loop_sizes[1])
        ]
        print(f"\nencryption keys : {encryption_keys}\n")

        return encryption_keys[0]

    def part_two(self):
        return "ᕕ( ᐛ )ᕗ"