from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.grid import Point2D
from adventofcode.common.graph.search import AStar, SearchState, S
from collections import deque
from functools import cache
from itertools import pairwise
from typing import Iterable, List, Tuple


direction_deltas = {'^': Point2D(0, -1), '>': Point2D(1, 0), 'v': Point2D(0, 1), '<': Point2D(-1, 0)}
direction_deltas_reverse = {v: k for k, v in direction_deltas.items()}
direction_reverses = {'^': 'v', '>': '<', 'v': '^', '<': '>'}


class ShortestKeyToKeySequenceSearchState(SearchState):
    def __init__(self, keypad: Keypad, key: str, gain: int, cost: int):
        super().__init__(f"{key}", gain + 1, cost + 1)
        self._keypad = keypad
        self._key = key

    @property
    def key(self) -> str:
        return self._key

    def next_search_states(self) -> List[S]:
        states = []
        for direction, key in self._keypad.neighbor_keys(self._key):
            if key != ' ':
                states.append(self.__class__(self._keypad, key, self.gain, self.cost))
        return states


class CodeTranslator(object):
    def __init__(self, numeric_keypad: Keypad, directional_keypad: Keypad):
        self._nk = numeric_keypad
        self._dk = directional_keypad

    def _translate_directional_sequence(self, sequence: str) -> List[str]:
        remaining = deque([('A', sequence, '')])
        translations = []
        while len(remaining) > 0:
            current, to_translate, translated = remaining.pop()
            if len(to_translate) > 0:
                for s in self._dk.shortest_sequences(current, to_translate[0]):
                    remaining.append((to_translate[0], to_translate[1:], translated + s))
            else:
                translations.append(translated)
        return translations

    @cache
    def _shortest_translated_directional_sequence(self, sequence: str, level: int) -> str:
        translated = ''
        if level == 0:
            translated = sequence
        else:
            for subsequence in sequence.split('A')[:-1]:
                shortest = None
                for translated_subsequence in self._translate_directional_sequence(subsequence + 'A'):
                    candidate = self._shortest_translated_directional_sequence(translated_subsequence, level - 1)
                    if shortest is None or len(shortest) > len(candidate):
                        shortest = candidate
                translated += shortest
        return translated

    @cache
    def _shortest_translated_directional_sequence_length(self, sequence: str, level: int) -> int:
        translated = 0
        if level == 0:
            translated = len(sequence)
        else:
            for subsequence in sequence.split('A')[:-1]:
                shortest = None
                for translated_subsequence in self._translate_directional_sequence(subsequence + 'A'):
                    candidate = self._shortest_translated_directional_sequence_length(translated_subsequence, level - 1)
                    if shortest is None or shortest > candidate:
                        shortest = candidate
                translated += shortest
        return translated

    def translate(self, to_translate: str, level: int) -> str:
        best = ''
        for a, b in pairwise('A' + to_translate):
            shortest = None
            for sequence in self._nk.shortest_sequences(a, b):
                candidate = self._shortest_translated_directional_sequence(sequence, level)
                if shortest is None or len(shortest) > len(candidate):
                    shortest = candidate
            best += shortest
        return best

    def translate_length(self, to_translate: str, level: int) -> int:
        best = 0
        for a, b in pairwise('A' + to_translate):
            shortest = None
            for sequence in self._nk.shortest_sequences(a, b):
                candidate = self._shortest_translated_directional_sequence_length(sequence, level)
                if shortest is None or shortest > candidate:
                    shortest = candidate
            best += shortest
        return best


class Keypad(object):
    def __init__(self, keys: List[str]):
        self._keys = {}
        for y, row in enumerate(keys):
            for x, cell in enumerate(row):
                self._keys[cell] = Point2D(x, y)
        self._positions = {v: k for k, v in self._keys.items()}
        self._sequences = {}

    @property
    def keys(self) -> List[str]:
        return list(self._keys.keys())

    def shortest_sequences(self, start_key, end_key) -> List[str]:
        if (start_key, end_key) not in self._sequences:
            astar = AStar(ShortestKeyToKeySequenceSearchState(self, start_key, 0, 0), ShortestKeyToKeySequenceSearchState(self, end_key, 0, 0))
            self._sequences[(start_key, end_key)] = []
            self._sequences[(end_key, start_key)] = []
            for path in astar.find_all_paths():
                sequence = ''
                for s, e in pairwise(path.search_states):
                    sequence += direction_deltas_reverse[(self._keys[e.key] - self._keys[s.key])]
                self._sequences[(start_key, end_key)].append(sequence + 'A')
                self._sequences[(end_key, start_key)].append(''.join((direction_reverses[d] for d in reversed(sequence))) + 'A')
        return self._sequences[(start_key, end_key)]

    def neighbor_keys(self, key: str) -> Iterable[Tuple[str, str]]:
        for direction, delta in direction_deltas.items():
            p = self._keys[key] + delta
            if p in self._positions:
                yield direction, self._positions[p]


class Day21(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._nk = Keypad(['789', '456', '123', ' 0A'])
        self._dk = Keypad([' ^A', '<v>'])
        self._ct = CodeTranslator(self._nk, self._dk)
        self._codes = [line for line in self._load_input_as_lines()]

    def part_one(self):
        levels = 2
        total = 0
        for c in self._codes:
            translated = self._ct.translate(c, levels)
            print(f"[{int(c[:-1])}] {c} --({levels} levels deep)-> {translated} ({len(translated)} long)")
            total += int(c[:-1]) * len(translated)
        return total

    def part_two(self):
        levels = 25
        total = 0
        for c in self._codes:
            # can only calculate final length due to actual sequence being too long to cache
            translated_length = self._ct.translate_length(c, levels)
            print(f"[{int(c[:-1])}] {c} --({levels} levels deep)-> {translated_length} long")
            total += int(c[:-1]) * translated_length
        return total
