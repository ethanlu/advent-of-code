from adventofcode import Solution


class Day10(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)

        self._start = list(map(lambda l: l.strip(), self._load_input_as_lines()))[0]

    def _do_look_say(self, number):
        response = ''

        i = 0
        current_digit_count = 1
        current_digit = number[i]
        while i < len(number) - 1:
            i += 1
            if number[i] == current_digit:
                # current digit is repeating, so increment counters
                current_digit_count += 1
            else:
                # current digit changed, so write it out and keep track of new
                response += str(current_digit_count) + current_digit
                current_digit_count = 1
                current_digit = number[i]
        response += str(current_digit_count) + current_digit

        return response

    def _get_next_look_say(self, number, iteration):
        if iteration > 1:
            return self._get_next_look_say(self._do_look_say(number), iteration - 1)
        else:
            return self._do_look_say(number)

    def part_one(self,):
        return len(self._get_next_look_say(self._start, 40))

    def part_two(self):
        return len(self._get_next_look_say(self._start, 50))
