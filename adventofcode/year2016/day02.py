from adventofcode import Solution


class KeyPad(object):
    keypad = ((1, 2, 3), (4, 5, 6), (7, 8, 9))

    def __init__(self):
        self._position = (1, 1)

    def key(self):
        return self.keypad[self._position[0]][self._position[1]]

    def u(self):
        if self._position[0] > 0:
            self._position = (self._position[0] - 1, self._position[1])

    def d(self):
        if self._position[0] < 2:
            self._position = (self._position[0] + 1, self._position[1])

    def r(self):
        if self._position[1] < 2:
            self._position = (self._position[0], self._position[1] + 1)

    def l(self):
        if self._position[1] > 0:
            self._position = (self._position[0], self._position[1] - 1)


class ComplexKeyPad(KeyPad):
    keypad = ((None, None, '1', None, None),
              (None, '2' , '3', '4' , None),
              ('5' , '6' , '7', '8' , '9' ),
              (None, 'A' , 'B', 'C' , None),
              (None, None, 'D', None, None))

    def __init__(self):
        self._position = (2, 0)

    def u(self):
        if self._position[0] > 0 and self.keypad[self._position[0] - 1][self._position[1]] is not None:
            self._position = (self._position[0] - 1, self._position[1])

    def d(self):
        if self._position[0] < 4 and self.keypad[self._position[0] + 1][self._position[1]] is not None:
            self._position = (self._position[0] + 1, self._position[1])

    def r(self):
        if self._position[1] < 4 and self.keypad[self._position[0]][self._position[1] + 1] is not None:
            self._position = (self._position[0], self._position[1] + 1)

    def l(self):
        if self._position[1] > 0 and self.keypad[self._position[0]][self._position[1] - 1] is not None:
            self._position = (self._position[0], self._position[1] - 1)


class Day02(Solution):
    def _init(self):
        self._input = self._load_input_as_lines()

    def part_one(self):
        # O(n) time complexity (n is length of movements in entire file)
        # O(c) space complexity
        k = KeyPad()

        sequence = []
        for line in self._input:
            for d in line:
                move = getattr(k, d.lower(), lambda: None)
                move()
            sequence.append(str(k.key()))

        return ''.join(sequence)

    def part_two(self):
        # O(n) time complexity (n is length of movements in entire file)
        # O(c) space complexity
        k = ComplexKeyPad()

        sequence = []
        for line in self._input:
            for d in line:
                move = getattr(k, d.lower(), lambda: None)
                move()
            sequence.append(str(k.key()))

        return ''.join(sequence)
