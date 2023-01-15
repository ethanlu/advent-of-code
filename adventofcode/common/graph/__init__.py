from __future__ import annotations
from typing import TypeVar


class LinkedListNode(object):
    def __init__(self):
        self._previous = None
        self._next = None

    @property
    def previous(self) -> LLN:
        return self._previous

    @previous.setter
    def previous(self, previous_node: LLN):
        self._previous = previous_node

    @property
    def next(self) -> LLN:
        return self._next

    @next.setter
    def next(self, next_node: LLN):
        self._next = next_node


LLN = TypeVar('LLN', bound=LinkedListNode)
