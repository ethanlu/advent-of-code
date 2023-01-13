from __future__ import annotations
from typing import List


def show_grid(grid: List[List[str]]) -> None:
    for row in grid:
        for col in row:
            print(f"{col}", end="")
        print("")
