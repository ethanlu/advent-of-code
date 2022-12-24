from collections import deque
from adventofcode import Solution

import re


class Lcd(object):
    rect_regex = re.compile('rect (\d+)x(\d+)')
    rotate_row_regex = re.compile('rotate row y=(\d+) by (\d+)')
    rotate_column_regex = re.compile('rotate column x=(\d+) by (\d+)')

    def __init__(self, w, h):
        self._width = w
        self._height = h
        self._screen = None
        self.reset()

    def reset(self):
        self._screen = [[False for y in range(self._height)] for x in range(self._width)]
        return self

    def execute(self, instruction):
        if self.rect_regex.match(instruction):
            r = self.rect_regex.findall(instruction)[0]
            return self.rect(int(r[0]), int(r[1]))
        elif self.rotate_row_regex.match(instruction):
            r = self.rotate_row_regex.findall(instruction)[0]
            return self.rotate_row(int(r[0]), int(r[1]))
        elif self.rotate_column_regex.match(instruction):
            r = self.rotate_column_regex.findall(instruction)[0]
            return self.rotate_column(int(r[0]), int(r[1]))
        else:
            raise Exception('Invalid instruction : {s}'.format(s=instruction))

    def rect(self, a, b):
        for x in range(a):
            for y in range(b):
                self._screen[x][y] = True
        return self

    def rotate_row(self, y, n):
        rotated_row = deque([self._screen[x][y] for x in range(self._width)])
        rotated_row.rotate(n)
        for i, v in enumerate(rotated_row):
            self._screen[i][y] = v
        return self

    def rotate_column(self, x, n):
        rotated_column = deque([self._screen[x][y] for y in range(self._height)])
        rotated_column.rotate(n)
        for i, v in enumerate(rotated_column):
            self._screen[x][i] = v
        return self

    def lit_count(self):
        lit = 0
        for x in range(self._width):
            for y in range(self._height):
                lit += 1 if self._screen[x][y] else 0
        return lit

    def show_screen(self):
        for y in range(self._height):
            for x in range(self._width):
               print('#' if self._screen[x][y] else '.', end='')
            print('')


class Day08(Solution):
    def _init(self):
        self._input = [l.strip() for l in self._load_input_as_lines()]

    def part_one(self):
        # O(n) time complexity (n is number of lines in input)
        # O(c) space complexity (n is number of lines in input)
        lcd = Lcd(50, 6)
        for instruction in self._input:
            lcd.execute(instruction)

        return lcd.lit_count()

    def part_two(self):
        # O(n) time complexity (n is number of lines in input)
        # O(c) space complexity (n is number of lines in input)
        lcd = Lcd(50, 6)
        for instruction in self._input:
            lcd.execute(instruction)

        return lcd.show_screen()
