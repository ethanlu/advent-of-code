from adventofcode import Solution


class Day02(Solution):
    def _init(self):
        self._boxes = map(lambda d: (int(d[0]), int(d[1]), int(d[2])), [l.strip().split('x') for l in self._load_input_as_lines()])

    def part_one(self):
        return sum([2*l*w + 2*w*h + 2*h*l + min(l*w, w*h, l*h) for (l, w, h) in self._boxes])

    def part_two(self):
        return sum([min((2*l+2*w), (2*w+2*h), (2*h+2*l)) + l*w*h for (l, w, h) in self._boxes])
