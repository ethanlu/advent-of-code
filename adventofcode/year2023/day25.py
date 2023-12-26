from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.graph import Node
from random import choice
from typing import Dict, Optional, Tuple


class Component(Node):
    def __init__(self, name: str):
        super().__init__(name)
        self._neighbors: Dict[str, int] = {}

    @property
    def neighbors(self) -> Dict[str, int]:
        return self._neighbors

    def add(self, name: str, edges: int = 1) -> Component:
        if name not in self._neighbors:
            self._neighbors[name] = 0
        self._neighbors[name] += edges
        return self

    def remove(self, name: str) -> Component:
        if name not in self._neighbors:
            raise Exception(f"{self._id} and {name} are not neighbors")
        self._neighbors.pop(name)
        return self


class ComponentPartitioner(object):
    def __init__(self, components: Dict[str, Component]):
        self._components: Dict[str, Component] = {k: Component(c.id) for k, c in components.items()}
        for k, c in components.items():
            for n, v in c.neighbors.items():
                self._components[k].add(n, v)

    def split(self, min_cut: int, debug: bool) -> Optional[Tuple[str, str]]:
        # based on https://en.wikipedia.org/wiki/Karger%27s_algorithm
        if debug:
            print(f"started with {len(self._components)} components")
        while len(self._components) > 2:
            a = choice(list(self._components.keys()))
            b = choice(list(self._components[a].neighbors.keys()))
            if debug:
                print(f"\tmerging {a} and {b}")

            mc = Component(','.join(sorted(self._components[a].id.split(',') + self._components[b].id.split('.'))))
            for n, v in self._components[a].neighbors.items():
                if n != b:
                    mc.add(n, v)
                    self._components[n].add(mc.id, v)
                    self._components[n].remove(a)
            for n, v in self._components[b].neighbors.items():
                if n != a:
                    mc.add(n, v)
                    self._components[n].add(mc.id, v)
                    self._components[n].remove(b)
            self._components[mc.id] = mc
            self._components.pop(a)
            self._components.pop(b)
            if debug:
                print(f"\t{len(self._components)} components left")
        a, b = list(self._components.keys())
        if self._components[a].neighbors[b] == min_cut:
            return a, b
        else:
            return None

class Day25(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._components: Dict[str, Component] = {}
        for l in self._load_input_as_lines():
            t = l.split(": ")
            if t[0] not in self._components:
                self._components[t[0]] = Component(t[0])
            for t2 in t[1].split(' '):
                if t2 not in self._components:
                    self._components[t2] = Component(t2)
                self._components[t[0]].add(t2)
                self._components[t2].add(t[0])

    def part_one(self):
        tries = 1
        while True:
            cp = ComponentPartitioner(self._components)
            r = cp.split(3, False)
            if r is not None:
                tries += 1
                break
        print(f"found after {tries} attempts!")
        a, b = r
        print(f"group a : [{len(a.split(','))}] {a}")
        print(f"group b : [{len(b.split(','))}] {b}")
        return len(a.split(',')) * len(b.split(','))

    def part_two(self):
        return "ᕕ( ᐛ )ᕗ"
