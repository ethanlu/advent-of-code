from adventofcode import Solution

import re


class Day08(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)

        self._inputs = list(map(lambda l: l.strip(), self._load_input_as_lines()))

        self._state = 0
        self._code_character_count = 0
        self._in_memory_character_count = 0
        self._escape_character_count = 0

    def reset(self):
        self._state = 0
        self._code_character_count = 0
        self._in_memory_character_count = 0
        self._escape_character_count = 0

    def part_one(self):
        for s in self._inputs:
            #print(s)
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
                elif re.match(r'\d', c):
                    character = 'number'
                elif re.match(r'[a-z]', c):
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
        return self._code_character_count - self._in_memory_character_count

    def part_two(self):
        self.reset()
        for s in self._inputs:
            new_count = 2
            for c in s:
                new_count += 1
                if c in ('"', '\\'):
                    new_count += 1
            #print(str(new_count) + " - " + str(len(s)))
            self._code_character_count += new_count
            self._in_memory_character_count += len(s)
        return self._code_character_count - self._in_memory_character_count
