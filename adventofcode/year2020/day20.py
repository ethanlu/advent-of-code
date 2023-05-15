from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.grid import Point2D
from collections import deque
from typing import Dict, List, Optional, Set, Union

import math


class ImageTile(object):
    def __init__(self, id: int, data: List[List[str]]):
        self._id = id
        self._data = data.copy()
        self._size = len(data)

    @property
    def id(self) -> int:
        return self._id

    @property
    def size(self) -> int:
        return self._size

    @property
    def data(self) -> List[List[str]]:
        return self._data

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

    def flip(self) -> List[List[str]]:
        return [list(reversed(row)) for row in self._data]

    def rotate(self) -> List[List[str]]:
        data = [["?" for x in range(self._size)] for y in range(self._size)]
        for y in range(self._size):
            for x in range(self._size):
                data[y][x] = self._data[self._size - 1 - x][y]
        return [row for row in data]

    def row(self, row: int) -> List[str]:
        return self._data[row]

    def show(self) -> None:
        for row in self._data:
            print("".join(row))


class ImageArray(object):
    def __init__(self, tiles: Dict[int, ImageTile]):
        self._size = int(math.sqrt(len(tiles)))
        self._tile_size = list(tiles.values())[0].size
        self._image: List[List[Optional[ImageTile]]] = [[None for x in range(self._size)] for y in range(self._size)]

        # store all possible orientations of each tile for future reference
        self._tiles: Dict[int, List[ImageTile]] = {}

        # store a lookup table of side signatures for each tile's side (and all orientations)
        self._tile_side_signatures: Dict[id, Dict[str, Set[str]]] = {}

        for id, tile in tiles.items():
            self._tiles[id] = []
            self._tile_side_signatures[id] = {
                'top': set([]),
                'right': set([]),
                'bottom': set([]),
                'left': set([])
            }

            t = tile
            for _ in range(4):
                self._tiles[id].append(t)
                for side in ('top', 'right', 'bottom', 'left'):
                    self._tile_side_signatures[id][side].add(getattr(t, side))
                t = ImageTile(id, t.rotate())

            t = ImageTile(id, tile.flip())
            for _ in range(4):
                self._tiles[id].append(t)
                for side in ('top', 'right', 'bottom', 'left'):
                    self._tile_side_signatures[id][side].add(getattr(t, side))
                t = ImageTile(t.id, t.rotate())

    def corners(self) -> Dict[str, Union[ImageTile, None]]:
        return {
            'upper left': self._image[0][0],
            'upper right': self._image[0][self._size - 1],
            'lower left': self._image[self._size - 1][0],
            'lower right': self._image[self._size - 1][self._size - 1]
        }

    def _can_fit(self, x: int, y: int, tile_id: int) -> Optional[ImageTile]:
        # get all neighbors that are already placed in the image
        neighbors = []
        if 0 <= (y - 1) < self._size and self._image[y - 1][x] is not None:     # top neighbor
            neighbors.append(('top', 'bottom', (self._image[y - 1][x])))
        if 0 <= (y + 1) < self._size and self._image[y + 1][x] is not None:     # bottom neighbor
            neighbors.append(('bottom', 'top', self._image[y + 1][x]))
        if 0 <= (x - 1) < self._size and self._image[y][x - 1] is not None:     # left neighbor
            neighbors.append(('left', 'right', self._image[y][x - 1]))
        if 0 <= (x + 1) < self._size and self._image[y][x + 1] is not None:     # right neighbor
            neighbors.append(('right', 'left', self._image[y][x + 1]))

        if len(neighbors) == 0:
            raise Exception(f"No neighbors found")

        for tile in self._tiles[tile_id]:
            for tile_side, neighbor_side, neighbor in neighbors:
                if getattr(tile, tile_side) != getattr(neighbor, neighbor_side):
                    # did not fit this neighbor
                    break
            else:
                # this orientation fits! return
                return tile

        # all orientations failed to fit with its neighbors
        return None

    def solve(self) -> None:
        remaining = self._tiles.keys()
        iteration = 0
        while len(remaining) > 0:
            # in each iteration, build the outer ring of tiles out of the remaining tiles that have not been placed yet. tiles in the outer ring are either corners or edges
            corners = []
            corner_neighbors = {}
            edges = []
            next_remaining = []

            for candidate in remaining:
                neighbor_matches = set([])
                for candidate_side, neighbor_side in (('top', 'bottom'), ('right', 'left'), ('bottom', 'top'), ('left', 'right')):
                    for neighbor in (neighbor for neighbor in remaining if neighbor != candidate):
                        if len(self._tile_side_signatures[candidate][candidate_side].intersection(self._tile_side_signatures[neighbor][neighbor_side])) != 0:
                            neighbor_matches.add(neighbor)

                match len(neighbor_matches):
                    case 0:     # tile matched no neighbors...must be only tile left
                        corners.append(candidate)
                    case 2:     # tiles matching neighbors on 2 sides are corners
                        corners.append(candidate)
                        corner_neighbors[candidate] = list(neighbor_matches)
                    case 3:     # tiles matching neighbors on 3 sides are edges
                        edges.append(candidate)
                    case 4:     # tile matched neighbors on all sides, so it must in an inner ring..add it back to reminaing for later processing
                        next_remaining.append(candidate)
                    case _:
                        raise Exception(f"Unexpected neighbor count : {len(neighbor_matches)}")

            # build the outer ring of this iteration by starting at the upper left and going clockwise matching all tiles
            ring_members = deque(edges)
            if iteration == 0:      # in the first iteration, start with the corner that fits with its neighbors in the upper left
                starting_tile = None
                for cid in corners:
                    for corner in self._tiles[cid]:
                        for neighbor1, neighbor2 in ((corner_neighbors[cid][0], corner_neighbors[cid][1]), (corner_neighbors[cid][1], corner_neighbors[cid][0])):
                            match_right = 0
                            for corner_neighbor in self._tiles[neighbor1]:
                                if corner.right == corner_neighbor.left:
                                    match_right += 1
                            match_bottom = 0
                            for corner_neighbor in self._tiles[neighbor2]:
                                if corner.bottom == corner_neighbor.top:
                                    match_bottom += 1
                            if match_right == 1 and match_bottom == 1:
                                starting_tile = corner
                                break
                        if starting_tile:
                            break
                    if starting_tile:
                        break
                else:
                    raise Exception(f"Failed to find upper left corner tile in first iteration")

                self._image[iteration][iteration] = starting_tile
                for cid in corners:
                    if cid != starting_tile.id:
                        ring_members.append(cid)
            else:                   # in all other iterations, the upper left must fit with previous outer ring in the upper left
                for cid in corners:
                    corner = self._can_fit(iteration, iteration, cid)
                    if corner is not None:
                        self._image[iteration][iteration] = corner
                    else:
                        ring_members.append(cid)

            # fill top edge from left to right
            y = iteration
            for x in range(iteration + 1, self._size - iteration):
                for _ in range(len(ring_members)):
                    member = ring_members.popleft()
                    tile = self._can_fit(x, y, member)
                    if tile is not None:
                        # found a fit! add to ring and move to next member
                        self._image[y][x] = tile
                        break
                    else:
                        # did not fit, add member back to other ring members and continue fitting
                        ring_members.append(member)
                else:
                    raise Exception(f"Failed to find ring member for top edge in iteration {iteration}")

            # fill right edge from top to bottom
            x = self._size - iteration - 1
            for y in range(iteration + 1, self._size - iteration):
                for _ in range(len(ring_members)):
                    member = ring_members.popleft()
                    tile = self._can_fit(x, y, member)
                    if tile is not None:
                        # found a fit! 1add to ring and move to next member
                        self._image[y][x] = tile
                        break
                    else:
                        # did not fit, add member back to other ring members and continue fitting
                        ring_members.append(member)
                else:
                    raise Exception(f"Failed to find ring member for right edge in iteration {iteration}")

            # fill bottom edge from right to left
            y = self._size - iteration - 1
            for x in range(self._size - iteration - 2, iteration - 1, -1):
                for _ in range(len(ring_members)):
                    member = ring_members.popleft()
                    tile = self._can_fit(x, y, member)
                    if tile is not None:
                        # found a fit! 1add to ring and move to next member
                        self._image[y][x] = tile
                        break
                    else:
                        # did not fit, add member back to other ring members and continue fitting
                        ring_members.append(member)
                else:
                    raise Exception(f"Failed to find ring member for bottom edge in iteration {iteration}")

            # fill left edge from bottom to top
            x = iteration
            for y in range(self._size - iteration - 2, iteration, -1):
                for _ in range(len(ring_members)):
                    member = ring_members.popleft()
                    tile = self._can_fit(x, y, member)
                    if tile is not None:
                        # found a fit! 1add to ring and move to next member
                        self._image[y][x] = tile
                        break
                    else:
                        # did not fit, add member back to other ring members and continue fitting
                        ring_members.append(member)
                else:
                    raise Exception(f"Failed to find ring member for left edge in iteration {iteration}")

            remaining = next_remaining
            iteration += 1

    def show(self) -> None:
        for tile_row in self._image:
            for data_row in range(self._tile_size):
                line_output = []
                for tile in tile_row:
                    line_output.append("".join(tile.row(data_row)))
                print(" ".join(line_output))
            print()

    def combine(self) -> ImageTile:
        combined_size = self._size * (self._tile_size - 2)
        combined_data = [["?" for x in range(combined_size)] for y in range(combined_size)]
        for row, tiles in enumerate(self._image):
            for col, tile in enumerate(tiles):
                for y in range(1, self._tile_size - 1):
                    combined_y = (y - 1) + (row * (self._tile_size - 2))
                    for x in range(1, self._tile_size - 1):
                        combined_x = (x - 1) + (col * (self._tile_size - 2))
                        combined_data[combined_y][combined_x] = tile.data[y][x]
        return ImageTile(0, combined_data)


