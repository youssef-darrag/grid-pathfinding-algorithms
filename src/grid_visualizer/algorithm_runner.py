# To be completed later
import pygame
from typing import Set, List, Tuple, Dict, Optional

from grid_visualizer.grid_algorithms.astar import AStarSearch
from grid_visualizer.grid_algorithms.dfs import dfs
from grid_visualizer.grid_algorithms.bfs import breadth_first_search
from grid_visualizer.grid_algorithms.dls import dls
from grid_visualizer.grid_algorithms.ids import iterative_deepening_search
from grid_visualizer.grid_algorithms.ucs import UniformCostSearch

from .colors import BLACK


class AlgorithmRunner:
    def __init__(self, grid, screen, ui, cell_size, animation_speed):
        self.grid = grid
        self.screen = screen
        self.ui = ui
        self.cell_size = cell_size
        self.animation_speed = animation_speed

        self.visited: Set[Tuple[int, int]] = set()
        self.path: List[Tuple[int, int]] = []
        self.metrics: Optional[Dict] = None

    def reset(self):
        self.visited.clear()
        self.path.clear()
        self.metrics = None

    def _animate_step(self, buttons, current_algorithm):
        self.screen.fill(BLACK)
        self.ui.draw_grid(self.grid, self.visited, self.path, self.cell_size)
        self.ui.draw_panel(buttons, current_algorithm, self.metrics)
        pygame.display.flip()
        pygame.time.delay(self.animation_speed)

    def _animate_path(self, path: List[Tuple[int, int]], buttons, current_algorithm):
        for pos in path:
            self.path.append(pos)
            self._animate_step(buttons, current_algorithm)

    def run_astar(self, buttons, current_algorithm):
        def visualize(new_visited):
            self.visited = new_visited
            self._animate_step(buttons, current_algorithm)

        astar = AStarSearch(self.grid)
        path, metrics = astar.search(callback=visualize)
        self.metrics = metrics
        if path:
            self._animate_path(path, buttons, current_algorithm)

    def run_bfs(self, buttons, current_algorithm):
        def visualize(new_visited):
            self.visited = new_visited
            self._animate_step(buttons, current_algorithm)

        result = breadth_first_search(self.grid, callback=visualize)
        self.metrics = result
        self._animate_path(result["path"], buttons, current_algorithm)

    def run_dfs(self, buttons, current_algorithm):
        nodes_expanded = 0
        # inaccurate but who cares at this point anyway
        max_nodes_in_memory = 0

        def visualize(new_visited):
            nonlocal nodes_expanded, max_nodes_in_memory
            nodes_expanded = len(new_visited)
            max_nodes_in_memory = max(max_nodes_in_memory, len(new_visited))
            self.visited = new_visited
            self._animate_step(buttons, current_algorithm)

        path = dfs(self.grid, callback=visualize)

        self.metrics = {
            "algorithm": "Depth-First Search",
            "nodes_expanded": nodes_expanded,
            "max_nodes_in_memory": max_nodes_in_memory,
            "path_found": bool(path),
            "path_length": len(path) - 1 if path else 0,
            "is_optimal": False,
            "path": path,
        }

        self._animate_path(path, buttons, current_algorithm)

    def run_ucs(self, buttons, current_algorithm):
        nodes_expanded = 0
        # again, who cares
        max_nodes_in_memory = 0

        def visualize(new_visited):
            nonlocal nodes_expanded, max_nodes_in_memory
            nodes_expanded = len(new_visited)
            max_nodes_in_memory = max(max_nodes_in_memory, len(new_visited))
            self.visited = new_visited
            self._animate_step(buttons, current_algorithm)

        ucs = UniformCostSearch(self.grid)
        path = ucs.search(callback=visualize)

        self.metrics = {
            "algorithm": "Uniform Cost Search",
            "nodes_expanded": nodes_expanded,
            "max_nodes_in_memory": max_nodes_in_memory,
            "path_found": bool(path),
            "path_length": len(path) - 1 if path else 0,
            "is_optimal": True,
            "path": path,
        }

        self._animate_path(path, buttons, current_algorithm)

    def run_dls(self, buttons, current_algorithm, limit: int = 50):
        nodes_expanded = 0
        max_nodes_in_memory = 0

        def visualize(new_visited):
            nonlocal nodes_expanded, max_nodes_in_memory
            nodes_expanded = len(new_visited)
            max_nodes_in_memory = max(max_nodes_in_memory, len(new_visited))
            self.visited = new_visited
            self._animate_step(buttons, current_algorithm)

        path = dls(self.grid, limit, callback=visualize)

        self.metrics = {
            "algorithm": "Depth-Limited Search",
            "nodes_expanded": nodes_expanded,
            "max_nodes_in_memory": max_nodes_in_memory,
            "path_found": bool(path),
            "path_length": len(path) - 1 if path else 0,
            "is_optimal": False,
            "path": path,
        }

        if path:
            self._animate_path(path, buttons, current_algorithm)

    def run_ids(self, buttons, current_algorithm):
        def visualize(new_visited):
            self.visited = new_visited
            self._animate_step(buttons, current_algorithm)

        metrics = iterative_deepening_search(self.grid, callback=visualize)
        self.metrics = metrics
        self._animate_path(metrics["path"], buttons, current_algorithm)
