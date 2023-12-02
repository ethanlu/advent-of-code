from __future__ import annotations
from adventofcode.common import Solution


class CubeGame(object):
    def __init__(self, s: str):
        self._s = s

        t = self._s.split(':')
        self._game = int(t[0][5:])

        self._reds = []
        self._greens = []
        self._blues = []
        for r in t[1].split(';'):
            for c in r.strip().split(','):
                match c.strip().split(' '):
                    case n, 'red':
                        self._reds.append(int(n))
                    case n, 'green':
                        self._greens.append(int(n))
                    case n, 'blue':
                        self._blues.append(int(n))

    @property
    def game(self) -> int:
        return self._game

    @property
    def power(self) -> int:
        return max(self._reds) * max(self._greens) * max(self._blues)

    def possible(self, r: int, g: int, b: int) -> bool:
        return len(list(filter(lambda i: i > r, self._reds))) == 0 and \
            len(list(filter(lambda i: i > g, self._greens))) == 0 and \
            len(list(filter(lambda i: i > b, self._blues))) == 0

class Day02(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._input = self._load_input_as_lines()

    def part_one(self):
        total = 0
        for s in self._input:
            g = CubeGame(s)
            if g.possible(12, 13, 14):
                total += g.game
            else:
                print(f"Game {g.game} is impossible")

        return total

    def part_two(self):
        total = 0
        for s in self._input:
            g = CubeGame(s)
            total += g.power

        return total
    