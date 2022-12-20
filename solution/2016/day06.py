class Day06(object):
    def __init__(self, input_file):
        with open(input_file) as f:
            self._input = f.readlines()

    def _build_character_counts(self):
        characters = [{} for i in range(len(self._input[0]))]
        for message in self._input:
            for index, char in enumerate(message):
                if char not in characters[index]:
                    characters[index][char] = 0
                characters[index][char] += 1

        return characters

    def part_one(self):
        # O(n) time complexity (n is number of messages in input)
        # O(m) space complexity (m is number of unique chars in messages)
        message = []
        for char_position in self._build_character_counts():
            largest = 0
            most_frequent = '?'
            for char, total in char_position.items():
                if largest < total:
                    largest = total
                    most_frequent = char
            message.append(most_frequent)

        return ''.join(message)

    def part_two(self):
        # O(n) time complexity (n is number of messages in input)
        # O(m) space complexity (m is number of unique chars in messages)
        message = []
        for char_position in self._build_character_counts():
            smallest = len(self._input) * len(self._input[0])
            least_frequent = '?'
            for char, total in char_position.items():
                if smallest > total:
                    smallest = total
                    least_frequent = char
            message.append(least_frequent)

        return ''.join(message)

if __name__ == '__main__':
    p = Day06('../../input/2016/day06.txt')

    print('-----part one-----')
    print(p.part_one())

    print('-----part two-----')
    print(p.part_two())
