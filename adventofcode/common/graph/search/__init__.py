from __future__ import annotations
from abc import ABC, abstractmethod
from collections import deque
from copy import copy
from functools import reduce, total_ordering
from queue import PriorityQueue
from typing import Dict, List, Tuple, TypeVar


class SearchState(ABC):
    def __init__(self, fingerprint: str, gain: int, cost: int):
        self._fingerprint = fingerprint
        self._gain = gain
        self._cost = cost
        self._completed = False

    def __eq__(self, other):
        return self.fingerprint == other.fingerprint if issubclass(type(other), SearchState) else False

    def __ne__(self, other):
        return self.fingerprint != other.fingerprint if issubclass(type(other), SearchState) else True

    def __lt__(self, other):
        return (self.cost + self.potential_gain) < (other.cost + other.potential_gain)

    def __le__(self, other):
        return (self.cost + self.potential_gain) <= (other.cost + other.potential_gain)

    def __gt__(self, other):
        return (self.cost + self.potential_gain) > (other.cost + other.potential_gain)

    def __ge__(self, other):
        return (self.cost + self.potential_gain) >= (other.cost + other.potential_gain)

    def __hash__(self):
        return hash(self.fingerprint)

    def __str__(self):
        return self.fingerprint

    @property
    def fingerprint(self) -> str:
        return self._fingerprint

    @fingerprint.setter
    def fingerprint(self, fingerprint: str):
        self._fingerprint = fingerprint

    @property
    def gain(self) -> int:
        return self._gain

    @property
    def cost(self) -> int:
        return self._cost

    @property
    def potential_gain(self) -> int:
        return 0

    @property
    def completed(self) -> bool:
        return self._completed

    @abstractmethod
    def next_search_states(self) -> List[S]:
        raise Exception("implement in subclass")

    def complete(self) -> S:
        self._completed = True
        return self


S = TypeVar('S', bound=SearchState)


@total_ordering
class SearchPath(object):
    def __init__(self, start_state: S):
        self._search_states: List[S] = [start_state]

    def __eq__(self, other):
        return self.gain == other.gain if issubclass(type(other), SearchPath) else False

    def __ne__(self, other):
        return self.gain != other.gain if issubclass(type(other), SearchPath) else False

    def __lt__(self, other):
        return (self.cost + self.depth - (self.gain + self.potential_gain)) < (other.cost + other.depth - (other.gain + other.potential_gain))

    def __le__(self, other):
        return (self.cost + self.depth - (self.gain + self.potential_gain)) <= (other.cost + other.depth - (other.gain + other.potential_gain))

    def __gt__(self, other):
        return (self.cost + self.depth - (self.gain + self.potential_gain)) > (other.cost + other.depth - (other.gain + other.potential_gain))

    def __ge__(self, other):
        return (self.cost + self.depth - (self.gain + self.potential_gain)) >= (other.cost + other.depth - (other.gain + other.potential_gain))

    def __copy__(self):
        cls = self.__class__
        clone = cls.__new__(cls)
        clone.__dict__.update(self.__dict__)
        # create a new list, but keep references to same search state instances to save memory
        clone._search_states = [search_state for search_state in self._search_states]
        return clone

    def __str__(self):
        return f"[{self.gain}:{self.cost}:{self.depth}] (" + ") -> (".join((str(state) for state in self._search_states)) + ")"

    @property
    def depth(self) -> int:
        return len(self._search_states)

    @property
    def gain(self) -> int:
        return self._search_states[-1].gain

    @property
    def cost(self) -> int:
        return self._search_states[-1].cost

    @property
    def completed(self) -> bool:
        return self._search_states[-1].completed

    @property
    def potential_gain(self) -> int:
        return self._search_states[-1].potential_gain

    @property
    def last(self):
        return self._search_states[-1]

    @property
    def search_states(self) -> List[S]:
        return self._search_states

    def add(self, search_state: S) -> P:
        self._search_states.append(search_state)
        return self


P = TypeVar('P', bound=SearchPath)


class DebugMixin(object):
    def __init__(self):
        self._verbose = False
        self._lap = 5000

    def verbose(self, verbose: bool, lap: int) -> DebugMixin:
        self._verbose = verbose
        self._lap = lap
        return self


