import pygame
from .colors import *
from .config import *


class UIComponents:

    def __init__(self, screen, grid_width, grid_height):
        self.screen = screen
        self.grid_width = grid_width
        self.grid_height = grid_height

        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 20)
        self.title_font = pygame.font.Font(None, 28)

    def draw_panel(self, buttons, current_algorithm, metrics):
        # Background
        panel_rect = pygame.Rect(self.grid_width, 0, PANEL_WIDTH, self.grid_height)
        pygame.draw.rect(self.screen, PANEL_BG, panel_rect)

        # Title
        title = self.title_font.render("Controls", True, TEXT_COLOR)
        self.screen.blit(title, (self.grid_width + BUTTON_PADDING, 15))

        # Draw buttons
        self._draw_buttons(buttons, current_algorithm)

        self._draw_info_panel(metrics)
    
    def _draw_info_panel(self, metrics):
        """Draw info panel."""
        info_panel_rect = pygame.Rect(0, self.grid_height, self.grid_width + PANEL_WIDTH, INFO_PANEL_HEIGHT)
        pygame.draw.rect(self.screen, PANEL_BG, info_panel_rect)

        # Draw metrics
        if metrics:
            self._draw_metrics(metrics)

        # Draw legend
        self._draw_legend()

    def _draw_buttons(self, buttons, current_algorithm):
        """Draw algorithm and control buttons."""
        mouse_pos = pygame.mouse.get_pos()

        button_labels = {
            'astar': 'A* Search',
            'bfs': 'BFS',
            'dfs': 'DFS',
            'ucs': 'UCS',
            'dls': 'DLS',
            'ids': 'IDS',
            'reset': 'Reset',
            'new_grid': 'New Grid'
        }

        for name, rect in buttons.items():
            # Determine button color
            is_hover = rect.collidepoint(mouse_pos)
            is_selected = name == current_algorithm.lower().replace(" ", "").replace("*", "")

            if is_selected and name in ALGORITHMS:
                color = BUTTON_SELECTED
            elif is_hover:
                color = BUTTON_HOVER
            else:
                color = BUTTON_COLOR

            # Draw button
            pygame.draw.rect(self.screen, color, rect, border_radius=5)

            # Draw button text
            label = self.small_font.render(button_labels[name], True, WHITE)
            label_rect = label.get_rect(center=rect.center)
            self.screen.blit(label, label_rect)

    def _draw_metrics(self, metrics):
        """Draw performance metrics."""
        y_offset = self.grid_height + 20

        metrics_title = self.font.render("Metrics", True, TEXT_COLOR)
        self.screen.blit(metrics_title, (self.grid_width * 0.5 + BUTTON_PADDING, y_offset))
        y_offset += 30

        # Format metrics text
        if metrics["path_found"]:
            metrics_text = [
                f"Algorithm: {metrics['algorithm']}",
                f"Path: {metrics['path_length']} steps",
                f"Expanded: {metrics['nodes_expanded']}",
                f"Memory: {metrics['max_nodes_in_memory']}",
                f"Optimal: {'Yes' if metrics['is_optimal'] else 'No'}"
            ]
        else:
            metrics_text = [
                f"Algorithm: {metrics['algorithm']}",
                "No path found!",
                f"Expanded: {metrics['nodes_expanded']}",
                f"Memory: {metrics['max_nodes_in_memory']}"
            ]

        for text in metrics_text:
            surf = self.small_font.render(text, True, TEXT_COLOR)
            self.screen.blit(surf, (self.grid_width * 0.5 + BUTTON_PADDING, y_offset))
            y_offset += 25

    def _draw_legend(self):
        """Draw color legend."""
        legend_y = self.grid_height + 20
        legend_title = self.font.render("Legend", True, TEXT_COLOR)
        self.screen.blit(legend_title, (BUTTON_PADDING, legend_y))
        legend_y += 30

        legend_items = [
            (GREEN, "Start"),
            (RED, "Goal"),
            (DARK_GRAY, "Wall"),
            (BLUE, "Visited"),
            (YELLOW, "Path")
        ]

        for color, label in legend_items:
            pygame.draw.rect(self.screen, color,
                           (BUTTON_PADDING, legend_y, 20, 20))
            text = self.small_font.render(label, True, TEXT_COLOR)
            self.screen.blit(text, (BUTTON_PADDING + 30, legend_y))
            legend_y += 25

    def draw_grid(self, grid, visited, path, cell_size):
        """Draw the grid with cells, obstacles, start, and goal."""
        rows = grid.rows
        cols = grid.cols

        for row in range(rows):
            for col in range(cols):
                x = col * cell_size
                y = row * cell_size
                rect = pygame.Rect(x, y, cell_size, cell_size)

                pos = (row, col)

                # Determine cell color
                if pos == grid.start:
                    color = GREEN
                elif pos == grid.goal:
                    color = RED
                elif pos in grid.obstacles:
                    color = DARK_GRAY
                elif pos in path:
                    color = YELLOW
                elif pos in visited:
                    color = BLUE
                else:
                    color = WHITE

                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, BORDER_COLOR, rect, 1)


def create_buttons(grid_width):
    """Create UI buttons and return their rectangles."""
    x = grid_width + BUTTON_PADDING
    y_start = 60
    button_width = PANEL_WIDTH - (BUTTON_PADDING * 2)

    buttons = {
        'astar': pygame.Rect(x, y_start, button_width, BUTTON_HEIGHT),
        'bfs': pygame.Rect(x, y_start + (BUTTON_HEIGHT + BUTTON_SPACING), button_width, BUTTON_HEIGHT),
        'dfs': pygame.Rect(x, y_start + 2*(BUTTON_HEIGHT + BUTTON_SPACING), button_width, BUTTON_HEIGHT),
        'ucs': pygame.Rect(x, y_start + 3*(BUTTON_HEIGHT + BUTTON_SPACING), button_width, BUTTON_HEIGHT),
        'dls': pygame.Rect(x, y_start + 4*(BUTTON_HEIGHT + BUTTON_SPACING), button_width, BUTTON_HEIGHT),
        'ids': pygame.Rect(x, y_start + 5*(BUTTON_HEIGHT + BUTTON_SPACING), button_width, BUTTON_HEIGHT),
        'reset': pygame.Rect(x, y_start + 6*(BUTTON_HEIGHT + BUTTON_SPACING) + 20, button_width, BUTTON_HEIGHT),
        'new_grid': pygame.Rect(x, y_start + 7*(BUTTON_HEIGHT + BUTTON_SPACING) + 20, button_width, BUTTON_HEIGHT),
    }

    return buttons
