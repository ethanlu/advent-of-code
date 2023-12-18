from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.grid import Point2D
from adventofcode.common.graph.search import AStar, SearchState, S, P
from adventofcode.common.util import show_dict_grid
from typing import Dict, List


directions = {'N': Point2D(0, -1), 'S': Point2D(0, 1), 'W': Point2D(-1, 0), 'E': Point2D(1, 0)}
facing = {'*': '*', '@': '@', 'N': '^', 'S': 'v', 'W': '<', 'E': '>'}


class TrafficMap(object):
    def __init__(self, data: List[List[str]]):
        self._maxy = len(data)
        self._maxx = len(data[0])
        self._grid = {}
        for y, row in enumerate(data):
            for x, cell in enumerate(row):
                self._grid[Point2D(x, y)] = cell

    @property
    def maxx(self) -> int:
        return self._maxx

    @property
    def maxy(self) -> int:
        return self._maxy

    def contains(self, p: Point2D) -> bool:
        return p in self._grid

    def heat_loss_at(self, p: Point2D) -> int:
        return int(self._grid[p])

    def show(self, path: P) -> None:
        breadcrumb = {s.position: facing[s.direction]  for s in path.search_states}
        show_dict_grid(
            {(p.x, p.y): breadcrumb[p] if p in breadcrumb else v for p, v in self._grid.items()},
            self.maxx,
            self.maxy
        )


class CrucibleMinimumHeatLossSearchState(SearchState):
    def __init__(self, traffic_map: TrafficMap, position: Point2D, direction: str, steps: int, min_steps: int, max_steps: int, cost: int):
        if direction != '@':    # all positions besides the start/end position needs position + steps + direction as key for search
            super().__init__(f"{position}:{steps}:{direction}", 0, cost)
        else:   # end position just need position to match
            super().__init__(f"{position}", 0, cost)
        self._traffic_map = traffic_map
        self._position = position
        self._direction = direction
        self._steps = steps
        self._min_steps = min_steps
        self._max_steps = max_steps

    def __str__(self) -> str:
        return f"{self._position}[{self._traffic_map.heat_loss_at(self._position)}][{self.cost}]"

    @property
    def position(self) -> Point2D:
        return self._position

    @property
    def direction(self) -> str:
        return self._direction

    def _allowed_directions(self) -> Dict[str, Point2D]:
        # based on state, next states can continue in same direction and change directions
        allowed_directions = []
        if self._direction != '*':
            # allow turning only if steps taken meets min steps requirement
            if self._steps >= self._min_steps:
                match self._direction:
                    case 'N' | 'S':
                        allowed_directions.append('W')
                        allowed_directions.append('E')
                    case 'W' | 'E':
                        allowed_directions.append('N')
                        allowed_directions.append('S')
                    case _:
                        raise Exception(f"Unexpected facing direction : {self._direction}")

            # allow going straight if steps take meets max steps requirement
            if self._steps < self._max_steps:
                allowed_directions.append(self._direction)
        else:   # starting point has no direction, but can only go in 2 directions
            allowed_directions.append('S')
            allowed_directions.append('E')
        return {d: self._position + directions[d] for d in allowed_directions if self._traffic_map.contains(self._position + directions[d])}

    def _is_valid_end_position(self, position: Point2D, direction: str) -> bool:
        return position.x == (self._traffic_map.maxx - 1) and (position.y == self._traffic_map.maxy - 1)

    def next_search_states(self) -> List[S]:
        states = []
        for next_direction, next_position in self._allowed_directions().items():
            if self._is_valid_end_position(next_position, next_direction):
                # next position is valid end position, so force steps and direction to match end state
                states.append(self.__class__(
                    self._traffic_map, next_position,
                    '@', 0,
                    self._min_steps, self._max_steps,
                    self._cost + self._traffic_map.heat_loss_at(next_position)
                ))
            else:
                # next position is not valid end position, so need to ensure steps and direction are used for search states
                states.append(self.__class__(
                    self._traffic_map,
                    next_position, next_direction,
                    1 if next_direction != self._direction else self._steps + 1,
                    self._min_steps, self._max_steps,
                    self._cost + self._traffic_map.heat_loss_at(next_position)
                ))
        return states


class UltraCrucibleMinimumHeatLossSearchState(CrucibleMinimumHeatLossSearchState):
    def __init__(self, traffic_map: TrafficMap, position: Point2D, direction: str, steps: int, min_steps: int, max_steps: int, cost: int):
        super().__init__(traffic_map, position, direction, steps, min_steps, max_steps, cost)

    def _is_valid_end_position(self, position: Point2D, direction: str) -> bool:
        # must be at end position and with minimum steps reached in order to be able to stop
        return super()._is_valid_end_position(position, direction) and self._direction == direction and (self._steps + 1) >= self._min_steps


class Day17(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._traffic_map = TrafficMap([list(l) for l in self._load_input_as_lines()])

    def part_one(self):
        ss = CrucibleMinimumHeatLossSearchState(self._traffic_map, Point2D(0, 0), '*', 0, 0, 3, 0)
        es = CrucibleMinimumHeatLossSearchState(self._traffic_map, Point2D(self._traffic_map.maxx - 1, self._traffic_map.maxy - 1), '@', 0, 0, 3, 0)
        astar = AStar(ss, es)
        astar.verbose(True, 10000)
        best = astar.find_path()
        self._traffic_map.show(best)
        return best.cost

    def part_two(self):
        ss = UltraCrucibleMinimumHeatLossSearchState(self._traffic_map, Point2D(0, 0), '*', 0, 4, 10, 0)
        es = UltraCrucibleMinimumHeatLossSearchState(self._traffic_map, Point2D(self._traffic_map.maxx - 1, self._traffic_map.maxy - 1), '@', 0, 4, 10, 0)
        astar = AStar(ss, es)
        astar.verbose(True, 100000)
        best = astar.find_path()
        self._traffic_map.show(best)
        return best.cost