from __future__ import annotations
from abc import ABC, abstractmethod
from copy import copy
from functools import total_ordering
from queue import PriorityQueue
from typing import List, Type, TypeVar


class SearchState(ABC):
    def __init__(self, fingerprint: str, gain: int, cost: int, max_cost: int):
        self._fingerprint = fingerprint
        self._gain = gain
        self._cost = cost
        self._max_cost = max_cost

    def __eq__(self, other):
        return self.fingerprint == other.fingerprint if issubclass(type(other), SearchState) else False

    def __ne__(self, other):
        return self.fingerprint != other.fingerprint if issubclass(type(other), SearchState) else True

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
    def max_cost(self) -> int:
        return self._max_cost

    @property
    def potential_gain(self) -> int:
        return 0

    @abstractmethod
    def next_search_states(self, previous_search_state: S) -> List[S]:
        raise Exception("implement in subclass")


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
    def max_cost(self) -> int:
        return self._search_states[-1].max_cost

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
    def __init__(self, start_path: P, end: S):
        super().__init__()
        self._start_path = start_path
        self._end = end

    def find_path(self, ) -> P:
        best = self._start_path
        visited = {self._start_path.last}

        candidates = PriorityQueue()
        candidates.put(best)

        i = 1
        trimmed = 0
        while not candidates.empty():
            candidate: SearchPath = candidates.get()

            # found end, end search
            if candidate.last == self._end:
                best = candidate
                break

            # continue search by getting current search state's next states and add to priority queue
            for next_search_state in candidate.last.next_search_states(candidate.last if candidate.depth > 0 else None):
                if next_search_state in visited:
                    trimmed += 1
                    continue

                visited.add(next_search_state)
                candidates.put(copy(candidate).add(next_search_state))

            i += 1
            if self._verbose and i % self._lap == 0:
                print(f"{i} : ~{candidates.qsize()} : {trimmed} : ({candidate.gain}){candidate.last.fingerprint}")

        return best


class BFS(DebugMixin):
    def __init__(self, start_path: P, max_cost: int):
        super().__init__()
        self._start_path = start_path
        self._max_cost = max_cost

    def find_path(self) -> P:
        best = self._start_path

        candidates = PriorityQueue()
        candidates.put(best)

        i = 1
        trimmed = 0
        while not candidates.empty():
            candidate: SearchPath = candidates.get()

            # candidate reached max cost limit, check if it is now the current best before continuing search
            if candidate.cost >= self._max_cost:
                if candidate.gain > best.gain:
                    best = candidate
                continue

            # continue search by getting current search state's next states and add to priority queue
            for next_search_state in candidate.last.next_search_states(candidate.last if candidate.depth > 0 else None):
                if next_search_state.gain < best.gain and (next_search_state.potential_gain + next_search_state.gain) < best.gain:
                    trimmed += 1
                    continue

                candidates.put(copy(candidate).add(next_search_state))

            i += 1
            if self._verbose and i % self._lap == 0:
                print(f"{i} : ~{candidates.qsize()} : {trimmed} : ({best.gain}){best.last.fingerprint}")

        return best
