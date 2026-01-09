from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.grid import Point2D
from adventofcode.common.graph.search import AStar, SearchState, S
from typing import Dict, Iterable, List, Optional


costs = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
room_positions = {
    'A': [Point2D(3, i) for i in range(2, 6, 1)],
    'B': [Point2D(5, i) for i in range(2, 6, 1)],
    'C': [Point2D(7, i) for i in range(2, 6, 1)],
    'D': [Point2D(9, i) for i in range(2, 6, 1)]
}


def move_cost(id: str, start: Point2D, end: Point2D) -> int:
    delta = end - start
    match end.y:
        case 1:  # moving to hallway
            return (abs(delta.x) + abs(delta.y)) * costs[id]
        case 2 | 3 | 4 | 5:  # moving to room
            match start.y:
                case 1:  # from hallway
                    return (abs(delta.x) + abs(delta.y)) * costs[id]
                case 2 | 3 | 4 | 5:  # from another room
                    return (abs(delta.x) + ((end.y - 1) + (start.y - 1))) * costs[id]
                case _:
                    raise Exception(f"unexpected start position for move : {start}")
        case _:
            raise Exception(f"unexpected end position for move : {end}")


def doubles(items: List):
    for i in range(0, len(items), 2):
        if i + 2 < len(items):
            yield items[i:i + 2]
        else:
            yield items[i:]


class Amphipod(object):
    def __init__(self, id: str, position: Point2D):
        self._id = id
        self._position = position

    def __hash__(self):
        return hash(self._id) + hash(self._position)

    def __eq__(self, other):
        return self.id == other.id and self.position == other.position if isinstance(other, Amphipod) else False

    @property
    def id(self) -> str:
        return self._id

    @property
    def position(self) -> Point2D:
        return self._position


class Hallway(object):
    def __init__(self, occupied: List[Amphipod]):
        self._hallways = (Point2D(1, 1), Point2D(2, 1), Point2D(4, 1), Point2D(6, 1), Point2D(8, 1), Point2D(10, 1), Point2D(11, 1))
        self._occupied = occupied
        self._occupied_positions = {amp.position for amp in self.occupied}

    @property
    def id(self) -> str:
        occupied_positions = {o.position: o.id for o in self._occupied}
        return ''.join(['.' if h not in occupied_positions else occupied_positions[h] for h in self._hallways])

    @property
    def occupied(self) -> List[Amphipod]:
        return self._occupied

    def is_unobstructed(self, start: Point2D, end: Point2D) -> bool:
        x_delta = Point2D(1 if end.x > start.x else -1, 0)
        current = Point2D(start.x, 1)
        while current.x != end.x:
            current = current + x_delta
            if current in self._occupied_positions:
                return False
        return True

    def available(self) -> Iterable[Point2D]:
        for p in (Point2D(1, 1), Point2D(2, 1), Point2D(4, 1), Point2D(6, 1), Point2D(8, 1), Point2D(10, 1), Point2D(11, 1)):
            if p not in self._occupied_positions:
                yield p

    def moveables(self) -> Iterable[Amphipod]:
        for amp in self._occupied:
            yield amp


class Room(object):
    def __init__(self, rid: str, depth: int, occupied: List[Amphipod]):
        self._rid = rid
        self._depth = depth
        self._rooms = {room_positions[rid][i]: None for i in range(depth)}
        for amp in occupied:
            if amp.position not in self._rooms:
                raise Exception(f"unexpected position {amp.position} in room type {rid}")
            self._rooms[amp.position] = amp
        self._move_order = []
        self._available_order = []
        correct_occupancy = True
        for room_position, occupancy in reversed(self._rooms.items()):
            correct_occupancy = correct_occupancy and (occupancy is None or occupancy.id == self._rid)
            if correct_occupancy and occupancy is None:
                # while occupancy is correct, any non-occupied room are available in the order they are encountered
                self._available_order.append(room_position)
            if not correct_occupancy and occupancy is not None:
                # while occupancy is incorrect, any occupant encountered can be moved in reverse order
                self._move_order.append(occupancy)

    @property
    def id(self) -> str:
        return ''.join(['.' if o is None else o.id for o in self._rooms.values()])

    @property
    def depth(self) -> int:
        return self._depth

    @property
    def occupied(self) -> List[Amphipod]:
        return [occupancy for occupancy in self._rooms.values() if occupancy is not None]

    def available(self) -> Optional[Point2D]:
        return self._available_order[0] if self._available_order else None

    def moveable(self) -> Optional[Amphipod]:
        return self._move_order[-1] if self._move_order else None


