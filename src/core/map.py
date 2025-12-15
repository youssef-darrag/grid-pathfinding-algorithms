import os
import random
import osmnx as ox


class Map:
    def __init__(self, filename: str = "map_data.graphml"):
        self.filename = filename
        self.graph = None
        self.node_keys = []
        self.node_coords = {}

    def load_map(self, location: str, force_download: bool = False):
        try:
            if os.path.exists(self.filename) and not force_download:
                self.graph = ox.load_graphml(self.filename)
                status = "Loaded cached map data."
            else:
                self.graph = ox.graph_from_place(location, network_type="drive")
                ox.save_graphml(self.graph, self.filename)
                status = "Downloaded and cached new map data."

            self.node_keys = list(self.graph.nodes)
            self.node_coords = {
                n: (data["y"], data["x"]) for n, data in self.graph.nodes(data=True)
            }

            return True, status
        except Exception as e:
            return False, f"Error loading map: {e}"

    def get_random_endpoints(self):
        start = random.choice(self.node_keys)
        end = random.choice(self.node_keys)

        while end == start:
            end = random.choice(self.node_keys)

        return start, end

    def get_node_coords(self, nodeId: int):
        return self.node_coords[nodeId]

    def get_path_length(self, path: list[int]):
        total_length = 0
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            edge_data = self.graph.get_edge_data(u, v)[0]
            total_length += edge_data["length"]
        return total_length

    def get_path_coords(self, path: list[int]):
        coords = [self.node_coords[path[0]]]

        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]

            # Get edge data (0 is the key for the first edge)
            edge_data = self.graph.get_edge_data(u, v)[0]

            if "geometry" in edge_data:
                curve_points = [(lat, lon) for lon, lat in edge_data["geometry"].coords]
                coords.extend(curve_points)
            else:
                coords.append(self.node_coords[v])

        return coords
