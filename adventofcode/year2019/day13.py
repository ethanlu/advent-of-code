from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.grid import Point2D
from adventofcode.year2019.day09 import IntCodeCPUComplete
from functools import reduce
from typing import List

import sys


class ArcadeCabinet(object):
    _tile_map = (' ', '#', '=', '-', '@')

    def __init__(self, program: List[int], free: bool = False, verbose: bool = False):
        self._cpu = IntCodeCPUComplete(program, verbose)
        self._screen = {}
        self._score = 0

        if free:
            self._cpu.write_memory(0, 2)

    @property
    def screen(self):
        return self._screen

    @property
    def score(self) -> int:
        return self._score

    def run(self) -> None:
        paddle_target_x = None
        paddle = None
        ball = None
        last_score = 0
        while not self._cpu.halted:
            if paddle is not None and paddle_target_x is not None:
                self._cpu.clear_input()
                self._cpu.add_input(max(min(paddle_target_x - paddle.x, 1), -1))
            else:
                self._cpu.add_input(0)

            output = []
            while len(output) < 3:
                self._cpu.run()
                output.append(self._cpu.get_output())

            if output[0] == -1 and output[1] == 0:
                # score output
                self._score = output[2]
                if self._score == 0 or (self._score // last_score) > 0:
                    self.show()
                    last_score += 1000
            else:
                # screen output
                x, y, tile = output
                p = Point2D(x, y)

                match tile:
                    case 0 | 1 | 2:
                        self._screen[p] = tile
                    case 3:
                        paddle = p
                        self._screen[p] = tile
                    case 4:
                        if ball is not None:
                            delta = p - ball
                            if delta.y > 0 and paddle is not None:
                                # ball is moving towards paddle, calculate the x position that it would be where its y position is the same as the paddle, and move the paddle to there
                                paddle_target_x = ball.x + delta.x * ((paddle.y - p.y) // delta.y)
                            else:
                                # ball is moving away from paddle, move paddle towards x position of ball
                                paddle_target_x = p.x
                        ball = p
                        self._screen[p] = tile
                    case _:
                        pass

    def show(self) -> None:
        minx = reduce(lambda acc, p: acc if acc < p.x else p.x, self._screen.keys(), sys.maxsize)
        maxx = reduce(lambda acc, p: acc if acc > p.x else p.x, self._screen.keys(), -sys.maxsize)
        miny = reduce(lambda acc, p: acc if acc < p.y else p.y, self._screen.keys(), sys.maxsize)
        maxy = reduce(lambda acc, p: acc if acc > p.y else p.y, self._screen.keys(), -sys.maxsize)
        for y in range(miny, maxy + 1):
            row = []
            for x in range(minx, maxx + 1):
                p = Point2D(x, y)
                if p in self._screen.keys():
                    row.append(self._tile_map[self._screen[p]])
            print("".join(row))
        print(f"score: {self._score}")



class Day13(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._input = [int(i) for i in self._load_input_as_string().split(',')]

    def part_one(self):
        ac = ArcadeCabinet(self._input, False, False)
        ac.run()
        ac.show()
        return sum((1 for (p, tile) in ac.screen.items() if tile == 2))

    def part_two(self):
        ac = ArcadeCabinet(self._input, True, False)
        ac.run()
        ac.show()
        return ac.score
