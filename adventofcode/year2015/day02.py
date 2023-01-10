from adventofcode import Solution


class Day02(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)

        self._input = [l.strip().split('x') for l in self._load_input_as_lines()]

    def part_one(self):
        return sum([2*l*w + 2*w*h + 2*h*l + min(l*w, w*h, l*h) for (l, w, h) in map(lambda d: (int(d[0]), int(d[1]), int(d[2])), self._input)])

    def part_two(self):
        return sum([l*w*h + min((2*l+2*w), (2*w+2*h), (2*h+2*l)) for (l, w, h) in map(lambda d: (int(d[0]), int(d[1]), int(d[2])), self._input)])
