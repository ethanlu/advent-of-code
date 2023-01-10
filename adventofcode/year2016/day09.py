from adventofcode import Solution


class DecompressionFormat(object):
    def __init__(self, version=1):
        self._version = version

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

                if self._version == 1:
                    response += len(s[(j + 1):i] * int(repeat))
                else:
                    response += self.decompress(s[(j + 1):i]) * int(repeat)
            else:
                # current is a non-marker, add to response and proceed to next
                i += 1
                response += 1

        return response


class Day09(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)

        self._input = self._load_input_as_string()

    def part_one(self):
        # O(n) time complexity (n is number of chars in input)
        # O(c) space complexity
        return DecompressionFormat(version=1).decompress(self._input)

    def part_two(self):
        # O(n) time complexity (n is number of chars in input)
        # O(c) space complexity
        return DecompressionFormat(version=2).decompress(self._input)
