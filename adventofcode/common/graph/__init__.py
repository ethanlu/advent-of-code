from __future__ import annotations
from typing import List, TypeVar


class Node(object):
    def __init__(self, id: str):
        self._id = id

    @property
    def id(self) -> str:
        return self._id

    def __eq__(self, other):
        return self._id == other.id if issubclass(type(other), Node) else False

    def __ne__(self, other):
        return self._id != other.id if issubclass(type(other), Node) else True

    def __str__(self):
        return f"({id})"

    def __hash__(self):
        return self._id.__hash__()


class LinkedListNode(Node):
    def __init__(self, id: str):
        super().__init__(id)
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


class TreeNode(Node):
    def __init__(self, id: str):
        super().__init__(id)
        self._parent = None
        self._children = []

    @property
    def parent(self) -> TN:
        return self._parent

    @parent.setter
    def parent(self, parent: TN) -> None:
        self._parent = parent

    @property
    def children(self) -> List[TN]:
        return self._children

    def add_child(self, child: TN) -> TN:
        self._children.append(child)
        child.parent = self
        return self


TN = TypeVar('TN', bound=TreeNode)
