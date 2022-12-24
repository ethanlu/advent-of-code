from adventofcode import Solution


class Day06(Solution):
    def _init(self):
        self._input = self._load_input_as_lines()

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
