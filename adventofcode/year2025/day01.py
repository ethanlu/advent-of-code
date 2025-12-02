from __future__ import annotations
from adventofcode.common import Solution


class SafeDial(object):
    def __init__(self, dial_size: int, start: int):
        self._position = start
        self._dial_size = dial_size

    @property
    def position(self) -> int:
        return self._position

    def rotate(self, direction: str, clicks: int) -> int:
        crossed_zero = 0
        match direction:
            case 'L':
                if self._position != 0:
                    crossed_zero = (self._dial_size - self._position + clicks) // self._dial_size
                else:
                    crossed_zero = (self._position + clicks) // self._dial_size
                self._position = (self._position - clicks) % self._dial_size
            case 'R':
                crossed_zero = (self._position + clicks) // self._dial_size
                self._position = (self._position + clicks) % self._dial_size

        if self._position == 0 and crossed_zero > 0:
            # if position is at zero, then crossed_zero might incorrectly count being at zero to also be crossing zero, so subtract 1 if it has at least 1 count
            crossed_zero -= 1

        return crossed_zero


class Day01(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._input = [(line[0], int(line[1:])) for line in self._load_input_as_lines()]

    def part_one(self):
        sd = SafeDial(100, 50)
        count = 0
        print(f"the dial starts by pointing at {sd.position}")
        for direction, clicks in self._input:
            sd.rotate(direction, clicks)
            if sd.position == 0:
                count += 1
            print(f"{count:05} : the dial is rotated {direction}{str(clicks)} to point at {sd.position}")
        return count

    def part_two(self):
        sd = SafeDial(100, 50)
        count = 0
        print(f"the dial starts by pointing at {sd.position}")
        for direction, clicks in self._input:
            crossed_zero = sd.rotate(direction, clicks)
            count += crossed_zero
            if sd.position == 0:
                count += 1
            print(f"{count:05} : the dial is rotated {direction}{str(clicks)} to point at {sd.position} and crossed zero {crossed_zero} times")
        return count
