import heapq
#..
class UniformCostSearch:
    def __init__(self, grid):
        self.grid = grid

    def search(self, callback=None):
        start = self.grid.start
        goal = self.grid.goal

        frontier = []
        heapq.heappush(frontier, (0, start))

        visited = set()
        parent = {start: None}
        cost_so_far = {start: 0}

        while frontier:
            current_cost, current_pos = heapq.heappop(frontier)

            if current_pos == goal:
                return self._reconstruct_path(parent)

            if current_pos in visited:
                continue
            visited.add(current_pos)

            if callback:
                callback(visited.copy())

            for neighbor in self.grid.get_neighbors(current_pos):
                new_cost = current_cost + 1
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    parent[neighbor] = current_pos
                    heapq.heappush(frontier, (new_cost, neighbor))

        return None

    def _reconstruct_path(self, parent):
        path = []
        current = self.grid.goal
        while current is not None:
            path.append(current)
            current = parent[current]
        path.reverse()
        return path
