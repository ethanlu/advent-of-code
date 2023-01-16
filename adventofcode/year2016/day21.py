from __future__ import annotations
from adventofcode.common import Solution
from typing import List


class Scrambler(object):
    def __init__(self, instructions: List[str], password: str):
        self._instructions = instructions
        self._password = list(password)

    @property
    def password(self):
        return ''.join(self._password)

    def _find_position(self, letter: str) -> int:
        return [i for i, c in enumerate(self._password) if c == letter][0]

    def _swap(self, x: int, y: int) -> None:
        self._password[x], self._password[y] = self._password[y], self._password[x]

    def _rotate(self, amount: int) -> None:
        amount = amount % len(self._password)
        self._password = self._password[amount:] + self._password[:amount]

    def _reverse(self, x: int, y: int) -> None:
        x, y = min(x, y), max(x, y)
        # [items before x] + [items from x to y reversed] + [elements after y]
        self._password = (self._password[:x] if x > 0 else []) + list(reversed(self._password[x:(y + 1)])) + (self._password[(y + 1):] if y + 1 < len(self.password) else [])

    def _move(self, s: int, d: int) -> None:
        if s < d:
            # [items before s] + [items after s to d] + [item at s] + [items after d]
            self._password = (self._password[:s] if s > 0 else []) + self._password[(s + 1):(d + 1)] + [self._password[s]] + (self._password[(d + 1):] if d + 1 < len(self.password) else [])
        elif s > d:
            # [items before d] + [item at s] + [items after d to s] + [items after s]
            self._password = (self._password[:d] if d > 0 else []) + [self._password[s]] + self._password[d:s] + (self._password[(s + 1):] if s + 1 < len(self.password) else [])
        else:
            pass

    def scramble(self, verbose: bool = False):
        if verbose:
            print(f"000 : {self.password} = start")
        for i, instruction in enumerate(self._instructions):
            match instruction.split(' '):
                case 'swap', 'position', index_x, 'with', 'position', index_y:
                    self._swap(int(index_x), int(index_y))
                case 'swap', 'letter', letter_x, 'with', 'letter', letter_y:
                    self._swap(self._find_position(letter_x), self._find_position(letter_y))
                case 'rotate', direction, amount, _:
                    self._rotate(int(amount) if direction == 'left' else -int(amount))
                case 'rotate', 'based', 'on', 'position', 'of', 'letter', letter_x:
                    index = self._find_position(letter_x)
                    self._rotate(-(index + (2 if index >= 4 else 1)))
                case 'reverse', 'positions', index_x, 'through', index_y:
                    self._reverse(int(index_x), int(index_y))
                case 'move', 'position', index_x, 'to', 'position', index_y:
                    self._move(int(index_x), int(index_y))
                case _:
                    raise Exception(f"Unrecognized instruction : {instruction}")
            if verbose:
                print(f"{str(i + 1).zfill(3)} : {self.password} = {instruction}")

    def unscramble(self, verbose: bool = False):
        if verbose:
            print(f"000 : {self.password} = start")
        for i, instruction in enumerate(reversed(self._instructions)):
            match instruction.split(' '):
                case 'swap', 'position', index_x, 'with', 'position', index_y:
                    self._swap(int(index_y), int(index_x))
                case 'swap', 'letter', letter_x, 'with', 'letter', letter_y:
                    self._swap(self._find_position(letter_y), self._find_position(letter_x))
                case 'rotate', direction, amount, _:
                    self._rotate(-int(amount) if direction == 'left' else int(amount))
                case 'rotate', 'based', 'on', 'position', 'of', 'letter', letter_x:
                    '''
                        se...... start at 0, end at 1 (rotated 1)
                        .s.e.... start at 1, end at 3 (rotated 2)
                        ..s..e.. start at 2, end at 5 (rotated 3)
                        ...s...e start at 3, end at 7 (rotated 4)
                        ..e.s... start at 4, end at 2 (rotated -2)
                        ....es.. start at 5, end at 4 (rotated -1)
                        ......s. start at 6, end at 6 (rotated 0)
                        e......s start at 7, end at 0 (rotated 1)
                    '''
                    end_at_index = self._find_position(letter_x)
                    if end_at_index % 2 == 1:
                        start_at_index = end_at_index // 2
                        self._rotate(end_at_index - start_at_index)
                    elif end_at_index == 0:
                        self._rotate(1)
                    elif end_at_index == 2:
                        self._rotate(-2)
                    elif end_at_index == 4:
                        self._rotate(-1)
                    else:
                        self._rotate(0)
                case 'reverse', 'positions', index_x, 'through', index_y:
                    self._reverse(int(index_y), int(index_x))
                case 'move', 'position', index_x, 'to', 'position', index_y:
                    self._move(int(index_y), int(index_x))
                case _:
                    raise Exception(f"Unrecognized instruction : {instruction}")
            if verbose:
                print(f"{str(i + 1).zfill(3)} : {self.password} = {instruction}")


class Day21(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._input = self._load_input_as_lines()

    def part_one(self):
        s = Scrambler(self._input, 'abcdefgh')
        s.scramble(True)

        return s.password

    def part_two(self):
        s = Scrambler(self._input, 'fbgdceah')
        s.unscramble(True)

        return s.password
