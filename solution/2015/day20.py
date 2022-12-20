class Day20(object):
    def __init__(self, input_file):
        with open(input_file) as f:
            self._number = int(f.read().strip())

    def _get_factors_sum(self, n, gift_factor, house_limit):
        factors = set([])
        for i in xrange(1, int(n**0.5) + 1):
            if n % i == 0:
                if house_limit == 0 or i * house_limit >= n:
                    factors.add(i)
                    factors.add(n / i)
                else:
                    if (n / i ) * house_limit >= n:
                        factors.add(n / i)

        return (sum([i for i in factors]) * gift_factor)

    def part_one(self):
        i = 1
        largest = 0
        while True:
            fsum = self._get_factors_sum(i, 10, 0)

            if largest < fsum:
                largest = fsum
            #print(str(i) + ' : ' + str(largest))

            if fsum >= self._number:
                break

            i += 1

        return i

    def part_two(self):
        i = 1
        largest = 0
        while True:
            fsum = self._get_factors_sum(i, 11, 50)

            if largest < fsum:
                largest = fsum
            #print(str(i) + ' : ' + str(largest))

            if fsum >= self._number:
                break

            i += 1

        return i


if __name__ == '__main__':
    p = Day20('../../input/2015/day20.txt')

    print('-----part one-----')
    print(p.part_one())

    print('-----part two-----')
    print(p.part_two())
