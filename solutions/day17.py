input = [33,14,18,20,45,35,16,35,1,13,18,13,50,44,48,6,24,41,30,42]

class Day17(object):
    def __init__(self, containers):
        self.containers = containers

    def _find_combinations(self, required_total, current_total, current_container_index):
        if current_container_index == len(self.containers) - 1:
            if current_total + self.containers[current_container_index] <= required_total:
                return [[current_container_index]]
            else:
                return []
        else:
            container_index_combinations = []
            i = current_container_index
            while i < len(self.containers):
                if current_total + self.containers[i] <= required_total:
                    combinations = self._find_combinations(required_total, current_total + self.containers[i], i + 1)

                    if len(combinations):
                        for c in combinations:
                            container_index_combinations.append([i] + c)
                    else:
                        container_index_combinations.append([i])
                i += 1

            return container_index_combinations

    def part_one(self, required_amount):
        combinations = filter(lambda x: sum(x) == required_amount, [[self.containers[i] for i in c] for c in self._find_combinations(required_amount, 0, 0)])

        return len(combinations)

    def part_two(self, required_amount):
        combinations =  filter(lambda x: sum(x) == required_amount, [[self.containers[i] for i in c] for c in self._find_combinations(required_amount, 0, 0)])
        combination_lengths = [len(c) for c in combinations]
        minimum_length = min(combination_lengths)

        return len(filter(lambda x: x == minimum_length, combination_lengths))
