from __future__ import annotations
from adventofcode.common import Solution
from typing import Dict, List, Set


class ImageTile(object):
    def __init__(self, id: int, data: List[str]):
        self._id = id
        self._data = [[c for c in data[y]] for y in range(len(data))]
        self._size = len(data)

    @property
    def id(self) -> int:
        return self._id

    @property
    def top(self) -> str:
        return "".join(self._data[0])

    @property
    def bottom(self) -> str:
        return "".join(self._data[self._size - 1])

    @property
    def left(self) -> str:
        return "".join((self._data[y][0] for y in range(self._size)))

    @property
    def right(self) -> str:
        return "".join((self._data[y][self._size - 1] for y in range(self._size)))

    def flip_x(self) -> None:
        self._data = [list(reversed(row)) for row in self._data]

    def flip_y(self) -> None:
        self._data = list(reversed(self._data))

    def rotate_right(self) -> None:
        data = [["?" for x in range(self._size)] for y in range(self._size)]
        for y in range(self._size):
            for x in range(self._size):
                data[y][x] = self._data[self._size - 1 - x][y]
        self._data = data

    def rotate_left(self) -> None:
        data = [["?" for x in range(self._size)] for y in range(self._size)]
        for y in range(self._size):
            for x in range(self._size):
                data[y][x] = self._data[x][self._size - 1 - y]
        self._data = data

    def show(self) -> None:
        for row in self._data:
            print("".join(row))


class ImageArray(object):
    def __init__(self, tiles: Dict[int, ImageTile]):
        self._tiles = tiles
        self._size = len(tiles)
        self._corners: List[ImageTile] = []
        self._side_orientation_signatures: Dict[id, Dict[str, Set[str]]] = {}

    @property
    def corners(self) -> List[ImageTile]:
        return self._corners

    def _get_side_orientations(self, side: str, tile: ImageTile) -> Set[str]:
        if tile.id in self._side_orientation_signatures and side in self._side_orientation_signatures[tile.id]:
            return self._side_orientation_signatures[tile.id][side]

        if tile.id not in self._side_orientation_signatures:
            self._side_orientation_signatures[tile.id] = {}
        if side not in self._side_orientation_signatures[tile.id]:
            self._side_orientation_signatures[tile.id][side] = set([])

        # get the side from all 4 rotations
        for _ in range(4):
            self._side_orientation_signatures[tile.id][side].add(getattr(tile, side))
            tile.rotate_right()

        # get the side from all 4 rotations after flipping on x
        tile.flip_x()
        for _ in range(4):
            self._side_orientation_signatures[tile.id][side].add(getattr(tile, side))
            tile.rotate_left()

        # get the side from all 4 rotations after flipping on y
        tile.flip_x()
        tile.flip_y()
        for _ in range(4):
            self._side_orientation_signatures[tile.id][side].add(getattr(tile, side))
            tile.rotate_right()

        return self._side_orientation_signatures[tile.id][side]

    def solve(self) -> None:
        corners = []
        # each corner has 2 unique sides that must match and the other 2 sides should not match at all
        candidates = set(self._tiles.keys()).difference(set((c.id for c in corners)))
        for candidate in candidates:
            neighbor_matches = set([])
            for candidate_side, neighbor_side in (('top', 'bottom'), ('right', 'left'), ('bottom', 'top'), ('left', 'right')):
                candidate_sides = self._get_side_orientations(candidate_side, self._tiles[candidate])
                for neighbor in (neighbor for neighbor in candidates if neighbor != candidate):
                    neighbor_sides = self._get_side_orientations(neighbor_side, self._tiles[neighbor])
                    if len(candidate_sides.intersection(neighbor_sides)) != 0:
                        neighbor_matches.add(neighbor)

            if len(neighbor_matches) == 2:
                self._corners.append(self._tiles[candidate])


class Day20(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._tiles = {}

        id = 0
        data = []
        for line in self._load_input_as_lines():
            if not line:
                self._tiles[id] = ImageTile(id, data)
                id = 0
                data = []
                continue

            if line.startswith("Tile"):
                id = int(line.replace("Tile ", "").replace(":", "").strip())
            else:
                data.append(line)
        self._tiles[id] = ImageTile(id, data)

    def part_one(self):
        ia = ImageArray(self._tiles)
        ia.solve()

        total = 1
        for corner in ia.corners:
            print(f"tile {corner.id} is a corner")
            total *= corner.id

        return total

    def part_two(self):
        return "ᕕ( ᐛ )ᕗ"