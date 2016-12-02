class Day01(object):
    def __init__(self, input_file):
        with open(input_file) as f:
            self._input = f.read().replace('\n','').strip()

    def part_one(self):
        return self._input.count('(') - self._input.count(')')

    def part_two(self):
        floor = 0
        position = 0
        while floor >= 0:
            floor += 1 if self._input[position] == '(' else -1
            position += 1

        return position

if __name__ == '__main__':
    p = Day01('../../input/2015/day01.txt')

    print '-----part one-----'
    print p.part_one()

    print '-----part two-----'
    print p.part_two()
