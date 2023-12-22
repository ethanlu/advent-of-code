from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.grid import Point2D
from adventofcode.common.util import show_dict_grid
from collections import deque
from typing import Dict, List, Tuple


directions = {'N': Point2D(0, -1), 'S': Point2D(0, 1), 'W': Point2D(-1, 0), 'E': Point2D(1, 0)}


class GardenPlot(object):
    def __init__(self, plot: Dict[Point2D, str], maxx: int, maxy: int):
        self._plot = plot
        self._maxx = maxx
        self._maxy = maxy

    @property
    def size(self) -> int:
        return self._maxx + 1

    def show(self, positions: List[Point2D]) -> None:
        grid = {(p.x, p.y): c for p, c in self._plot.items()}
        for p in positions:
            grid[(p.x, p.y)] = 'O'
        show_dict_grid(grid, self._maxx, self._maxy)

    def _position_steps(self, start: Point2D, steps: int) -> Dict[Point2D, int]:
        visited = {}
        remaining = deque([(0, [start])])
        while len(remaining):
            step, positions = remaining.pop()
            next_positions = []
            for p in positions:
                for delta in directions.values():
                    pp = p + delta
                    if pp in self._plot and self._plot[pp] != '#' and pp not in visited:
                        visited[pp] = step + 1
                        next_positions.append(pp)
            if len(next_positions) and (step + 1) < steps:
                remaining.append((step + 1, next_positions))
        return visited

    def step_coverage(self, start: Point2D, steps: int, distance_from_start=-1) -> List[Point2D]:
        visited = self._position_steps(start, steps)
        if steps % 2 == 1:
            return [p for p, s in visited.items() if s == steps or (s % 2 == 1 and (abs(p.x - start.x) + abs(p.y - start.y) > distance_from_start))]
        else:
            return [p for p, s in visited.items() if s == steps or (s % 2 == 0 and (abs(p.x - start.x) + abs(p.y - start.y) > distance_from_start))]


class Day21(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        start = None
        plot = {}
        maxx = 0
        maxy = 0
        for y, row in enumerate(self._load_input_as_lines()):
            for x, cell in enumerate(row):
                p = Point2D(x, y)
                maxx = max(maxx, p.x)
                maxy = max(maxy, p.y)
                plot[p] = cell
                if cell == 'S':
                    start = p
        self._gp = GardenPlot(plot, maxx, maxy)
        self._start = start

    def part_one(self):
        positions = self._gp.step_coverage(self._start, 64)
        self._gp.show(positions)
        return len(positions)

    def part_two(self):
        # solution based on : https://www.youtube.com/watch?v=9UOMZSL0JTg

        # plot has empty space horizontally and vertically from center, so step coverage forms a giant diamond when plot repeats endlessly
        # find how many times the plot will repeat in all cardinal directions
        steps = 26501365
        full_plot_radius = steps // self._gp.size - 1   # subtract 1 because starting point is in middle of plot and we need full plot
        rs = steps % full_plot_radius

        # plots not on the edge of the giant diamond will alternate in a checkboard pattern of full even and odd plots. based on number of full plots radius,
        # when full_plot_radius is odd, the # of odd full plots is (full_plot_radius + 1)^2 and even full plots is full_plot_radius^2
        total_even_full_plots = pow((full_plot_radius + 1) // 2 * 2, 2)
        total_odd_full_plots = pow(full_plot_radius //2 * 2 + 1, 2)

        # get how many positions are covered by even plots and odd plots
        full_even_positions = len(self._gp.step_coverage(self._start, self._gp.size * 2))
        full_odd_positions = len(self._gp.step_coverage(self._start, self._gp.size * 2 + 1))
        print(f"plots with even steps have {full_even_positions} positions covered and will repeat {total_even_full_plots} times")
        print(f"plots with odd steps have {full_odd_positions} positions covered and will repeat {total_odd_full_plots} times")

        fully_covered = total_even_full_plots * full_even_positions + total_odd_full_plots * full_odd_positions
        print(f"fully covered plots within the giant diamond is {fully_covered}")

        # the edges of the diamond form only partially cover the plot:
        # the tips of the diamond (N, S, W, E plots) are partial covers with the starting point at the center edges closest to the center of the giant diamond
        north_tip_partial = len(self._gp.step_coverage(Point2D(self._start.x, self._gp.size - 1), self._gp.size - 1))
        south_tip_partial = len(self._gp.step_coverage(Point2D(self._start.x, 0), self._gp.size - 1))
        west_tip_partial = len(self._gp.step_coverage(Point2D(self._gp.size - 1, self._start.y), self._gp.size - 1))
        east_tip_partial = len(self._gp.step_coverage(Point2D(0, self._start.y), self._gp.size - 1))

        tip_partials = north_tip_partial + south_tip_partial + west_tip_partial + east_tip_partial
        print(f"partial covered plots at the tips of the giant diamond is {tip_partials}")

        # the edges of the diamond are either a small triangle or a large triangle, but in 4 directions
        nw_small_partial = len(self._gp.step_coverage(Point2D(self._gp.size - 1, self._gp.size - 1), self._gp.size // 2 - 1))
        ne_small_partial = len(self._gp.step_coverage(Point2D(0, self._gp.size - 1), self._gp.size // 2 - 1))
        sw_small_partial = len(self._gp.step_coverage(Point2D(self._gp.size - 1, 0), self._gp.size // 2 - 1))
        se_small_partial = len(self._gp.step_coverage(Point2D(0, 0), self._gp.size // 2 - 1))

        small_partials = nw_small_partial + ne_small_partial + sw_small_partial + se_small_partial
        print(f"partial covered plots of small triangles at the edges at edges of the giant diamond is {small_partials}")

        nw_big_partial = len(self._gp.step_coverage(Point2D(self._gp.size - 1, self._gp.size - 1), self._gp.size * 3 // 2 - 1))
        ne_big_partial = len(self._gp.step_coverage(Point2D(0, self._gp.size - 1), self._gp.size * 3 // 2 - 1))
        sw_big_partial = len(self._gp.step_coverage(Point2D(self._gp.size - 1, 0), self._gp.size * 3 // 2 - 1))
        se_big_partial = len(self._gp.step_coverage(Point2D(0, 0), self._gp.size * 3 // 2 - 1))

        big_partials = nw_big_partial + ne_big_partial + sw_big_partial + se_big_partial
        print(f"partial covered plots of big triangles at the edges at edges of the giant diamond is {big_partials}")

        return fully_covered + tip_partials + (full_plot_radius + 1) * small_partials + full_plot_radius * big_partials
