"""
Modified __init__.py for algorithms with animation support

Add this to: src/algorithms/__init__.py
"""

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
    callback=None,  # NEW: callback for visualization
    delay: float = 0.0,  # NEW: delay in seconds
):
    """
    Run pathfinding algorithm with optional animation.

    Args:
        algorithm_name: Name of algorithm to run
        graph: Road network graph
        start_node: Starting node ID
        goal_node: Goal node ID
        node_coords: Dictionary of node coordinates
        callback: Optional function called after each step with (current_node, visited_set)
        delay: Optional delay in seconds between steps (for animation)

    Returns:
        tuple: (path, nodes_explored)
    """
    algorithm = ALGORITHMS.get(algorithm_name)

    if not algorithm:
        raise ValueError(f"Algorithm {algorithm_name} not found")

    if algorithm_name == "A*":
        return algorithm(graph, start_node, goal_node, node_coords, callback, delay)

    return algorithm(graph, start_node, goal_node, callback, delay)
