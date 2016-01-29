from itertools import cycle

class Day03(object):
    def __init__(self, input_file):
        with open(input_file) as f:
            self._directions = f.read().replace('\n','').strip()

    def _journey(self, directions):
        x = 0
        y = 0
        visited_houses = set([(x,y)])
        for d in directions:
            if d == '>':
                x+=1
            elif d == '<':
                x-=1
            elif d == '^':
                y+=1
            elif d == 'v':
                y-=1
            else:
                print 'error'
            visited_houses.add((x,y))
        return visited_houses

    def part_one(self):
        return len(self._journey(self._directions))

    def part_two(self):
        # use cycle module to alternate between the two direction lists
        direction_list = cycle([[],[]])
        map(lambda d: direction_list.next().append(d), self._directions)

        return len(self._journey(direction_list.next()).union(self._journey(direction_list.next())))

if __name__ == '__main__':
    p = Day03('input/day03.txt')

    print '-----part one-----'
    print p.part_one()

    print '-----part two-----'
    print p.part_two()