class ImageSearch(object):
    def __init__(self, pattern: ImageTile):
        self._pattern = pattern
        self._points_of_interest = []
        self._maxx = 0
        self._maxy = 0

        for y, row in enumerate(pattern.data):
            for x, c in enumerate(row):
                if c == '#':
                    self._points_of_interest.append(Point2D(x, y))
                    self._maxx = x if x > self._maxx else self._maxx
                    self._maxy = y if y > self._maxy else self._maxy

    def search(self, subject: ImageTile) -> Optional[ImageTile]:
        found_offsets = []
        for y in range(len(subject.data)):
            if 0 <= (y + self._maxy) < len(subject.data):
                for x in range(len(subject.data)):
                    if 0 <= (x + self._maxx) < len(subject.data):
                        for p in self._points_of_interest:
                            if subject.data[y + p.y][x + p.x] != '#':
                                # one of the points of interest was not #...so pattern does not match
                                break
                        else:
                            # all points of interests were found at this offset...record it
                            found_offsets.append(Point2D(x, y))

        if found_offsets:
            # pattern(s) found in this image, mark the pattern with O
            data = subject.data.copy()
            for offset in found_offsets:
                for p in self._points_of_interest:
                    data[offset.y + p.y][offset.x + p.x] = "O"
            return ImageTile(0, data)
        else:
            # pattern not found in this image
            return None


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
                data.append(list(line))
        self._tiles[id] = ImageTile(id, data)

    def part_one(self):
        ia = ImageArray(self._tiles)
        ia.solve()
        ia.show()

        total = 1
        for corner, tile in ia.corners().items():
            print(f"tile {tile.id} is the {corner} corner")
            tile.show()
            total *= tile.id
            print()

        return total

    def part_two(self):
        ia = ImageArray(self._tiles)
        ia.solve()

        subject = ia.combine()
        print(f"\nimage tiles combined into:")
        subject.show()

        ims = ImageSearch(ImageTile(
            1,
            [
                list("                  # "),
                list("#    ##    ##    ###"),
                list(" #  #  #  #  #  #   ")
            ]
        ))

        rough_waters = 0
        for _ in range(4):
            found = ims.search(subject)

            if found:
                print(f"\nsea monster found in image rotated as:")
                found.show()
                for row in found.data:
                    for c in row:
                        rough_waters += 1 if c == '#' else 0
                break

            subject = ImageTile(subject.id, subject.rotate())
        else:
            subject = ImageTile(subject.id, subject.flip())
            for _ in range(4):
                found = ims.search(subject)

                if found:
                    print(f"\nsea monster found in image flipped and rotated as:")
                    found.show()
                    for row in found.data:
                        for c in row:
                            rough_waters += 1 if c == '#' else 0
                    break

                subject = ImageTile(subject.id, subject.rotate())
            else:
                raise Exception("pattern not found")

        return rough_waters
