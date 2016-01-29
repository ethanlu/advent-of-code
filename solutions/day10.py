class Day10(object):
    def __init__(self, input_file):
        with open(input_file) as f:
            self._start = map(lambda l: l.strip(), f.readlines())[0]

    def look_say(self, input):
        look_say = []

        for n in input:
            if len(look_say) == 0:
                look_say.append((1, n))
            else:
                (count_n, current_n) = look_say.pop()

                if current_n == n:
                    count_n += 1
                    look_say.append((count_n, current_n))
                else:
                    look_say.append((count_n, current_n))
                    look_say.append((1, n))

        return "".join(["{c}{n}".format(c=c, n=n) for (c, n) in look_say])

    def _look_say(self, number):
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
            return self._get_next_look_say(self._look_say(number), iteration - 1)
        else:
            return self._look_say(number)

    def part_one(self,):
        return len(self._get_next_look_say(self._start, 40))

    def part_two(self):
        return len(self._get_next_look_say(self._start, 50))

if __name__ == '__main__':
    p = Day10('input/day10.txt')

    print '-----part one-----'
    print p.part_one()

    print '-----part two-----'
    print p.part_two()

