from collections import deque

import re


class DecompressionFormat(object):
    def __init__(self):
        pass

    def decompress(self, s):
        response = 0
        i = 0
        while i < len(s):
            current = s[i]

            if current == '(':
                # beginning of marker found, interpret the rest of the marker
                i += 1
                j = s.index(')', i)

                # marker info is the next j characters after i
                (length, repeat) = s[i:j].split('x')

                # after getting marker, move i to character after closing ) + the length of characters to read
                i = j + 1 + int(length)

                response += len(s[(j + 1):i] * int(repeat))
            else:
                # current is a non-marker, add to response and proceed to next
                i += 1
                response += 1

        return response

class DecompressionFormat2(object):
    def __init__(self):
        pass

    def decompress(self, s):
        response = 0
        i = 0
        while i < len(s):
            current = s[i]

            if current == '(':
                # beginning of marker found, interpret the rest of the marker
                i += 1
                j = s.index(')', i)

                # marker info is the next j characters after i
                (length, repeat) = s[i:j].split('x')

                # after getting marker, move i to character after closing ) + the length of characters to read
                i = j + 1 + int(length)

                response += self.decompress(s[(j + 1):i]) * int(repeat)
            else:
                # current is a non-marker, add to response and proceed to next
                i += 1
                response += 1

        return response

class Day09(object):
    def __init__(self, input_file):
        with open(input_file) as f:
            self._input = f.read().strip()

    def part_one(self):
        # O(n) time complexity (n is number of chars in input)
        # O(c) space complexity
        return DecompressionFormat().decompress(self._input)

    def part_two(self):
        # O(n) time complexity (n is number of chars in input)
        # O(c) space complexity
        return DecompressionFormat2().decompress(self._input)

if __name__ == '__main__':
    p = Day09('../../input/2016/day09.txt')

    print('-----part one-----')
    print(p.part_one())

    print('-----part two-----')
    print(p.part_two())
