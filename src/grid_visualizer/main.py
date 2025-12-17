import pygame

from .grid import Grid
from .colors import BLACK
from .config import DEFAULT_CELL_SIZE, DEFAULT_GRID_ROWS, DEFAULT_GRID_COLS, DEFAULT_OBSTACLE_PERCENT, PANEL_WIDTH, DEFAULT_ANIMATION_SPEED, FPS, INFO_PANEL_HEIGHT
from .ui_components import UIComponents, create_buttons
from .algorithm_runner import AlgorithmRunner


class PathfindingVisualizer:

    def __init__(self, cell_size=DEFAULT_CELL_SIZE, grid_rows=DEFAULT_GRID_ROWS, grid_cols=DEFAULT_GRID_COLS):
        pygame.init()

        self.cell_size = cell_size
        self.grid_rows = grid_rows
        self.grid_cols = grid_cols

        # Calculate window dimensions
        self.grid_width = grid_cols * cell_size
        self.grid_height = grid_rows * cell_size
        self.window_width = self.grid_width + PANEL_WIDTH
        self.window_height = self.grid_height + INFO_PANEL_HEIGHT

        # Create window
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Grid Pathfinding Visualizer")

        # Create grid
        self.grid = Grid(rows=grid_rows, cols=grid_cols, obstacle_percent=DEFAULT_OBSTACLE_PERCENT)

        # Initialize components
        self.ui = UIComponents(self.screen, self.grid_width, self.grid_height)
        self.algorithm_runner = AlgorithmRunner(
            self.grid,
            self.screen,
            self.ui,
            self.cell_size,
            DEFAULT_ANIMATION_SPEED
        )

        # State
        self.current_algorithm = "A*"
        self.is_running = False

        # UI elements
        self.buttons = create_buttons(self.grid_width)

        self.clock = pygame.time.Clock()

    def visualize_algorithm(self, algorithm_name):
        self.algorithm_runner.reset()
        self.current_algorithm = algorithm_name
        self.is_running = True

        if algorithm_name == "A*":
            self.algorithm_runner.run_astar(self.buttons, self.current_algorithm)
        elif algorithm_name == "BFS":
            self.algorithm_runner.run_bfs(self.buttons, self.current_algorithm)
        elif algorithm_name == "DFS":
            self.algorithm_runner.run_dfs(self.buttons, self.current_algorithm)
        elif algorithm_name == "UCS":
            self.algorithm_runner.run_ucs(self.buttons, self.current_algorithm)
        elif algorithm_name == "DLS":
            self.algorithm_runner.run_dls(self.buttons, self.current_algorithm)
        elif algorithm_name == "IDS":
            self.algorithm_runner.run_ids(self.buttons, self.current_algorithm)

        self.is_running = False

    def reset(self):
        self.algorithm_runner.reset()

    def new_grid(self):
        self.grid = Grid(rows=self.grid_rows, cols=self.grid_cols, obstacle_percent=DEFAULT_OBSTACLE_PERCENT)
        self.algorithm_runner.grid = self.grid
        self.reset()

    def handle_button_click(self, mouse_pos):
        if self.buttons['astar'].collidepoint(mouse_pos):
            self.visualize_algorithm("A*")
        elif self.buttons['bfs'].collidepoint(mouse_pos):
            self.visualize_algorithm("BFS")
        elif self.buttons['dfs'].collidepoint(mouse_pos):
            self.visualize_algorithm("DFS")
        elif self.buttons['ucs'].collidepoint(mouse_pos):
            self.visualize_algorithm("UCS")
        elif self.buttons['dls'].collidepoint(mouse_pos):
            self.visualize_algorithm("DLS")
        elif self.buttons['ids'].collidepoint(mouse_pos):
            self.visualize_algorithm("IDS")
        elif self.buttons['reset'].collidepoint(mouse_pos):
            self.reset()
        elif self.buttons['new_grid'].collidepoint(mouse_pos):
            self.new_grid()

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN and not self.is_running:
                    mouse_pos = pygame.mouse.get_pos()
                    self.handle_button_click(mouse_pos)

            # Draw everything
            self.screen.fill(BLACK)
            self.ui.draw_grid(
                self.grid,
                self.algorithm_runner.visited,
                self.algorithm_runner.path,
                self.cell_size
            )
            self.ui.draw_panel(
                self.buttons,
                self.current_algorithm,
                self.algorithm_runner.metrics
            )
            pygame.display.flip()
            self.clock.tick(FPS)
        pygame.quit()
