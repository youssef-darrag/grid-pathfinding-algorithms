from collections import deque

from networkx import MultiDiGraph
from core.utils import reconstruct_path


def bfs(graph: MultiDiGraph, start: int, goal: int):
    queue = deque([start])
    parent = {start: None}

    while queue:
        current = queue.popleft()
        if current == goal:
            break

        for neighbor in graph.neighbors(current):
            if neighbor not in parent:
                parent[neighbor] = current
                queue.append(neighbor)

    return reconstruct_path(parent, goal), len(parent)
