from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.year2019.day09 import IntCodeCPUComplete
from typing import List


class QuitException(Exception):
    pass


class ScoutBot(object):
    def __init__(self, program: List[int]):
        self._cpu = IntCodeCPUComplete(program)

    def _validate(self, s: str) -> str:
        match s.split(' ')[0]:
            case 'north' | 'south' | 'east' | 'west':
                return s
            case 'take':
                return s
            case 'drop':
                return s
            case 'inv':
                return s
            case 'code':
                return "".join(s.split(' ')[1:])
            case 'quit':
                raise QuitException("quit")
            case _:
                raise Exception(f"Invalid command : {s}")

    def run(self) -> None:
        output = []
        while not self._cpu.halted:
            self._cpu.run()

            if self._cpu.has_output:
                output.append(chr(self._cpu.get_output()))
            else:
                while True:
                    print("".join(output))
                    try:
                        command = self._validate(input("command: ").lower().strip())
                        break
                    except QuitException:
                        return
                    except:
                        print("Invalid command! Try again...")
                for c in command:
                    self._cpu.add_input(ord(c))
                self._cpu.add_input(10)
                output = []


class Day25(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._input = [int(i) for i in self._load_input_as_string().split(',')]

    def part_one(self):
        sb = ScoutBot(self._input)
        sb.run()
        return "ᕕ( ᐛ )ᕗ"

    def part_two(self):
        return "ᕕ( ᐛ )ᕗ"