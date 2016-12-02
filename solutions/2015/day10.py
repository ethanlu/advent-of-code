class Day10(object):
    def __init__(self, input_file):
        with open(input_file) as f:
            self._start = map(lambda l: l.strip(), f.readlines())[0]

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

if __name__ == '__main__':
    p = Day10('../../input/2015/day10.txt')

    print '-----part one-----'
    print p.part_one()

    print '-----part two-----'
    print p.part_two()

