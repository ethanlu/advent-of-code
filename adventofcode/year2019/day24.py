from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.grid import Point2D
from functools import lru_cache
from typing import Dict, List


deltas = (Point2D(0, -1), Point2D(1, 0), Point2D(0, 1), Point2D(-1, 0))


class Eris(object):
    def __init__(self, input: List[str]):
        self._map = {Point2D(x, y): input[y][x] for x in range(len(input[0])) for y in range(len(input))}
        self._size = len(input)
        self._minute = 0

    def fingerprint(self) -> str:
        s = []
        for y in range(self._size):
            for x in range(self._size):
                s.append(self._map[Point2D(x, y)])
        return "".join(s)

    def biodiversity(self):
        biodiversity = 0
        tile = 1
        for y in range(self._size):
            for x in range(self._size):
                if self._map[Point2D(x, y)] == '#':
                    biodiversity += pow(2, tile - 1)
                tile += 1
        return biodiversity

    def step(self) -> None:
        next_map = {}
        for x in range(self._size):
            for y in range(self._size):
                position = Point2D(x, y)
                empty_spaces = 0
                adjacent_bugs = 0
                for delta in deltas:
                    neighbor = position + delta
                    if 0 <= neighbor.x < self._size and 0 <= neighbor.y < self._size:
                        match self._map[neighbor]:
                            case '.':
                                empty_spaces += 1
                            case '#':
                                adjacent_bugs += 1
                            case _:
                                raise Exception(f"Unexpected map tile ({self._map[neighbor]}) and position {neighbor}")
                    else:
                        empty_spaces += 1

                match self._map[position]:
                    case '.':
                        next_map[position] = '#' if 1 <= adjacent_bugs <= 2 else '.'
                    case '#':
                        next_map[position] = '#' if adjacent_bugs == 1 else '.'
                    case _:
                        raise Exception(f"Unexpected map tile ({self._map[position]}) and position {position}")
        self._map = next_map
        self._minute += 1

    def show(self) -> None:
        print(f"\nafter minute : {self._minute}")
        for y in range(self._size):
            s = []
            for x in range(self._size):
                s.append(self._map[Point2D(x, y)])
            print("".join(s))


