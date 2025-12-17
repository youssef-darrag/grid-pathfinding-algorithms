# dls.py
from ..grid import Grid
from ..utils import Node, reconstruct_path
from typing import List, Tuple

def dls(grid: Grid, limit: int, callback=None) -> List[Tuple[int, int]]:
    # Depth-Limited Search: stops when depth limit is reached
    stack = [(Node(position=grid.start), 0)]  # (node, depth)
    visited = set()

    while stack:
        current, depth = stack.pop()

        # Check goal
        if current.position == grid.goal:
            return reconstruct_path(current)

        # Expand node only if depth limit allows
        if depth < limit:
            for neighbor in grid.get_neighbors(current.position):
                if neighbor not in visited:
                    stack.append(
                        (Node(position=neighbor, parent=current), depth + 1)
                    )

            visited.add(current.position)

            if callback:
                callback(visited.copy())

    # No path found within the depth limit
    return []

if __name__ == "__main__":
    grid = Grid(rows=8, cols=8, obstacle_percent=0.2)
    grid.print_grid()

    depth_limit = 5
    path = dls(grid, depth_limit)  # run DLS
    print(f"\nDLS Path (limit={depth_limit}):", path)
    grid.print_grid(path=path)
