from __future__ import annotations
from typing import Dict, List, Tuple


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
