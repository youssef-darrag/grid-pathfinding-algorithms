import heapq
import math
from networkx import MultiDiGraph
from core.utils import reconstruct_path


def astar(
    graph: MultiDiGraph,
    start: int,
    goal: int,
    nodes_data: dict[int, tuple[float, float]],
):
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

        for neighbor in graph.neighbors(current):
            edge_data = graph.get_edge_data(current, neighbor)[0]
            weight = edge_data.get("length", 1)

            new_g = g_score[current] + weight

            if neighbor not in g_score or new_g < g_score[neighbor]:
                parent[neighbor] = current
                g_score[neighbor] = new_g

                # heuristic: euclidean distance
                nx_lat, nx_lon = nodes_data[neighbor]

                # *111000 converts rough degrees difference to meters
                dist = math.sqrt((nx_lat - gx) ** 2 + (nx_lon - gy) ** 2) * 111000

                f_score = new_g + dist
                heapq.heappush(pq, (f_score, neighbor))

    return reconstruct_path(parent, goal), len(visited_set)
