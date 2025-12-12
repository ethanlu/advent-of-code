from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.grid import Grid2D
from typing import List


class Gift(object):
    def __init__(self, data: List[str]):
        self._shape = Grid2D(int(data[0][:-1]), [list(line) for line in data[1:]])

    @property
    def id(self) -> int:
        return self._shape.id

    @property
    def area(self) -> int:
        return sum([sum([1 for c in row if c == '#']) for row in self._shape.data])

    def flip(self) -> None:
        self._shape = Grid2D(self._shape.id, self._shape.flip())

    def rotate(self) -> None:
        self._shape = Grid2D(self._shape.id, self._shape.rotate())

    def show(self) -> None:
        self._shape.show()


class Region(object):
    def __init__(self, data: str):
        t = data.split(': ')
        r = t[0].split('x')
        self._width = int(r[0])
        self._length = int(r[1])
        self._quantities = [int(a) for a in t[1].split(' ')]

    @property
    def width(self) -> int:
        return self._width

    @property
    def length(self) -> int:
        return self._length

    @property
    def area(self) -> int:
        return self._width * self._length

    @property
    def quantities(self) -> List[int]:
        return self._quantities


class Day12(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._shapes = []
        self._regions = []
        reading_shapes = True
        shape_data = []
        for line in self._load_input_as_lines():
            if 'x' in line:
                reading_shapes = False
            if not line:
                self._shapes.append(Gift(shape_data))
                shape_data = []
                continue
            if reading_shapes:
                shape_data.append(line)
            else:
                self._regions.append(Region(line))

    def part_one(self):
        total = 0
        for i, r in enumerate(self._regions):
            areas = 0
            for i, q in enumerate(r.quantities):
                areas += self._shapes[i].area * q
            if areas > r.area:
                print(f"region {i}: {r.width}x{r.length} has total area {r.area} and need to fit {areas} worth of gifts : IMPOSSIBLE")
            else:
                total += 1
                print(f"region {i}: {r.width}x{r.length} has total area {r.area} and need to fit {areas} worth of gifts : OK")
        return total

    def part_two(self):
        pass