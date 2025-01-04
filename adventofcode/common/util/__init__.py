from __future__ import annotations
from typing import Dict, List, Tuple
from itertools import cycle, islice


def show_grid(grid: List[List[str]]) -> None:
    for row in grid:
        for col in row:
            print(f"{col}", end="")
        print("")


def show_dict_grid(grid: Dict[Tuple[int, int], str], max_x: int, max_y: int):
    for y in range(max_y):
        for x in range(max_x):
            print(grid[(x, y)], end="")
        print("")


def roundrobin(*iterables):
    # https://docs.python.org/3.13/library/itertools.html#itertools-recipes
    # Visit input iterables in a cycle until each is exhausted.
    # roundrobin('ABC', 'D', 'EF') → A D E B F C
    # Algorithm credited to George Sakkis
    iterators = map(iter, iterables)
    for num_active in range(len(iterables), 0, -1):
        iterators = cycle(islice(iterators, num_active))
        yield from map(next, iterators)