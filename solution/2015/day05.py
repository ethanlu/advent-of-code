import re

class Day05(object):
    def __init__(self, input_file):
        with open(input_file) as f:
            self._strings = map(lambda l: l.strip(), f.readlines())

    def part_one(self):
        return len([i for i in self._strings if len(re.findall('(ab|cd|pq|xy)', i)) == 0 and len(re.findall('[aeiou]', i)) >= 3 and len(re.findall('(?P<letter>[a-z])(?P=letter)', i)) >= 1])

    def part_two(self):
        return len([i for i in self._strings if len(re.findall('(?P<letter>[a-z][a-z]).*(?P=letter)', i)) >= 1 and len(re.findall('(?P<letter>[a-z])[a-z](?P=letter)', i)) >= 1])


if __name__ == '__main__':
    p = Day05('../../input/2015/day05.txt')

    print('-----part one-----')
    print(p.part_one())

    print('-----part two-----')
    print(p.part_two())
