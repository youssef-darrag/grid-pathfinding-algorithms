from typing import  Optional
from ..grid import Grid
from ..utils import Node, Direction, reconstruct_path, calculate_metrics

def iterative_deepening_search(grid: Grid, max_depth: int = 50, callback=None) -> dict:

    nodes_expanded_total = 0
    max_nodes_in_memory_total = 0
    path = None

    visited = set()

    def depth_limited_search(current_node: Node, depth: int) -> Optional[Node]:
        nonlocal nodes_expanded
        nodes_expanded += 1

        visited.add(current_node.position)
        if callback:
            callback(visited.copy())

        if current_node.position == grid.goal:
            return current_node
        if depth <= 0:
            return None

        for move in [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]:
            new_pos = (current_node.position[0] + move.value[0],
                       current_node.position[1] + move.value[1])

            if grid.is_valid_position(new_pos):
                child_node = Node(position=new_pos, parent=current_node, action=move)
                result = depth_limited_search(child_node, depth - 1)
                if result is not None:
                    return result
        return None

    # Iterative deepening loop
    for depth in range(max_depth + 1):
        nodes_expanded = 0
        result_node = depth_limited_search(Node(grid.start), depth)
        max_nodes_in_memory_total = max(max_nodes_in_memory_total, nodes_expanded)
        nodes_expanded_total += nodes_expanded

        if result_node is not None:
            path = reconstruct_path(result_node)
            break

    metrics = calculate_metrics(
        algorithm_name="Iterative Deepening Search",
        nodes_expanded=nodes_expanded_total,
        max_nodes_in_memory=max_nodes_in_memory_total,
        path=path,
        optimal_path_length=len(path) - 1 if path else 0  # assume found path is optimal for IDS
    )
    return metrics


if __name__ == "__main__":
    g = Grid(rows=6, cols=6, obstacle_percent=0.2)
    g.print_grid()
    metrics = iterative_deepening_search(g, max_depth=20)
    # print_metrics(metrics)
    if metrics['path_found']:
        g.print_grid(path=metrics['path'])
