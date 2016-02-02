import re

class Day11(object):
    def __init__(self, input_file):
        with open(input_file) as f:
            self._s = map(lambda l: l.strip(), f.readlines())[0]

    def _is_valid(self, s):
        # must be 8 characters
        if re.match('^[a-z]{8,8}$', s) is None:
            return False

        # cannot have i, o, l characters
        if re.match('.*[iol]+.*', s):
            return False

        has_sequence = False
        character_pairs = set()
        for i in range(len(s)):
            # sequence
            if i+2 < len(s) and ord(s[i])+1 == ord(s[i+1]) and ord(s[i])+2 == ord(s[i+2]):
                has_sequence = True

            # character pair
            if i+1 < len(s) and s[i] == s[i+1]:
                character_pairs.add(s[i])

        return has_sequence and len(list(character_pairs)) > 1

    def _next_password(self, s):
        while True:
            next_s = list(s)

            carry = True
            for i in reversed(range(len(next_s))):
                if carry:
                    next_char = chr(ord(next_s[i]) + 1)
                    if ord(next_char) > ord('z'):
                        next_s[i] = 'a'
                        carry = True
                    else:
                        next_s[i] = next_char
                        carry = False

            s = "".join(next_s)
            yield s

    def part_one(self):
        for s in self._next_password(self._s):
            #print s + ' is invalid'
            if self._is_valid(s):
                break

        return s

    def part_two(self):
        valid_password = self.part_one()

        for s in self._next_password(valid_password):
            #print s + ' is invalid'
            if self._is_valid(s):
                break

        return s


if __name__ == '__main__':
    p = Day11('input/day11.txt')

    print '-----part one-----'
    print p.part_one()

    print '-----part two-----'
    print p.part_two()
