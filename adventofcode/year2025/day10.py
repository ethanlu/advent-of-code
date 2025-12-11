from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.graph.search import AStar, SearchState, S
from typing import List, Tuple


class FewestButtonPressSearchState(SearchState):
    def __init__(self, lights: str, button_sequences: List[List[int]], cost: int):
        super().__init__(f"{lights}", 0, cost)
        self._lights = lights
        self._button_sequences = button_sequences

    def next_search_states(self) -> List[S]:
        states = []
        for button_sequence in self._button_sequences:
            next_lights = list(self._lights)
            for button in button_sequence:
                next_lights[button] = '#' if next_lights[button] == '.' else '.'
            states.append(FewestButtonPressSearchState(''.join(next_lights), self._button_sequences, self._cost + 1))
        return states


class Day10(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._machines = []
        for line in self._load_input_as_lines():
            t = line.split(' ')
            self._machines.append((
                t[0][1:-1],
                [[int(n) for n in s[1:-1].split(',')] for s in t[1:-1]],
                tuple((int(j) for j in t[-1][1:-1].split(',')))
            ))

    def part_one(self):
        total = 0
        for i, (target_lights, button_sequences, joltages) in enumerate(self._machines):
            print(f"machine {i} : target lights {target_lights} with {button_sequences}")
            astar = AStar(
                FewestButtonPressSearchState('.'*len(target_lights), button_sequences, 0),
                FewestButtonPressSearchState(target_lights, button_sequences, 0)
            )
            best = astar.find_path()
            print(f"\tbest found with {best.cost} presses")
            total += best.cost
        return total

    def part_two(self):
        pass
