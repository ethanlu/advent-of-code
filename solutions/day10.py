class Day10(object):
    def __init__(self):
        pass

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

    def part_one(self, puzzle_input, n):
        start = puzzle_input
        for i in range(n):
            print '#' + i + ' : ' + len(start)
            end = self.look_say(start)
            start = end

        return len(end)

    def part_two(self):
        pass
