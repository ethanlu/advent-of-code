from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.grid import Point3D
from typing import Dict, List, Set, Tuple


fall_delta = Point3D(0, 0, -1)
rise_delta = Point3D(0, 0, 1)


class SandBrick(object):
    def __init__(self, name: str, start: Point3D, end: Point3D):
        self._name = name
        self._start: Point3D = start
        self._above: Set[SandBrick] = set()
        self._below: Set[SandBrick] = set()
        delta = end - start
        match delta.x, delta.y, delta.z:
            case d, 0, 0:
                self._deltas = [Point3D(x, 0, 0) for x in range(d + 1)]
            case 0, d, 0:
                self._deltas = [Point3D(0, y, 0) for y in range(d + 1)]
            case 0, 0, d:
                self._deltas = [Point3D(0, 0, z) for z in range(d + 1)]
            case _:
                raise Exception(f"Unexpected brick with delta of {delta} and starts at {start}")

    def __repr__(self):
        return self._name

    def __str__(self):
        return self._name

    def __hash__(self):
        return int(self._name)

    def __lt__(self, other):
        return self.start.z < other.start.z

    def __le__(self, other):
        return self.start.z <= other.start.z

    def __gt__(self, other):
        return self.start.z > other.start.z

    def __ge__(self, other):
        return self.start.z >= other.start.z

    @property
    def name(self) -> str:
        return self._name

    @property
    def start(self) -> Point3D:
        return self._start

    @property
    def size(self) -> int:
        return len(self._deltas)

    @property
    def positions(self) -> List[Point3D]:
        return [self._start + d for d in self._deltas]

    @property
    def above(self) -> Set[SandBrick]:
        return self._above

    @property
    def below(self) -> Set[SandBrick]:
        return self._below

    def move_to(self, start: Point3D) -> SandBrick:
        self._start = start
        return self

    def add_above(self, brick: SandBrick) -> SandBrick:
        self._above.add(brick)
        return self

    def add_below(self, brick: SandBrick) -> SandBrick:
        self._below.add(brick)
        return self

class SandBrickSimulator(object):
    def __init__(self, bricks: List[SandBrick], maxp: Point3D):
        self._maxp = maxp
        self._bricks: List[SandBrick] = bricks      # map of bricks to positions
        self._cubes: Dict[Point3D, SandBrick] = {}  # map of positions to bricks
        for b in self._bricks:
            for p in b.positions:
                if p in self._cubes:
                    raise Exception(f"Unexpected occupied cube at position {p}")
                self._cubes[p] = b

    def _neighbors(self, brick: SandBrick, delta: Point3D) -> Set[SandBrick]:
        dependents = set()
        for p in brick.positions:
            np = p + delta
            if np in self._cubes and self._cubes[np] != brick:
                dependents.add(self._cubes[np])
        return dependents

    def fall(self) -> None:
        for b in sorted(self._bricks):
            final_positions = b.positions
            next_positions = b.positions
            total_fall_delta = Point3D(0, 0, 0)
            ground_hit = False
            bricks_hit = set()
            while True:
                next_positions = [p + fall_delta for p in next_positions]
                for np in next_positions:
                    if np.z < 1:    # hit ground
                        ground_hit = True
                    if np in self._cubes and self._cubes[np] != b:  # hit other brick
                        bricks_hit.add(self._cubes[np])
                if ground_hit:
                    break
                if bricks_hit:  # update bricks with their neighbors
                    for bb in bricks_hit:
                        bb.add_above(b)
                        b.add_below(bb)
                    break
                final_positions = next_positions
                total_fall_delta += fall_delta
            # brick reached its final resting point, update records
            for p in b.positions:
                self._cubes.pop(p)
            for fp in final_positions:
                if fp in self._cubes:
                    raise Exception(f"Unexpected occupied cube for final position {fp}")
                self._cubes[fp] = b
            b.move_to(b.start + total_fall_delta)

    def show(self, axis: str = 'xz') -> None:
        grid: Dict[Tuple[int, int], str] = {}
        for r in range(self._maxp.z + 1):
            for c in range((self._maxp.x if axis == 'xz' else self._maxp.y) + 1):
                grid[(c, r)] = '.' if r != 0 else '-'
        for b in self._bricks:
            for p in b.positions:
                key = (p.x, p.z) if axis == 'xz' else (p.y, p.z)
                if key not in grid or grid[key] in ('.', b.name):
                    grid[key] = b.name
                else:
                    grid[key] = '?'
        print(f"{axis} axis:")
        for r in range(self._maxp.z, -1, -1):
            for c in range((self._maxp.x if axis == 'xz' else self._maxp.y) + 1):
                print(grid[(c, r)], end="")
            print("")

    def destroyable(self) -> Set[SandBrick]:
        destroyable = set()
        for b in self._bricks:
            if b.above: # bricks with at least 1 brick above them
                # check if the above-bricks have another brick below them for alternative support
                for ab in b.above:
                    if not ab.below.difference({b}):
                        break
                else:
                    # all above-bricks have an alternate support brick
                    destroyable.add(b)
            else:
                # bricks with nothing above it can be disintegrated
                destroyable.add(b)
        return destroyable

class Day22(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._bricks = []
        self._maxp = Point3D(0, 0, 0)
        for i, l in enumerate(self._load_input_as_lines()):
            t = l.split('~')
            p1, p2 = t[0].split(','), t[1].split(',')
            self._bricks.append(SandBrick(str(i + 1), Point3D(int(p1[0]), int(p1[1]), int(p1[2])), Point3D(int(p2[0]), int(p2[1]), int(p2[2]))))
            self._maxp = Point3D(max(self._maxp.x, int(p1[0]), int(p2[0])), max(self._maxp.y, int(p1[1]), int(p2[1])), max(self._maxp.z, int(p1[2]), int(p2[2])))
            if int(p1[2]) > int(p2[2]):
                raise Exception(f"Unexpected start-end pair for brick {i + 1}")
        self._sbs = SandBrickSimulator(self._bricks, self._maxp)

    def part_one(self):
        self._sbs.fall()
        destroyable = self._sbs.destroyable()
        print(f"bricks {str(destroyable)} can be disintegrated")
        return len(destroyable)

    def part_two(self):
        def all_fallable_bricks_above(bricks: Set[SandBrick], all_falling_bricks: Set[SandBrick]) -> Set[SandBrick]:
            next_falling = set()
            for brick in bricks:
                for ab in brick.above:
                    # check if this brick has an alternate support that is not in the set of bricks that are falling so far
                    if len(ab.below.difference(all_falling_bricks)) == 0:
                        # no other bricks below it support, so it will also fall..add it to the set of falling bricks
                        next_falling.add(ab)
            if next_falling:
                return next_falling.union(all_fallable_bricks_above(next_falling, all_falling_bricks.union(next_falling)))
            return next_falling

        # run part 1 incase it was not run (should be idempotent)
        self._sbs.fall()
        destroyable = self._sbs.destroyable()

        falling_other_bricks = 0
        for b in self._bricks:
            if b not in destroyable:
                falling_bricks_above = all_fallable_bricks_above({b}, {b})
                #print(f"brick {b.name} has bricks {str(falling_bricks_above)} above it : {len(falling_bricks_above)}")
                falling_other_bricks += len(falling_bricks_above)
        return falling_other_bricks
