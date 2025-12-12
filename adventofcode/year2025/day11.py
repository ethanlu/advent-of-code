from __future__ import annotations
from adventofcode.common import Solution
from collections import deque
from typing import List, Set


class ReactorNetwork(object):
    def __init__(self, data: List[str]):
        self._connections = {}
        for line in data:
            t = line.split(' ')
            source = t[0][:-1]
            self._connections[source] = set([destination for destination in t[1:]])

    @property
    def devices(self) -> Set[str]:
        return set(self._connections.keys())

    def paths(self, start: str, end: str, exclude: Set[str] = {}) -> int:
        paths = 0
        remaining = deque([{start: [1, {start}]}])
        while len(remaining) > 0:
            current = remaining.popleft()
            next_current = {}
            for source, (total_paths, visited) in current.items():
                for destination in self._connections[source]:
                    if destination in exclude or destination in visited:
                        continue
                    if destination == end:
                        paths += total_paths
                        continue
                    if destination not in next_current:
                        next_current[destination] = [0, set()]
                    next_current[destination][0] += total_paths
                    next_current[destination][1] = next_current[destination][1].union(visited)
            if next_current:
                remaining.append(next_current)
        return paths

    def connected_devices_downstream(self, target: str) -> Set[str]:
        connected = set()
        remaining = deque([target])
        while len(remaining) > 0:
            device = remaining.popleft()
            for d in self._connections[device]:
                if d not in connected:
                    connected.add(d)
                    if d in self._connections:
                        remaining.append(d)
        return connected

    def connected_devices_upstream(self, target: str) -> Set[str]:
        connected = set()
        remaining = deque([target])
        while len(remaining) > 0:
            device = remaining.popleft()
            for d, connections in self._connections.items():
                if device in connections and d not in connected:
                    connected.add(d)
                    remaining.append(d)
        return connected


class Day11(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._rn = ReactorNetwork(self._load_input_as_lines())

    def part_one(self):
        return self._rn.paths('you', 'out')

    def part_two(self):
        total = 0
        for device, downstream_device in (('dac', 'fft'), ('fft', 'dac')):
            print(f"considering paths 'svr' ... '{device}' ... {downstream_device} ... 'out'")
            downstream = self._rn.connected_devices_downstream(device)
            if 'out' not in downstream:
                print(f"\t'{device}' has no connections that leads to 'out'")
                continue
            if downstream_device not in downstream:
                print(f"\t'{device}' has no downstream connections to '{downstream_device}'")
                continue
            upstream = self._rn.connected_devices_upstream(device)
            if 'svr' not in upstream:
                print(f"\t'{device}' has no connections that comes from 'svr'")
                continue
            if downstream_device in upstream:
                print(f"\t'{device}' is not upstream to '{downstream_device}'")
                continue
            excluded = self._rn.devices - downstream - upstream - {device}
            print(f"\texcluding {len(excluded)} devices that are not connected to '{device}' and '{downstream_device}'")
            paths_sd = self._rn.paths('svr', device, exclude=excluded)
            print(f"\t{paths_sd} paths from 'svr' to '{device}'")
            paths_ddd = self._rn.paths(device, downstream_device, exclude=excluded.union({'out'}))
            print(f"\t{paths_ddd} paths from '{device}' to '{downstream_device}'")
            paths_ddo = self._rn.paths(downstream_device, 'out', exclude=excluded)
            print(f"\t{paths_ddo} paths from '{downstream_device}' to 'out'")
            total += paths_sd * paths_ddd * paths_ddo
        return total
