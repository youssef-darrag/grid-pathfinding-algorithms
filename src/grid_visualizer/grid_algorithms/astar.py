import heapq
from typing import List, Tuple, Dict, Optional
from ..grid import Grid
from ..utils import Node, reconstruct_path

#! This uses euclidean distance

class AStarSearch:
    def __init__(self, grid: Grid):
        self.grid = grid

    def search(self, callback=None) -> Tuple[Optional[List[Tuple[int, int]]], Dict]:
        start = self.grid.start
        goal = self.grid.goal

        # Performance tracking
        nodes_expanded = 0
        max_memory = 0
        current_memory = 0

        # Frontier: (f_score, Node)
        frontier = []

        # Create start node
        start_node = Node(
            position=start,
            parent=None,
            cost=0,  # g(n)
            heuristic=self.grid.euclidean_distance(start, goal)  # h(n)
        )


        heapq.heappush(frontier, (start_node.total_cost, start_node))
        g_scores = {start: 0}
        nodes_in_memory = {start}
        current_memory = 1
        max_memory = 1

        # Map positions to Node objects for easy access
        node_map = {start: start_node}

        visited = set()

        while frontier:
            # Update max memory
            current_memory = len(nodes_in_memory)
            max_memory = max(max_memory, current_memory)

            # Get node with lowest f_score
            _, current_node = heapq.heappop(frontier)
            current_pos = current_node.position

            if current_pos in visited:
                continue

            visited.add(current_pos)

            if callback:
                callback(visited.copy())

            # Remove from memory tracking
            if current_pos in nodes_in_memory:
                nodes_in_memory.remove(current_pos)

            # Track node expansion
            nodes_expanded += 1

            # Check if goal reached
            if current_pos == goal:
                path = reconstruct_path(current_node)

                metrics = {
                    "algorithm": "A* Search",
                    "nodes_expanded": nodes_expanded,
                    "max_nodes_in_memory": max_memory,
                    "path_found": True,
                    "path_length": len(path) - 1,
                    "is_optimal": True,
                    "path": path
                }
                return path, metrics

            # Explore neighbors
            for neighbor_pos in self.grid.get_neighbors(current_pos):
                # Calculate tentative g_score (current cost + 1)
                tentative_g_score = g_scores[current_pos] + 1

                # If neighbor not visited or found better path
                if neighbor_pos not in g_scores or tentative_g_score < g_scores[neighbor_pos]:
                    # Update g_score
                    g_scores[neighbor_pos] = tentative_g_score

                    # Calculate heuristic (h(n))
                    h_score = self.grid.euclidean_distance(neighbor_pos, goal)

                    # Create neighbor node
                    neighbor_node = Node(
                        position=neighbor_pos,
                        parent=current_node,
                        cost=tentative_g_score,
                        heuristic=h_score
                    )

                    # Add to frontier
                    heapq.heappush(frontier, (neighbor_node.total_cost, neighbor_node))
                    node_map[neighbor_pos] = neighbor_node

                    # Track memory
                    if neighbor_pos not in nodes_in_memory:
                        nodes_in_memory.add(neighbor_pos)

        # No path found
        metrics = {
            "algorithm": "A* Search",
            "nodes_expanded": nodes_expanded,
            "max_nodes_in_memory": max_memory,
            "path_found": False,
            "path_length": 0,
            "is_optimal": False,
            "path": None
        }
        return None, metrics

    def run(self, verbose: bool = True) -> Dict:
        """
        Run A* search and return results.

        Args:
            verbose: Print results if True

        Returns:
            Dictionary with complete results
        """
        path, metrics = self.search()

        if verbose:
            self._print_results(metrics)

        return metrics

    def _print_results(self, metrics: Dict):
        """Print search results in readable format."""
        print("\n" + "=" * 50)
        print("A* SEARCH RESULTS")
        print("=" * 50)

        if not metrics["path_found"]:
            print("❌ No path found!")
        else:
            print(f"✅ Path found: {metrics['path_length']} steps")
            print(f"📊 Nodes expanded: {metrics['nodes_expanded']}")
            print(f"💾 Max nodes in memory: {metrics['max_nodes_in_memory']}")
            print(f"🎯 Optimal path: {'Yes' if metrics['is_optimal'] else 'No'}")

            if metrics["path"] and len(metrics["path"]) <= 20:
                print(f"\n📍 Path: {' → '.join(str(p) for p in metrics['path'])}")

        print("=" * 50)


# Convenience function
def a_star_search(grid: Grid, verbose: bool = True) -> Tuple[Optional[List[Tuple[int, int]]], Dict]:
    """
    Convenience function to run A* search.

    Args:
        grid: Grid object
        verbose: Print results if True

    Returns:
        Tuple of (path, metrics)
    """
    astar = AStarSearch(grid)
    return astar.search()


# Test function
def test_astar():
    """Test A* algorithm."""
    print("🧪 Testing A* Search Algorithm")
    print("-" * 40)

    # Create test grid
    grid = Grid(rows=8, cols=8, obstacle_percent=0.2)

    # Print grid info
    print(f"Grid: {grid.rows}×{grid.cols}")
    print(f"Start: {grid.start}, Goal: {grid.goal}")
    print(f"Euclidean distance: {grid.euclidean_distance(grid.start, grid.goal)}")

    # Run A*
    astar = AStarSearch(grid)
    results = astar.run(verbose=True)

    # Show grid with path
    if results["path_found"]:
        grid.print_grid(results["path"])

    return results


