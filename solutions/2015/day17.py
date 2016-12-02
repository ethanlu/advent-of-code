class Day17(object):
    def __init__(self, input_file):
        with open(input_file) as f:
            self._containers = [int(l.strip()) for l in f.readlines()]

    def _find_combinations(self, required_total, current_total, current_container_index):
        if current_container_index == len(self._containers) - 1:
            if current_total + self._containers[current_container_index] <= required_total:
                return [[current_container_index]]
            else:
                return []
        else:
            container_index_combinations = []
            i = current_container_index
            while i < len(self._containers):
                if current_total + self._containers[i] <= required_total:
                    combinations = self._find_combinations(required_total, current_total + self._containers[i], i + 1)

                    if len(combinations):
                        for c in combinations:
                            container_index_combinations.append([i] + c)
                    else:
                        container_index_combinations.append([i])
                i += 1

            return container_index_combinations

    def part_one(self, required_amount):
        combinations = filter(lambda x: sum(x) == required_amount, [[self._containers[i] for i in c] for c in self._find_combinations(required_amount, 0, 0)])

        return len(combinations)

    def part_two(self, required_amount):
        combinations =  filter(lambda x: sum(x) == required_amount, [[self._containers[i] for i in c] for c in self._find_combinations(required_amount, 0, 0)])
        combination_lengths = [len(c) for c in combinations]
        minimum_length = min(combination_lengths)

        return len(filter(lambda x: x == minimum_length, combination_lengths))


if __name__ == '__main__':
    p = Day17('input/2015/day17.txt')

    print '-----part one-----'
    print p.part_one(150)

    print '-----part two-----'
    print p.part_two(150)