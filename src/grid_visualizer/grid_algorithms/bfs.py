from collections import deque
from ..utils import Node, Direction, reconstruct_path, calculate_metrics
from ..grid import Grid


def breadth_first_search(grid: Grid, callback=None):
    start_node = Node(position=grid.start)
    goal_position = grid.goal

    frontier = deque([start_node])
    explored = set()

    nodes_expanded = 0
    max_nodes_in_memory = 1

    while frontier:
        max_nodes_in_memory = max(max_nodes_in_memory, len(frontier) + len(explored))
        current_node = frontier.popleft()
        nodes_expanded += 1

        if current_node.position == goal_position:
            path = reconstruct_path(current_node)
            return calculate_metrics(
                algorithm_name="Breadth-First Search",
                nodes_expanded=nodes_expanded,
                max_nodes_in_memory=max_nodes_in_memory,
                path=path,
                optimal_path_length=len(path)-1
            )

        explored.add(current_node.position)

        if callback:
            callback(explored.copy())

        for direction in Direction:
            dr, dc = direction.value
            r, c = current_node.position
            next_pos = (r + dr, c + dc)

            if grid.is_valid_position(next_pos) and next_pos not in explored and next_pos not in [n.position for n in frontier]:
                child_node = Node(
                    position=next_pos,
                    parent=current_node,
                    action=direction,
                    cost=current_node.cost + 1
                )
                frontier.append(child_node)

    # No path found
    return calculate_metrics(
        algorithm_name="Breadth-First Search",
        nodes_expanded=nodes_expanded,
        max_nodes_in_memory=max_nodes_in_memory,
        path=[],
        optimal_path_length=0
    )


if __name__ == "__main__":
    g = Grid()
    result = breadth_first_search(g)

    # print_metrics(result)

    g.print_grid(result['path'])
