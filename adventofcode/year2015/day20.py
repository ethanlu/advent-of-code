from adventofcode import Solution


class Day20(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)

        self._number = int(self._load_input_as_string())

    def _get_factors_sum(self, n, gift_factor, house_limit):
        factors = set([])
        for i in range(1, int(n**0.5) + 1):
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
