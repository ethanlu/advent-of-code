from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.grid import Point2D
from adventofcode.common.graph.search import AStar, SearchState, S
from adventofcode.common.util import show_dict_grid
from typing import Iterable, List, Tuple


directions = {
    '^': Point2D(0, -1),
    '>': Point2D(1, 0),
    'v': Point2D(0, 1),
    '<': Point2D(-1, 0)
}


def valid_directions(facing: str) -> Iterable[Tuple[str, Point2D]]:
    match facing:
        case '^':
            return ((k, v) for k, v in directions.items() if k in ('^', '>', '<'))
        case '>':
            return ((k, v) for k, v in directions.items() if k in ('>', 'v', '^'))
        case 'v':
            return ((k, v) for k, v in directions.items() if k in ('v', '<', '>'))
        case '<':
            return ((k, v) for k, v in directions.items() if k in ('<', '^', 'v'))
        case _:
            raise Exception(f"unexpected facing direction : {facing}")


class MinimumTurnSearchState(SearchState):
    def __init__(self, maze: Maze, position: Point2D, facing: str, cost: int):
        self._maze = maze
        self._position = position
        self._facing = facing
        if self._maze.end == self._position:
            # end position only uses position as fingerprint
            super().__init__(f"{position}", 0, cost)
        else:
            super().__init__(f"{position}{facing}", 0, cost)

    @property
    def position(self) -> Point2D:
        return self._position

    @property
    def facing(self) -> str:
        return self._facing

    def next_search_states(self) -> List[S]:
        states = []
        for facing, delta in valid_directions(self.facing):
            next_p = self._position + delta
            if not self._maze.is_wall(next_p):
                states.append(self.__class__(self._maze, next_p, facing, self._cost + (1 if facing == self.facing else 1001)))
        return states


class Maze(object):
    def __init__(self, data: List[str]):
        self._maxx = len(data[0])
        self._maxy = len(data)
        self._maze = {}
        self._facing = '>'
        self._start = None
        self._end = None

        for y, row, in enumerate(data):
            for x, cell in enumerate(row):
                p = Point2D(x, y)
                match cell:
                    case '#' | '.':
                        self._maze[p] = cell
                    case 'S':
                        self._maze[p] = '.'
                        self._start = p
                    case 'E':
                        self._maze[p] = '.'
                        self._end = p

    @property
    def start(self) -> Point2D:
        return self._start

    @property
    def end(self) -> Point2D:
        return self._end

    @property
    def facing(self) -> str:
        return self._facing

    def show(self, breadcrumb: List[Tuple[Point2D, str]]) -> None:
        grid = {}
        for p, c in self._maze.items():
            grid[(p.x, p.y)] = c
        for p, v in breadcrumb:
            grid[(p.x, p.y)] = v
        grid[(self._start.x, self._start.y)] = 'S'
        grid[(self._end.x, self._end.y)] = 'E'
        show_dict_grid(grid, self._maxx, self._maxy)

    def is_wall(self, position: Point2D) -> bool:
        return self._maze[position] == '#'


class Day16(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._maze = Maze(list(self._load_input_as_lines()))

    def part_one(self):
        ss = MinimumTurnSearchState(self._maze, self._maze.start, self._maze.facing, 0)
        es = MinimumTurnSearchState(self._maze, self._maze.end, '*', 0)
        astar = AStar(ss, es)
        astar.verbose(True, 10000)
        best = astar.find_path()
        self._maze.show([(s.position, s.facing) for s in best.search_states])
        return best.cost

    def part_two(self):
        ss = MinimumTurnSearchState(self._maze, self._maze.start, self._maze.facing, 0)
        es = MinimumTurnSearchState(self._maze, self._maze.end, '*', 0)
        astar = AStar(ss, es)
        astar.verbose(True, 10000)
        best_spots = set([])
        for shortest_path in astar.find_all_paths():
            for s in shortest_path.search_states:
                best_spots.add(s.position)

        self._maze.show([(p, 'O') for p in best_spots])
        return len(best_spots)
