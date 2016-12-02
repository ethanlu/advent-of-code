import json

class Day12(object):
    def __init__(self, input_file):
        with open(input_file) as f:
            self._json_document = map(lambda l: json.loads(l.strip()), f.readlines())[0]

    def _traverse(self, json_obj, ignore_red=False):
        total = 0

        if type(json_obj) == int:
            total += json_obj
        elif type(json_obj) == list:
            for value in json_obj:
                total += self._traverse(value, ignore_red)
        elif type(json_obj) == dict:
            if ignore_red:
                red_properties = [property for property in json_obj if type(json_obj[property]) in [unicode, str] and json_obj[property] == 'red']
                if len(red_properties) == 0:
                    for property in json_obj:
                        total += self._traverse(json_obj[property], ignore_red)
            else:
                for property in json_obj:
                    total += self._traverse(json_obj[property], ignore_red)

        return total

    def part_one(self):
        return self._traverse(self._json_document)

    def part_two(self):
        return self._traverse(self._json_document, ignore_red=True)


if __name__ == '__main__':
    p = Day12('input/2015/day12.txt')

    print '-----part one-----'
    print p.part_one()

    print '-----part two-----'
    print p.part_two()
