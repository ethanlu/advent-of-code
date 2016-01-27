class Day02(object):
    def __init__(self, input_file):
        with open(input_file) as f:
            # input file gets converted to list of tuples where each tuple is a (length, width, height) of a line
            self.boxes = map(lambda d: (int(d[0]), int(d[1]), int(d[2])), [l.strip().split('x') for l in f.readlines()])

    def part_one(self):
        return sum([2*l*w + 2*w*h + 2*h*l + min(l*w, w*h, l*h) for (l, w, h) in self.boxes])

    def part_two(self):
        return sum([min((2*l+2*w), (2*w+2*h), (2*h+2*l)) + l*w*h for (l, w, h) in self.boxes])

if __name__ == '__main__':
    p = Day02('input/day02.txt')

    print '-----part one-----'
    print p.part_one()

    print '-----part two-----'
    print p.part_two()