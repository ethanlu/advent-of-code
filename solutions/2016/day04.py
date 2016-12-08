from itertools import islice
import re


class Code(object):
    def __init__(self, s):
        r = re.match('(.*)\-(\d+)\[([a-z]+)\]', s)

        self._name = r.group(1)
        self._sector = int(r.group(2))
        self._checksum = r.group(3)

    def is_valid(self, n):
        tmp = {}
        for c in self._name.replace('-', ''):
            if c not in tmp:
                tmp[c] = 0
            tmp[c] += 1

        # sort by letter count descending and then letter ascendinfg
        tmp = sorted(sorted([(v, k) for k, v in tmp.items()], key=lambda x: x[1]), key=lambda x: x[0], reverse=True)

        return ''.join([i[1] for i in list(islice(tmp, 0, n))]) == self._checksum

    def decrypt(self):
        s = ''
        shift = self._sector % 26
        for c in self._name.replace('-', ' '):
            if c == ' ':
                new_c = ' '
            elif ord(c) + shift > ord('z'):
                new_c = chr(96 + (ord(c) + shift) % ord('z'))
            else:
                new_c = chr(ord(c) + shift)
            s += new_c

        return s

    @property
    def sector(self):
        return self._sector


class Day04(object):
    def __init__(self, input_file):
        with open(input_file) as f:
            self._input = [Code(l) for l in f.readlines()]

    def part_one(self):
        # O(n) time complexity (n is number of lines in input)
        # O(n) space complexity
        return sum([code.sector for code in self._input if code.is_valid(5)])

    def part_two(self):
        # O(n) time complexity (n is length of movements in entire file)
        # O(c) space complexity
        sector = None
        for code in self._input:
            s = code.decrypt()

            if s == 'northpole object storage':
                sector = code.sector
                break

        return sector

if __name__ == '__main__':
    p = Day04('../../input/2016/day04.txt')

    print('-----part one-----')
    print(p.part_one())

    print('-----part two-----')
    print(p.part_two())
