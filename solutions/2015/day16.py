import re


class Day16(object):
    def __init__(self, input_file):
        self._matching_properties = {'children': 3,
                                     'cats': 7,
                                     'samoyeds': 2,
                                     'pomeranians': 3,
                                     'akitas': 0,
                                     'vizslas': 0,
                                     'goldfish': 5,
                                     'trees': 3,
                                     'cars': 2,
                                     'perfumes': 1}
        self._aunts = {}

        with open(input_file) as f:
            for l in f.readlines():
                r = re.match('^Sue (\d+): (.*)$', l)

                if r is None:
                    raise Exception('invalid input : ' + l)

                aunt_id = int(r.group(1))
                self._aunts[aunt_id] = {}

                properties = r.group(2).split(',')
                for property in properties:
                    tmp = property.split(':')
                    self._aunts[aunt_id][tmp[0].strip()] = int(tmp[1].strip())

    def part_one(self):
        best_matched_aunt = 0
        best_matches = 0

        for aunt_id in self._aunts.keys():
            matches = len([1 for aunt_property in self._aunts[aunt_id].keys() if aunt_property in self._matching_properties.keys() and self._aunts[aunt_id][aunt_property] == self._matching_properties[aunt_property]])

            if best_matches == 0 or best_matches < matches:
                best_matches = matches
                best_matched_aunt = aunt_id

        return best_matched_aunt

    def part_two(self):
        best_matched_aunt = 0
        best_matches = 0

        for aunt_id in self._aunts.keys():
            matches = 0
            for aunt_property in self._aunts[aunt_id].keys():
                if aunt_property in self._matching_properties.keys():
                    if aunt_property in ['cats', 'trees']:
                        if self._aunts[aunt_id][aunt_property] > self._matching_properties[aunt_property]:
                            matches += 1
                    elif aunt_property in ['pomeranians', 'goldfish']:
                        if self._aunts[aunt_id][aunt_property] < self._matching_properties[aunt_property]:
                            matches += 1
                    else:
                        if self._aunts[aunt_id][aunt_property] == self._matching_properties[aunt_property]:
                            matches += 1

            if best_matches == 0 or best_matches < matches:
                best_matches = matches
                best_matched_aunt = aunt_id

        return best_matched_aunt


if __name__ == '__main__':
    p = Day16('../../input/2015/day16.txt')

    print '-----part one-----'
    print p.part_one()

    print '-----part two-----'
    print p.part_two()