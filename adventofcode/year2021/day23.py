from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.grid import Point2D
from adventofcode.common.graph.search import AStar, SearchState, S
from typing import Dict, Iterable, List, Optional


costs = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}


def move_cost(id: str, start: Point2D, end: Point2D) -> int:
    delta = end - start
    match end.y:
        case 1:  # moving to hallway
            return (abs(delta.x) + abs(delta.y)) * costs[id]
        case 2 | 3:  # moving to room
            match start.y:
                case 1:  # from hallway
                    return (abs(delta.x) + abs(delta.y)) * costs[id]
                case 2 | 3:  # from another room
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

    @property
    def id(self) -> str:
        occupied_positions = {o.position: o.id for o in self._occupied}
        return ''.join(['.' if h not in occupied_positions else occupied_positions[h] for h in self._hallways])

    @property
    def occupied(self) -> List[Amphipod]:
        return self._occupied

    def available(self) -> Iterable[Point2D]:
        occupied_positions = set((amp.position for amp in self._occupied))
        for p in (Point2D(1, 1), Point2D(2, 1), Point2D(4, 1), Point2D(6, 1), Point2D(8, 1), Point2D(10, 1), Point2D(11, 1)):
            if p not in occupied_positions:
                yield p

    def moveables(self) -> Iterable[Amphipod]:
        for amp in self._occupied:
            yield amp


class Rooms(object):
    def __init__(self, occupied: List[Amphipod]):
        self._rooms: Dict[Point2D, Dict[str, Optional[Amphipod], str]] = {
            # every two is an outer and inner pair of rooms
            Point2D(3, 2): {'id': 'A', 'occupancy': None}, Point2D(3, 3): {'id': 'A', 'occupancy': None},
            Point2D(5, 2): {'id': 'B', 'occupancy': None}, Point2D(5, 3): {'id': 'B', 'occupancy': None},
            Point2D(7, 2): {'id': 'C', 'occupancy': None}, Point2D(7, 3): {'id': 'C', 'occupancy': None},
            Point2D(9, 2): {'id': 'D', 'occupancy': None}, Point2D(9, 3): {'id': 'D', 'occupancy': None}
        }
        self._occupied = occupied
        for amp in occupied:
            self._rooms[amp.position]['occupancy'] = amp

    @property
    def id(self) -> str:
        return ''.join((r['occupancy'].id if r['occupancy'] is not None else '.' for r in self._rooms.values()))

    @property
    def occupied(self) -> List[Amphipod]:
        return self._occupied

    def available(self, rid: str) -> Iterable[Point2D]:
        for (outer_p, outer_room), (inner_p, inner_room) in doubles(list(self._rooms.items())):
            if outer_room['occupancy'] is None and inner_room['occupancy'] is None and inner_room['id'] == rid:
                yield inner_p
            if outer_room['occupancy'] is None and inner_room['occupancy'] is not None and inner_room['id'] == inner_room['occupancy'].id and outer_room['id'] == rid:
                # outer room is available while inner room is correctly occupied
                yield outer_p

    def moveables(self) -> Iterable[Amphipod]:
        for outer_room, inner_room in doubles(list(self._rooms.values())):
            if outer_room['occupancy'] is not None and (outer_room['occupancy'].id != outer_room['id'] or (inner_room['occupancy'] is not None and inner_room['occupancy'].id != inner_room['id'])):
                # outer room has wrong occupancy or inner room has wrong occupancy
                yield outer_room['occupancy']
            if outer_room['occupancy'] is None and inner_room['occupancy'] is not None and inner_room['occupancy'].id != inner_room['id']:
                # outer is not occupied and inner has wrong occupancy, so inner is moveable
                yield inner_room['occupancy']


class LeastEnergyUsedSearchState(SearchState):
    def __init__(self, h: Hallway, r: Rooms, cost: int):
        super().__init__(f"{r.id}|{h.id}", 0, cost)
        self._h = h
        self._r = r

    @property
    def h(self):
        return self._h

    @property
    def r(self):
        return self._r

    def _hallway_path_unobstructed(self, start: Point2D, end: Point2D) -> bool:
        occupied_hallway_positions = {amp.position for amp in self._h.occupied}
        x_delta = Point2D(1 if end.x > start.x else -1, 0)
        current = Point2D(start.x, 1)
        while current.x != end.x:
            current = current + x_delta
            if current in occupied_hallway_positions:
                return False
        return True

    def next_search_states(self) -> List[S]:
        states = []
        # see if any amphipods in hallway can be moved into rooms
        for amp in self._h.moveables():
            # amphipod is in hallway, see which room it can move into
            for room_position in self._r.available(amp.id):
                if self._hallway_path_unobstructed(amp.position, room_position):
                    # path to room is unobstructed
                    s = LeastEnergyUsedSearchState(
                        Hallway([a for a in self._h.occupied if a.position != amp.position]),
                        Rooms(self._r.occupied + [Amphipod(amp.id, room_position)]),
                        self.cost + move_cost(amp.id, amp.position, room_position)
                    )
                    states.append(s)
        # see if any amphipods in rooms can be moved into room or hallway
        for amp in self._r.moveables():
            # amphipod is in a room, see if it can move into the correct room
            for room_position in self._r.available(amp.id):
                if self._hallway_path_unobstructed(amp.position, room_position):
                    # path to room is unobstructed
                    s = LeastEnergyUsedSearchState(
                        Hallway([a for a in self._h.occupied]),
                        Rooms([a for a in self._r.occupied if a.position != amp.position] + [Amphipod(amp.id, room_position)]),
                        self.cost + move_cost(amp.id, amp.position, room_position)
                    )
                    states.append(s)
                    break
            else:
                # otherwise, see if it can move into hallway
                for hallway_position in self._h.available():
                    if self._hallway_path_unobstructed(amp.position, hallway_position):
                        # path to hallway is unobstructed
                        s = LeastEnergyUsedSearchState(
                            Hallway(self._h.occupied + [Amphipod(amp.id, hallway_position)]),
                            Rooms([a for a in self._r.occupied if a.position != amp.position]),
                            self.cost + move_cost(amp.id, amp.position, hallway_position)
                        )
                        states.append(s)
        return states


class Day23(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._occupied = []
        for y, row in enumerate(self._load_input_as_lines(False)):
            for x, cell in enumerate(row):
                if cell in ('A', 'B', 'C', 'D'):
                    self._occupied.append(Amphipod(cell, Point2D(x, y)))

    def part_one(self):
        astar = AStar(
            LeastEnergyUsedSearchState(Hallway([]), Rooms(self._occupied), 0),
            LeastEnergyUsedSearchState(Hallway([]), Rooms([
                Amphipod('A', Point2D(3, 2)), Amphipod('A', Point2D(3, 3)),
                Amphipod('B', Point2D(5, 2)), Amphipod('B', Point2D(5, 3)),
                Amphipod('C', Point2D(7, 2)), Amphipod('C', Point2D(7, 3)),
                Amphipod('D', Point2D(9, 2)), Amphipod('D', Point2D(9, 3))]), 0))
        astar.verbose(True, 10000)
        best = astar.find_path()
        for s in best.search_states:
            print(f"{s.r.id}|{s.h.id} - {s.cost}")
        return best.cost

    def part_two(self):
        pass
