import re

class Day08(object):
    def __init__(self, input_file):
        with open(input_file) as f:
            self._inputs = map(lambda l: l.strip(), f.readlines())

        self._state = 0
        self._code_character_count = 0
        self._in_memory_character_count = 0

    def reset(self):
        self._state = 0
        self._code_character_count = 0
        self._in_memory_character_count = 0

    def part_one(self):
        for s in self._inputs:
            #print s
            self._code_character_count += len(s)
            self._state = 0

            # 0 : start state
            # 1 : string state
            # 2 : escape state
            # 3 : hexadecimal state
            hex_read = 0
            for c in s:
                if c == '\\':
                    character = 'escape'
                elif c == '"':
                    character = 'double-quote'
                elif c == 'x':
                    character = 'x'
                elif re.match('\d', c):
                    character = 'number'
                elif re.match('[a-z]', c):
                    character = 'character'
                else:
                    raise Exception('unknown character ' + str(c))

                if self._state == 0:
                    # regular character state : no increment, should only change to string state
                    if character in ['double-quote']:
                        self._state = 1
                    else:
                        raise Exception('inconsistent state 0')
                elif self._state == 1:
                    # string state : increment in-memory character count when character is not escape or double quote
                    if character in ['character','number','x']:
                        self._in_memory_character_count += 1
                    elif character in ['double-quote']:
                        self._state = 0
                    elif character in ['escape']:
                        self._state = 2
                    else:
                        raise Exception('inconsistent state 1')
                elif self._state == 2:
                    # escape state : increment in-memory character count when character is not escape or double quote
                    if character in ['x']:
                        self._state = 3
                        hex_read = 0
                    elif character in ['double-quote', 'escape']:
                        self._in_memory_character_count += 1
                        self._state = 1
                    else:
                        raise Exception('inconsistent state 2')
                elif self._state == 3:
                    # hex state : increment in-memory character count when leaving this state
                    if character in ['number', 'character']:
                        self._state = 3
                        hex_read += 1

                        if hex_read >= 2:
                            self._state = 1
                            self._in_memory_character_count += 1
                    else:
                        raise Exception('inconsistent state 3')
                else:
                    raise Exception('invalid state : ' + str(self._state))
        return (self._code_character_count - self._in_memory_character_count)

    def part_two(self):
        for s in self._inputs:
            #print s
            self._code_character_count += len(re.escape(s)) + 2
            self._in_memory_character_count += len(s)
        return (self._code_character_count - self._in_memory_character_count)


if __name__ == '__main__':
    p = Day08('input/day08.txt')

    print '-----part one-----'
    print p.part_one()

    print '-----part two-----'
    p.reset()
    print p.part_two()
