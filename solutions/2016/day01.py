class Position(object):
    def __init__(self, x, y):
        self._x = x
        self._y = y

    def move(self, direction, distance):
        if (direction == 'north'):
            coordinates_traveled = [(self._x, self._y + i) for i in range(1, distance + 1)]
            self._y += distance
        elif (direction == 'east'):
            coordinates_traveled = [(self._x + i, self._y) for i in range(1, distance + 1)]
            self._x += distance
        elif (direction == 'south'):
            coordinates_traveled = [(self._x, self._y - i) for i in range(1, distance + 1)]
            self._y -= distance
        else:
            coordinates_traveled = [(self._x - i, self._y) for i in range(1, distance + 1)]
            self._x -= distance

        return coordinates_traveled


class Day01(object):
    direction_map = {
        'north': {'L': 'west',
                  'R': 'east'},
        'east': {'L': 'north',
                 'R': 'south'},
        'south': {'L': 'east',
                  'R': 'west'},
        'west': {'L': 'south',
                 'R': 'north'}
    }

    def __init__(self, input_file):
        with open(input_file) as f:
            self._input = f.read().strip().split(', ')

    def part_one(self):
        # O(n) time complexity (n is length of input)
        # O(c) space complexity
        blocks_traveled =  {
            'north': 0,
            'east': 0,
            'south': 0,
            'west': 0
        }

        currently_facing = 'north'
        for i in self._input:
            direction = i[0]
            distance = int(i[1:])
            blocks_traveled[Day01.direction_map[currently_facing][direction]] += distance
            currently_facing = Day01.direction_map[currently_facing][direction]

        return abs(blocks_traveled['north'] - blocks_traveled['south']) + abs(blocks_traveled['east'] - blocks_traveled['west'])

    def part_two(self):
        # O(nm) time complexity (n is length of input, m is length of distances)
        # O(k) space complexity (k is number of unique coordinates in input)
        visited = set([(0,0)])

        rabbit_hq_coordinate = None
        position = Position(0, 0)
        currently_facing = 'north'
        for i in self._input:
            direction = i[0]
            distance = int(i[1:])
            currently_facing = Day01.direction_map[currently_facing][direction]

            #print('moving ' + currently_facing + ' ' + str(distance))
            for coordinate in position.move(currently_facing, distance):
                #print(coordinate)
                if coordinate in visited:
                    rabbit_hq_coordinate = coordinate
                    break
                visited.add(coordinate)

            if rabbit_hq_coordinate is not None:
                break

        return abs(rabbit_hq_coordinate[0]) + abs(rabbit_hq_coordinate[1])

if __name__ == '__main__':
    p = Day01('../../input/2016/day01.txt')

    print('-----part one-----')
    print(p.part_one())

    print('-----part two-----')
    print(p.part_two())
