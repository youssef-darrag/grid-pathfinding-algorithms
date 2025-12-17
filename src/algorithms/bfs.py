from collections import deque
import time
from networkx import MultiDiGraph
from core.utils import reconstruct_path


def bfs(graph: MultiDiGraph, start: int, goal: int, callback=None, delay: float = 0.0):
    queue = deque([start])
    parent = {start: None}
    visited_set = set()

    while queue:
        current = queue.popleft()

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
                queue.append(neighbor)

    return reconstruct_path(parent, goal), len(parent)
