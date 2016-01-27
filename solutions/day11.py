import re

class Day11(object):
    def __init__(self):
        pass

    def validate(self, s):
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

    def increment(self, s):
        next_s = list(s)

        carry = True
        for i in reversed(range(len(next_s))):
            if carry:
                next_char = chr(ord(next_s[i])+1)
                if ord(next_char) > ord('z'):
                    next_s[i] = 'a'
                    carry = True
                else:
                    next_s[i] = next_char
                    carry = False

        return "".join(next_s)

    def part_one(self, s):
        print 'given : ' + s
        while True:
            s = self.increment(s)

            if self.validate(s):
                print s + ' is good'
                break
            else:
                print s + ' is bad'

        return s

    def part_two(self):
        pass
