from .dfs import dfs
from .bfs import bfs
from .ucs import ucs
from .dls import dls
from .ids import ids
from .astar import astar
from networkx import MultiDiGraph

ALGORITHMS = {
    "DFS": dfs,
    "BFS": bfs,
    "UCS": ucs,
    "A*": astar,
    "DLS": dls,
    "IDS": ids,
}

COMPARE_MODE = "Compare All"


def run_algorithm(
    algorithm_name: str,
    graph: MultiDiGraph,
    start_node: int,
    goal_node: int,
    node_coords: dict[int, tuple[float, float]],
):
    algorithm = ALGORITHMS.get(algorithm_name)

    if not algorithm:
        raise ValueError(f"Algorithm {algorithm_name} not found")

    if algorithm_name == "A*":
        return algorithm(graph, start_node, goal_node, node_coords)

    return algorithm(graph, start_node, goal_node)