class AStar(DebugMixin):
    def __init__(self, start: S, end: S):
        super().__init__()
        self._start = start
        self._end = end

    def find_path(self, ) -> P:
        scores = {self._start: 0}
        shortest_previous = {}

        candidates = PriorityQueue()
        candidates.put(self._start)

        i = 1
        trimmed = 0
        while not candidates.empty():
            candidate: S = candidates.get()

            if candidate == self._end:
                # reached end...build shortest path and return
                sequence = deque([])
                current = candidate
                while current in shortest_previous.keys():
                    sequence.appendleft(current)
                    current = shortest_previous[current]

                return reduce(lambda path, state: path.add(state), sequence, SearchPath(self._start))

            # continue search by getting current search state's next states and add to priority queue
            for next_search_state in candidate.next_search_states():
                if next_search_state not in scores.keys() or next_search_state.cost < scores[next_search_state]:
                    scores[next_search_state] = next_search_state.cost
                    shortest_previous[next_search_state] = candidate
                    candidates.put(next_search_state)
                    continue

                trimmed += 1

            i += 1
            if self._verbose and i % self._lap == 0:
                print(f"{i} : ~{candidates.qsize()} : {trimmed}")

        return SearchPath(self._start)

    def find_all_paths(self) -> List[P]:
        scores = {self._start: 0}
        shortest_previous = {}
        lowest_cost = None
        end_candidate = None

        candidates = PriorityQueue()
        candidates.put(self._start)

        i = 1
        trimmed = 0
        while not candidates.empty():
            candidate: S = candidates.get()

            if candidate == self._end:
                if lowest_cost is None:
                    # encountered first shortest path...record the cost and keep searching until no more paths of equal cost are found
                    lowest_cost = candidate.cost
                    end_candidate = candidate
                if lowest_cost != candidate.cost:
                    # encountered all shortest paths...end search
                    break
                # keep searching as long as candidate are found with the same shortest path cost
                continue

            # continue search by getting current search state's next states and add to priority queue
            for next_search_state in candidate.next_search_states():
                if next_search_state not in scores.keys() or next_search_state.cost <= scores[next_search_state]:
                    scores[next_search_state] = next_search_state.cost
                    if next_search_state not in shortest_previous:
                        shortest_previous[next_search_state] = set([])
                    shortest_previous[next_search_state].add(candidate)
                    candidates.put(next_search_state)
                    continue
                trimmed += 1

            i += 1
            if self._verbose and i % self._lap == 0:
                print(f"{i} : ~{candidates.qsize()} : {trimmed}")

        shortest_paths = []
        remaining = deque([[end_candidate]])
        while len(remaining) > 0:
            path = remaining.pop()
            if path[-1] in shortest_previous:
                for ns in shortest_previous[path[-1]]:
                    remaining.append(path + [ns])
            else:
                shortest_paths.append(reduce(lambda p, s: p.add(s), reversed(path[:-1]), SearchPath(path[-1])))
        return shortest_paths


class BFS(DebugMixin):
    def __init__(self, start_path: P):
        super().__init__()
        self._start_path = start_path

    def find_path(self) -> P:
        best = None

        candidates = PriorityQueue()
        candidates.put(self._start_path)

        i = 1
        trimmed = 0
        while not candidates.empty():
            candidate: SearchPath = candidates.get()

            # candidate completed its search, check if it is now the current best before continuing search
            if candidate.completed:
                if (best is None) or (candidate.gain > best.gain) or (candidate.gain == best.gain and candidate.cost < best.cost):
                    best = candidate
                continue

            # continue search by getting current search state's next states and add to priority queue
            for next_search_state in candidate.last.next_search_states():
                if best is not None and next_search_state.gain < best.gain and (next_search_state.potential_gain + next_search_state.gain) < best.gain:
                    trimmed += 1
                    continue

                candidates.put(copy(candidate).add(next_search_state))

            i += 1
            if self._verbose and i % self._lap == 0:
                print(f"{i} : ~{candidates.qsize()} : {trimmed} : " + (f"{best.gain}" + best.last.fingerprint if best is not None else '?'))

        return best


class DFS(DebugMixin):
    def __init__(self, start_path: P):
        super().__init__()
        self._start_path = start_path
        self._cached = {}

    def find_path(self) -> P:
        best = None

        candidates = deque()
        candidates.append(self._start_path)

        visited: Dict[S, Tuple[int, int]] = {}

        i = 1
        trimmed = 0
        while len(candidates) > 0:
            candidate: SearchPath = candidates.pop()

            # candidate completed its search, check if it is now the current best before continuing search
            if candidate.completed:
                if (best is None) or (candidate.gain > best.gain) or (candidate.gain == best.gain and candidate.cost < best.cost):
                    best = candidate
                continue

            # continue search by getting current search state's next states and add to priority queue
            for next_search_state in candidate.last.next_search_states():
                if best is not None and next_search_state.gain < best.gain and (next_search_state.potential_gain + next_search_state.gain) < best.gain:
                    trimmed += 1
                    continue

                if next_search_state in visited and\
                        (next_search_state.gain < visited[next_search_state][0] or
                         (next_search_state.gain == visited[next_search_state][0] and next_search_state.cost >= visited[next_search_state][1])):
                    trimmed += 1
                    continue

                visited[next_search_state] = (next_search_state.gain, next_search_state.cost)
                candidates.append(copy(candidate).add(next_search_state))

            i += 1
            if self._verbose and i % self._lap == 0:
                print(f"{i} : ~{len(candidates)} : {trimmed} : " + (f"{best.gain}" + best.last.fingerprint if best is not None else '?'))

        return best
