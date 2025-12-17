from networkx import MultiDiGraph
from core.utils import reconstruct_path


def dls(
    graph: MultiDiGraph,
    start: int,
    goal: int,
    limit: int = 200,
    callback=None, 
    delay: float = 0.0,
):
    stack = [(start, 0)]
    parent = {start: None}

    while stack:
        current, current_depth = stack.pop()

        if current == goal:
            break

        if current_depth >= limit:
            continue

        for neighbor in graph.neighbors(current):
            if neighbor not in parent:
                parent[neighbor] = current
                stack.append((neighbor, current_depth + 1))

    if goal not in parent:
        return [], len(parent)

    return reconstruct_path(parent, goal), len(parent)
