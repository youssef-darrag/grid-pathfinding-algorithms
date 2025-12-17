import time
from networkx import MultiDiGraph
from core.utils import reconstruct_path


def dfs(
    graph: MultiDiGraph,
    start: int,
    goal: int,
    callback=None,
    delay: float = 0.0,  # Not used but kept for compatibility
):
    """
    DFS algorithm with optional step-by-step visualization.

    Args:
        callback: Function called with (current_node, visited_set) after each step
        delay: Kept for compatibility (delay is handled in callback)
    """
    stack = [start]
    parent = {start: None}
    visited_set = set()

    while stack:
        current = stack.pop()

        if current in visited_set:
            continue

        visited_set.add(current)

        # Call callback for visualization (no sleep here)
        if callback:
            callback(current, visited_set.copy())

        if current == goal:
            break

        for neighbor in graph.neighbors(current):
            if neighbor not in parent:
                parent[neighbor] = current
                stack.append(neighbor)

    return reconstruct_path(parent, goal), len(parent)
