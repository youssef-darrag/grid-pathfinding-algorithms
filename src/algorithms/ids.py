from networkx import MultiDiGraph
from core.utils import reconstruct_path


def ids(
    graph: MultiDiGraph,
    start: int,
    goal: int,
    max_depth: int = 200,
    callback=None,
    delay: float = 0.0,  
):
    total_explored = 0

    for depth_limit in range(max_depth + 1):
        parent = {start: None}
        found = _depth_limited_search(graph, start, goal, depth_limit, parent)
        total_explored += len(parent)

        if found:
            return reconstruct_path(parent, goal), total_explored

    return [], total_explored


def _depth_limited_search(graph, node, goal, limit, parent, current_depth=0):
    if node == goal:
        return True

    if current_depth >= limit:
        return False

    for neighbor in graph.neighbors(node):
        if neighbor not in parent:
            parent[neighbor] = node
            if _depth_limited_search(
                graph, neighbor, goal, limit, parent, current_depth + 1
            ):
                return True

    return False