class LeastEnergyUsedSearchState(SearchState):
    def __init__(self, hallway: Hallway, rooms: Dict[str, Room], cost: int):
        super().__init__(f"{''.join(r.id for r in rooms.values())}|{hallway.id}", 0, cost)
        self._hallway = hallway
        self._rooms = rooms

    @property
    def rooms_id(self) -> str:
        return ''.join(r.id for r in self._rooms.values())

    @property
    def hallway_id(self) -> str:
        return self._hallway.id

    def next_search_states(self) -> List[S]:
        states = []
        in_hallway = list(self._hallway.moveables())
        in_rooms = list(filter(None, (r.moveable() for r in self._rooms.values())))
        moved_to_room = set()
        # see if any occupants in rooms or hallway can be moved into their respective rooms
        for occupant in (in_rooms + in_hallway):
            available_room_position = self._rooms[occupant.id].available()
            if available_room_position and self._hallway.is_unobstructed(occupant.position, available_room_position):
                # room is available and the path to it is unobstructed
                states.append(LeastEnergyUsedSearchState(
                    Hallway([o for o in self._hallway.occupied if o.position != occupant.position]),
                    {rid: Room(
                        rid, room.depth,
                        [o for o in room.occupied if o.position != occupant.position] + ([] if occupant.id != rid else [Amphipod(occupant.id, available_room_position)]))
                        for rid, room in self._rooms.items()
                    },
                    self.cost + move_cost(occupant.id, occupant.position, available_room_position)
                ))
                moved_to_room.add(occupant)
        # see if any occupants in rooms can be moved into the hallway
        for occupant in list(set(in_rooms) - moved_to_room):
            for available_hallway_position in self._hallway.available():
                if self._hallway.is_unobstructed(occupant.position, available_hallway_position):
                    states.append(LeastEnergyUsedSearchState(
                        Hallway(self._hallway.occupied + [Amphipod(occupant.id, available_hallway_position)]),
                        {rid: Room(rid, room.depth, [o for o in room.occupied if o.position != occupant.position]) for rid, room in self._rooms.items()},
                        self.cost + move_cost(occupant.id, occupant.position, available_hallway_position)
                    ))
        return states


class Day23(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._occupancy = {}
        for y, row in enumerate(self._load_input_as_lines(False)):
            for x, cell in enumerate(row):
                if cell in ('A', 'B', 'C', 'D'):
                    p = Point2D(x, y)
                    self._occupancy[p] = Amphipod(cell, p)

    def part_one(self):
        num_rooms = 2
        astar = AStar(
            LeastEnergyUsedSearchState(Hallway([]), {rid: Room(rid, num_rooms, [self._occupancy[p] for p in positions if p in self._occupancy]) for rid, positions in room_positions.items()}, 0),
            LeastEnergyUsedSearchState(Hallway([]), {rid: Room(rid, num_rooms, [Amphipod(rid, p) for i, p in enumerate(positions) if i < num_rooms]) for rid, positions in room_positions.items()}, 0)
        )
        astar.verbose(True, 10000)
        best = astar.find_path()
        for s in best.search_states:
            print(f"{s.rooms_id}|{s.hallway_id} -> {s.cost}")
        return best.cost

    def part_two(self):
        num_rooms = 4
        column_occupancy = {
            'A': [self._occupancy[Point2D(3, 2)], Amphipod('D', Point2D(3, 3)), Amphipod('D', Point2D(3, 4)), Amphipod(self._occupancy[Point2D(3, 3)].id, Point2D(3, 5))],
            'B': [self._occupancy[Point2D(5, 2)], Amphipod('C', Point2D(5, 3)), Amphipod('B', Point2D(5, 4)), Amphipod(self._occupancy[Point2D(5, 3)].id, Point2D(5, 5))],
            'C': [self._occupancy[Point2D(7, 2)], Amphipod('B', Point2D(7, 3)), Amphipod('A', Point2D(7, 4)), Amphipod(self._occupancy[Point2D(7, 3)].id, Point2D(7, 5))],
            'D': [self._occupancy[Point2D(9, 2)], Amphipod('A', Point2D(9, 3)), Amphipod('C', Point2D(9, 4)), Amphipod(self._occupancy[Point2D(9, 3)].id, Point2D(9, 5))],
        }
        astar = AStar(
            LeastEnergyUsedSearchState(Hallway([]), {rid: Room(rid, num_rooms, occupants) for rid, occupants in column_occupancy.items()}, 0),
            LeastEnergyUsedSearchState(Hallway([]), {rid: Room(rid, num_rooms, [Amphipod(rid, p) for i, p in enumerate(positions) if i < num_rooms]) for rid, positions in room_positions.items()}, 0)
        )
        astar.verbose(True, 10000)
        best = astar.find_path()
        for s in best.search_states:
            print(f"{s.rooms_id}|{s.hallway_id} -> {s.cost}")
        return best.cost
