from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.graph.search import AStar, SearchState, S
from functools import cache
from typing import Any, List, Tuple


class Day10(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._machines = []
        for line in self._load_input_as_lines():
            t = line.split(' ')
            self._machines.append((
                t[0][1:-1],
                tuple([tuple([int(n) for n in s[1:-1].split(',')]) for s in t[1:-1]]),
                tuple((int(j) for j in t[-1][1:-1].split(',')))
            ))

    def part_one(self):
        class LightSearchState(SearchState):
            def __init__(self, lights: str, buttons: Tuple[Tuple[int]], cost: int):
                super().__init__(f"{lights}", 0, cost)
                self._lights = lights
                self._buttons = buttons

            def next_search_states(self) -> List[S]:
                states = []
                for wires in self._buttons:
                    next_lights = list(self._lights)
                    for wire in wires:
                        next_lights[wire] = '#' if next_lights[wire] == '.' else '.'
                    states.append(LightSearchState(''.join(next_lights), self._buttons, self._cost + 1))
                return states

        total = 0
        for i, (target_lights, buttons, joltages) in enumerate(self._machines):
            print(f"machine {i} : target lights {target_lights} with {buttons}")
            astar = AStar(
                LightSearchState('.'*len(target_lights), buttons, 0),
                LightSearchState(target_lights, buttons, 0)
            )
            best = astar.find_path()
            print(f"\tbest found with {best.cost} presses")
            total += best.cost
        return total

    def part_two(self):
        # solution based on : https://www.reddit.com/r/adventofcode/comments/1pk87hl/2025_day_10_part_2_bifurcate_your_way_to_victory/
        @cache
        def get_reduction_groups(target_lights: str, buttons: Tuple[Tuple[int]]) -> Tuple[Tuple[Any]]:
            valid = []
            digits = len(buttons)
            for i in range(2 ** digits):
                lights = ['.'] * len(target_lights)
                on_buttons = set()
                for index, value in enumerate(list(f"{i:0{digits}b}")):
                    if value == '1':
                        on_buttons.add(index)
                        for wire in buttons[index]:
                            lights[wire] = '#' if lights[wire] == '.' else '.'
                if "".join(lights) == target_lights:
                    valid.append(tuple([buttons[button_index] for button_index in on_buttons]))
            return tuple(valid)

        @cache
        def reduce_solve(joltages: Tuple[int], buttons: Tuple[Tuple[int]]) -> int:
            if sum(joltages) == 0:
                return 0
            best = 1000000000
            for reduction_group in get_reduction_groups(''.join(['.' if j % 2 == 0 else '#' for j in joltages]), buttons):
                next_joltages = list(joltages)
                for button in reduction_group:
                    for wire in button:
                        next_joltages[wire] -= 1
                if any([j < 0 or j % 2 != 0 for j in next_joltages]):
                    continue
                # reduce joltages further by continously dividing by 2 if they are all even
                next_joltages = [j // 2 for j in next_joltages]
                # print(f"joltage {joltages} becomes new goal : {next_joltages} from pattern: {reduction_group} - {len(reduction_group)}")
                best = min(best, len(reduction_group) + (2 * reduce_solve(tuple(next_joltages), buttons)))
            return best

        total = 0
        for i, (_, buttons, target_joltages) in enumerate(self._machines):
            print(f"machine {i} : target joltages {target_joltages}")
            best = reduce_solve(target_joltages, buttons)
            print(f"\t{best} presses")
            total += best
        return total