class RecursiveEris(object):
    def __init__(self, input: List[str]):
        self._maps = {
            -1: {Point2D(x, y): '.' for x in range(len(input[0])) for y in range(len(input))},
            0: {Point2D(x, y): input[y][x] for x in range(len(input[0])) for y in range(len(input))},
            1: {Point2D(x, y): '.' for x in range(len(input[0])) for y in range(len(input))}
        }
        self._size = len(input)
        self._minute = 0

    @lru_cache(maxsize=None)
    def _get_outer_neighbor(self, layer: int, delta: Point2D) -> str:
        if layer not in self._maps.keys():
            # next layer does not exist yet, so treat it as empty space
            return '.'

        match delta.x, delta.y:
            case 0, -1:
                return self._maps[layer][Point2D(2, 1)]
            case 1, 0:
                return self._maps[layer][Point2D(3, 2)]
            case 0, 1:
                return self._maps[layer][Point2D(2, 3)]
            case -1, 0:
                return self._maps[layer][Point2D(1, 2)]
            case _:
                raise Exception(f"Invalid delta passed to get_outer_neighbor : {delta}")

    @lru_cache(maxsize=None)
    def _get_inner_neighbors(self, layer: int, delta: Point2D) -> List[str]:
        if layer not in self._maps.keys():
            # next layer does not exist yet, so treat it as empty space
            return ['.'] * self._size

        match delta.x, delta.y:
            case 0, -1:
                return [self._maps[layer][Point2D(x, self._size - 1)] for x in range(self._size)]
            case 1, 0:
                return [self._maps[layer][Point2D(0, y)] for y in range(self._size)]
            case 0, 1:
                return [self._maps[layer][Point2D(x, 0)] for x in range(self._size)]
            case -1, 0:
                return [self._maps[layer][Point2D(self._size - 1, y)] for y in range(self._size)]
            case _:
                raise Exception(f"Invalid delta passed to get_inner_neighbors : {delta}")

    def bugs(self) -> int:
        count = 0
        for layer, map in self._maps.items():
            count += len([c for c in map.values() if c == '#'])
        return count

    def step(self) -> None:
        # flush cache at the start of each step
        self._get_outer_neighbor.cache_clear()
        self._get_inner_neighbors.cache_clear()

        lowest_layer = min(self._maps.keys()) - 1
        highest_layer = max(self._maps.keys()) + 1

        self._maps[lowest_layer] = {Point2D(x, y): '.' for x in range(self._size) for y in range(self._size)}
        self._maps[highest_layer] = {Point2D(x, y): '.' for x in range(self._size) for y in range(self._size)}

        next_maps = {}
        for layer in range(lowest_layer, highest_layer + 1):
            next_maps[layer] = {}
            for x in range(self._size):
                for y in range(self._size):
                    position = Point2D(x, y)
                    if position.x == 2 and position.y == 2:
                        next_maps[layer][position] = '?'
                        continue

                    empty_spaces = 0
                    adjacent_bugs = 0
                    for delta in deltas:
                        neighbor = position + delta
                        if 0 <= neighbor.x < self._size and 0 <= neighbor.y < self._size:
                            if neighbor.x == 2 and neighbor.y == 2:
                                # neighbor is center cell, so get inner layer's outer edge
                                inner_neighbors = self._get_inner_neighbors(layer - 1, delta)
                                empty_spaces += sum([1 for c in inner_neighbors if c == '.'])
                                adjacent_bugs += sum([1 for c in inner_neighbors if c == '#'])
                            else:
                                match self._maps[layer][neighbor]:
                                    case '.':
                                        empty_spaces += 1
                                    case '#':
                                        adjacent_bugs += 1
                                    case _:
                                        raise Exception(f"Unexpected map tile ({self._maps[layer][neighbor]}) at layer {layer} and position {neighbor}")
                        else:
                            # neighbor is an edge....get outer layer's inner edge
                            c = self._get_outer_neighbor(layer + 1, delta)
                            empty_spaces += 1 if c == '.' else 0
                            adjacent_bugs += 1 if c == '#' else 0

                    match self._maps[layer][position]:
                        case '.':
                            next_maps[layer][position] = '#' if 1 <= adjacent_bugs <= 2 else '.'
                        case '#':
                            next_maps[layer][position] = '#' if adjacent_bugs == 1 else '.'
                        case _:
                            raise Exception(f"Unexpected map tile ({self._maps[layer][position]}) at layer {layer} and position {position}")

        # trim lowest and highest layer if it is all empty
        for edge_layer in (lowest_layer, highest_layer):
            if len([v for v in next_maps[edge_layer].values() if v == '#']) == 0:
                next_maps.pop(edge_layer)

        self._maps = next_maps
        self._minute += 1

    def show(self) -> None:
        print(f"\nafter minute : {self._minute}")
        if len(self._maps.keys()) < 20:
            for layer in range(min(self._maps.keys()), max(self._maps.keys()) + 1):
                print(f"\nlayer : {layer}")
                for y in range(self._size):
                    s = []
                    for x in range(self._size):
                        s.append(self._maps[layer][Point2D(x, y)])
                    print("".join(s))
        else:
            lowest = min(self._maps.keys())
            highest = max(self._maps.keys()) + 1
            for layer in range(lowest, lowest + 3):
                print(f"\nlayer : {layer}")
                for y in range(self._size):
                    s = []
                    for x in range(self._size):
                        s.append(self._maps[layer][Point2D(x, y)])
                    print("".join(s))
            print("\n\n........\n")
            for layer in range(highest - 3, highest):
                print(f"\nlayer : {layer}")
                for y in range(self._size):
                    s = []
                    for x in range(self._size):
                        s.append(self._maps[layer][Point2D(x, y)])
                    print("".join(s))


class Day24(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._input = self._load_input_as_lines()

    def part_one(self):
        e = Eris(self._input)

        cache: Dict[str, int] = {}
        biodiversity = 0
        while True:
            fingerprint = e.fingerprint()
            if fingerprint not in cache:
                cache[fingerprint] = e.biodiversity()
            else:
                biodiversity = cache[fingerprint]
                break
            e.step()

        e.show()
        return biodiversity

    def part_two(self):
        e = RecursiveEris(self._input)
        for _ in range(200):
            e.step()

        e.show()
        return e.bugs()
