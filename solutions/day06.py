import re

class Day06(object):
    def __init__(self, input_file):
        with open(input_file) as f:
            self._instructions = map(lambda l: self._parse_instruction(l.strip()), f.readlines())

        self._light_grid = [[False for x in xrange(1000)] for x in xrange(1000)]
        self._brightness_grid = [[0 for x in xrange(1000)] for x in xrange(1000)]

    def _parse_instruction(self, s):
        r = re.match('([a-z\s]+) (\d+),(\d+) through (\d+),(\d+)', s)
        if r is None:
            raise Exception('invalid instruction : ' + s)

        # parse instructions into tuple of command, starting x, starting y, ending x, and ending y
        return (r.group(1).replace(' ', '_'), int(r.group(2)), int(r.group(3)), int(r.group(4)), int(r.group(5)))

    # commands for light grid
    def _light_turn_on(self, x, y):
        self._light_grid[x][y] = True

    def _light_turn_off(self, x, y):
        self._light_grid[x][y] = False

    def _light_toggle(self, x, y):
        self._light_grid[x][y] = not self._light_grid[x][y]

    # commands for brightness grid
    def _brightness_turn_on(self, x, y):
        self._brightness_grid[x][y] += 1

    def _brightness_turn_off(self, x, y):
        self._brightness_grid[x][y] -= 1

        if self._brightness_grid[x][y] < 0:
            self._brightness_grid[x][y] = 0

    def _brightness_toggle(self, x, y):
        self._brightness_grid[x][y] += 2

    def part_one(self):
        for (command, startx, starty, endx, endy) in self._instructions:
            for x in xrange(startx, endx + 1):
                for y in xrange(starty, endy + 1):
                    getattr(self, '_' + 'light_' + command)(x, y)

        return sum((self._light_grid[x][y] for x in xrange(1000) for y in xrange(1000)))

    def part_two(self):
        for (command, startx, starty, endx, endy) in self._instructions:
            for x in xrange(startx, endx + 1):
                for y in xrange(starty, endy + 1):
                    getattr(self, '_' + 'brightness_' + command)(x, y)

        return sum((self._brightness_grid[x][y] for x in xrange(1000) for y in xrange(1000)))


if __name__ == '__main__':
    p = Day06('input/day06.txt')

    print '-----part one-----'
    print p.part_one()

    print '-----part two-----'
    print p.part_two()
