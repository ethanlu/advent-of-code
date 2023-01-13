from functools import reduce
from adventofcode.common import Solution


class Day24(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)

        self.weights = list(int(l) for l in self._load_input_as_lines())

    def _find_all_groups_of_size(self, group_size, group_weight):
        def recurse_remaining(i, current_total, group):
            if i >= len(self.weights) or len(group) > group_size:
                # no more weights to consider or current group is already bigger than the desired size...so stop
                pass
            elif current_total + self.weights[i] == group_weight :
                # current weight + group meets the weight requirement...add it to group
                groups.add(tuple(group + [self.weights[i]]))
            else:
                k = i
                while k < len(self.weights):
                    k += 1
                    if current_total + self.weights[i] < group_weight:
                        # adding current weight is still under, so include it and try remaining
                        recurse_remaining(k, current_total + self.weights[i], group + [self.weights[i]])
                    else:
                        # adding current weight will go over, so exclude it but try remaining
                        recurse_remaining(k, current_total, group)

        groups = set([])
        for c in range(len(self.weights)):
            recurse_remaining(c, 0, [])

        return groups

    def _quantum_entanglement(self, group_weights):
        return reduce(lambda x, y: x * y, group_weights)

    def part_one(self):
        # just find the smallest group that adds up to the weight_per_group value. within this group, sort them by quantum entanglement
        # and return first
        best_groups = []
        for s in range(1, len(self.weights)):
            print('look for group if size ' + str(s))
            groups = self._find_all_groups_of_size(s, sum(self.weights)/3)

            if len(groups) > 0:
                best_groups = groups
                break

        return min([self._quantum_entanglement(group) for group in best_groups])

    def part_two(self):
        # just find the smallest group that adds up to the weight_per_group value. within this group, sort them by quantum entanglement
        # and return first
        best_groups = []
        for s in range(1, len(self.weights)):
            print('look for group if size ' + str(s))
            groups = self._find_all_groups_of_size(s, sum(self.weights)/4)

            if len(groups) > 0:
                best_groups = groups
                break

        return min([self._quantum_entanglement(group) for group in best_groups])
