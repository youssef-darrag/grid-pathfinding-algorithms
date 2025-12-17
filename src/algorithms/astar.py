import heapq
import math
import time
from networkx import MultiDiGraph
from core.utils import reconstruct_path


def astar(
    graph: MultiDiGraph,
    start: int,
    goal: int,
    nodes_data: dict[int, tuple[float, float]],
    callback=None,
    delay: float = 0.0,  # Not used but kept for compatibility
):
    """
    A* algorithm with optional step-by-step visualization.

    Args:
        callback: Function called with (current_node, visited_set) after each step
        delay: Kept for compatibility (delay is handled in callback)
    """
    pq = [(0, start)]
    g_score = {start: 0}
    parent = {start: None}
    visited_set = set()

    gx, gy = nodes_data[goal]

    while pq:
        _, current = heapq.heappop(pq)

        if current == goal:
            break

        if current in visited_set:
            continue

        visited_set.add(current)

        # Call callback for visualization (no sleep here)
        if callback:
            callback(current, visited_set.copy())

        for neighbor in graph.neighbors(current):
            edge_data = graph.get_edge_data(current, neighbor)[0]
            weight = edge_data.get("length", 1)

            new_g = g_score[current] + weight

            if neighbor not in g_score or new_g < g_score[neighbor]:
                parent[neighbor] = current
                g_score[neighbor] = new_g

                # heuristic: euclidean distance
                nx_lat, nx_lon = nodes_data[neighbor]
                dist = math.sqrt((nx_lat - gx) ** 2 + (nx_lon - gy) ** 2) * 111000

                f_score = new_g + dist
                heapq.heappush(pq, (f_score, neighbor))

    return reconstruct_path(parent, goal), len(visited_set)
