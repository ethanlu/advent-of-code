from __future__ import annotations
from adventofcode.common import Solution
from functools import reduce
from itertools import pairwise
from typing import Iterable, List, Set, Tuple


def quadruplewise(iterable):
    for ((a, _), (b, _)), ((_, c), (_, d)) in pairwise(pairwise(pairwise(iterable))):
        yield a, b, c, d


def generate_secret(secret: int, nth: int) -> Iterable[int]:
    current = secret
    for i in range(nth):
        current = ((current << 6) ^ current) % 16777216
        current = ((current >> 5) ^ current) % 16777216
        current = ((current << 11) ^ current) % 16777216
        yield current


class Monkey(object):
    def __init__(self, secret: int, amount: int):
        self._secret = secret
        self._prices = [secret % 10] + [s % 10 for s in generate_secret(secret, amount)]
        self._consecutive_changes = {}
        for i, consecutive_change in enumerate(quadruplewise((b - a for a, b in pairwise(self._prices)))):
            if consecutive_change not in self._consecutive_changes:
                self._consecutive_changes[consecutive_change] = self._prices[(i + 4)]

    @property
    def secret(self) -> int:
        return self._secret

    @property
    def prices(self) -> List[int]:
        return self._prices

    def unique_consecutive_changes(self) -> Set[Tuple[int, int, int, int]]:
        return set(self._consecutive_changes.keys())

    def consecutive_change_price(self, consecutive_change: Tuple[int, int, int, int], default: int = 0) -> int:
        return self._consecutive_changes[consecutive_change] if consecutive_change in self._consecutive_changes else default


class Day22(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._secrets = [int(line) for line in self._load_input_as_lines()]

    def part_one(self):
        total = 0
        for secret in self._secrets:
            new_secret = list(generate_secret(secret, 2000))[-1]
            print(f"{secret} : {new_secret}")
            total += new_secret
        return total

    def part_two(self):
        largest_bananas = 0
        monkeys = [Monkey(int(line), 2000) for line in self._load_input_as_lines()]
        for consecutive_change in reduce(lambda all_unique_s, s: all_unique_s.union(s), (m.unique_consecutive_changes() for m in monkeys)):
            # for each sequence in the set of all unique sequences from all monkeys, get the total bananas that each monkey would sell for it
            total_bananas = sum((m.consecutive_change_price(consecutive_change) for m in monkeys))
            if largest_bananas < total_bananas:
                largest_bananas = total_bananas
                print(f"consecutive change {consecutive_change} yields {total_bananas} bananas")
        return largest_bananas
