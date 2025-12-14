# dfs.py
from grid import Grid
from utils import Node, reconstruct_path
from typing import List, Tuple

def dfs(grid: Grid) -> List[Tuple[int, int]]:
    stack = [Node(position=grid.start)]  # Initialize stack with the start node
    visited = set()                      # Keep track of visited positions

    while stack:
        current = stack.pop()            # Pop the top node from the stack
        if current.position == grid.goal:
            # Goal reached, reconstruct and return the path
            return reconstruct_path(current)
        if current.position not in visited:
            visited.add(current.position)  # Mark current node as visited
            for neighbor in grid.get_neighbors(current.position):
                if neighbor not in visited:
                    # Add neighbor node to the stack
                    stack.append(Node(position=neighbor, parent=current))
    return []                              # Return empty list if no path found

if __name__ == "__main__":
    grid = Grid(rows=8, cols=8, obstacle_percent=0.2)
    grid.print_grid()                     # Print initial grid

    path = dfs(grid)                      # Run DFS algorithm
    print("\nDFS Path:", path)
    grid.print_grid(path=path)            # Print grid with path if found
