from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.grid import Point2D
from collections import deque
from typing import List, Set


directions = {
    'N': Point2D(0, -1),
    'E': Point2D(1, 0),
    'S': Point2D(0, 1),
    'W': Point2D(-1, 0)
}


class Region(object):
    def __init__(self, plant: str, plots: Set[Point2D]):
        self._plant = plant
        self._plots = set(plots)

    @property
    def plant(self) -> str:
        return self._plant

    @property
    def area(self) -> int:
        return len(self._plots)

    @property
    def perimeter(self) -> int:
        perimeter = 0
        for p in self._plots:
            for d in directions.values():
                if (p + d) not in self._plots:
                    perimeter += 1
        return perimeter

    @property
    def straight_perimeter(self) -> int:
        # identify the set of all plots and the edges that they have
        individual_plot_edges = set([])
        for plot in self._plots:
            for side, delta in directions.items():
                if (plot + delta) not in self._plots:
                    # plot edges identified by their x,y position and side of the edge
                    individual_plot_edges.add((plot, side))

        # with all individual plot edges identified, group the ones together if they form a longer straight edge
        straight_plot_edges = []
        while len(individual_plot_edges) > 0:
            remaining = deque([individual_plot_edges.pop()])
            straight_plot_edge = set([])
            while len(remaining) > 0:
                plot, side = remaining.pop()
                straight_plot_edge.add((plot, side))
                for direction, delta in directions.items():
                    match side, direction:
                        case ('N', 'E') | ('N', 'W') | ('S', 'E') | ('S', 'W') | ('W', 'N') | ('W', 'S') | ('E', 'N') | ('E', 'S'):
                            # only travel to neighboring plots that are in the direction perpendicular to the edge side
                            next_plot = plot + delta
                            if (next_plot, side) in individual_plot_edges and (next_plot, side) not in straight_plot_edge:
                                # neighboring plot is also an identified individual plot edge
                                remaining.append((next_plot, side))
                        case _:
                            continue
            straight_plot_edges.append(straight_plot_edge)
            individual_plot_edges.difference_update(straight_plot_edge)

        return len(straight_plot_edges)


class Garden(object):
    def __init__(self, data: List[str]):
        self._plots = {}
        self._regions = []
        self._maxy = len(data)
        self._maxx = len(data[0])

        for y, row in enumerate(data):
            for x, cell in enumerate(row):
                self._plots[Point2D(x, y)] = cell

        processed = set([])
        for plot, plant in self._plots.items():
            if plot not in processed:
                region_plots = self._region_floodfill(plot)
                self._regions.append(Region(plant, region_plots))
                processed.update(region_plots)

    @property
    def regions(self) -> List[Region]:
        return self._regions

    def _region_floodfill(self, plot: Point2D) -> Set[Point2D]:
        target_plant = self._plots[plot]
        target_plots = set([])
        remaining = deque([plot])
        while len(remaining) > 0:
            p = remaining.pop()
            target_plots.add(p)
            for d in directions.values():
                next_p = p + d
                if next_p in self._plots and self._plots[next_p] == target_plant and next_p not in target_plots:
                    remaining.append(next_p)
        return target_plots


class Day12(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._g = Garden(self._load_input_as_lines())

    def part_one(self):
        total = 0
        for r in self._g.regions:
            area = r.area
            perimeter = r.perimeter
            print(f"a region of {r.plant} plants with price {area} * {perimeter} = {area * perimeter}")
            total += area * perimeter
        return total

    def part_two(self):
        total = 0
        for r in self._g.regions:
            area = r.area
            perimeter = r.straight_perimeter
            print(f"a region of {r.plant} plants with price {area} * {perimeter} = {area * perimeter}")
            total += area * perimeter
        return total
