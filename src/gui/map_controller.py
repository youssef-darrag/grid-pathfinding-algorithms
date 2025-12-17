"""
Map Controller - Handles map interactions and node selection
"""

import math
from tkinter import messagebox
from core.map import Map
from core.map_diagnostics import check_connectivity, find_valid_endpoints


class MapController:
    """Manages map state and interactions."""

    def __init__(self, map_widget):
        self.map_widget = map_widget
        self.map = Map()

        # State
        self.start_node = None
        self.goal_node = None
        self.click_mode = "start"  # 'start' or 'goal'

        # Markers
        self.start_marker = None
        self.goal_marker = None
        self.debug_markers = []
        self.current_paths = []

    def load_map(self, location, force_download=False):
        """Load map data for given location."""
        success, msg = self.map.load_map(location, force_download)

        if success:
            # Center view on first node
            center = self.map.node_keys[0]
            lat, lon = self.map.get_node_coords(center)
            self.map_widget.set_position(lat, lon)
            self.map_widget.set_zoom(12)

        return success, msg

    def find_nearest_node(self, lat, lon):
        """Find the nearest graph node to given coordinates."""
        min_dist = float('inf')
        nearest = None

        for node_id in self.map.node_keys:
            n_lat, n_lon = self.map.get_node_coords(node_id)
            dist = self._haversine_distance(lat, lon, n_lat, n_lon)
            if dist < min_dist:
                min_dist = dist
                nearest = node_id

        return nearest

    def handle_map_click(self, coords, debug_mode=False):
        """
        Handle map click to select start/goal.
        Returns: (success, status_message)
        """
        lat, lon = coords

        # Show debug marker if enabled
        click_marker = None
        if debug_mode:
            click_marker = self.map_widget.set_marker(
                lat, lon,
                text="📍 CLICK",
                marker_color_circle="yellow",
                marker_color_outside="orange",
            )
            self.debug_markers.append(click_marker)

        # Find nearest node
        nearest_node = self.find_nearest_node(lat, lon)

        if not nearest_node:
            if click_marker and not debug_mode:
                click_marker.delete()
            return False, "Could not find nearest road node!"

        node_lat, node_lon = self.map.get_node_coords(nearest_node)
        snap_distance = self._haversine_distance(lat, lon, node_lat, node_lon)

        # Warn if far from road
        if snap_distance > 1.0:
            result = messagebox.askyesno(
                "Far from Road",
                f"Nearest road is {snap_distance:.2f} km away.\n"
                f"Continue anyway?"
            )
            if not result:
                if click_marker and not debug_mode:
                    click_marker.delete()
                return False, "Selection cancelled"

        # Remove temporary marker
        if click_marker and not debug_mode:
            click_marker.delete()

        # Set start or goal
        if self.click_mode == "start":
            return self._set_start(nearest_node, node_lat, node_lon, snap_distance)
        else:
            return self._set_goal(nearest_node, node_lat, node_lon, snap_distance)

    def _set_start(self, node_id, lat, lon, snap_distance):
        """Set start node."""
        self.start_node = node_id
        if self.start_marker:
            self.start_marker.delete()

        self.start_marker = self.map_widget.set_marker(
            lat, lon,
            text="START",
            text_color="white",
            marker_color_circle="green",
            marker_color_outside="darkgreen",
        )

        status = "✅ Start set"
        if snap_distance > 0.05:
            status += f" (snapped {snap_distance*1000:.0f}m)"
        status += " | Click to set GOAL"

        self.click_mode = "goal"
        return True, status

    def _set_goal(self, node_id, lat, lon, snap_distance):
        """Set goal node."""
        self.goal_node = node_id
        if self.goal_marker:
            self.goal_marker.delete()

        self.goal_marker = self.map_widget.set_marker(
            lat, lon,
            text="GOAL",
            text_color="white",
            marker_color_circle="red",
            marker_color_outside="darkred",
        )

        # Calculate distance
        s_lat, s_lon = self.map.get_node_coords(self.start_node)
        straight_dist = self._haversine_distance(s_lat, s_lon, lat, lon)

        status = "✅ Goal set"
        if snap_distance > 0.05:
            status += f" (snapped {snap_distance*1000:.0f}m)"
        status += f" | Distance: {straight_dist:.2f} km"

        self.click_mode = "start"
        return True, status

    def randomize_endpoints(self):
        """Randomly select start and goal from graph nodes."""
        if not self.map.graph:
            return False, "No map loaded"

        import random
        self.start_node, self.goal_node = self.map.get_random_endpoints()
        self._update_markers()

        # Calculate distance
        s_pos = self.map.get_node_coords(self.start_node)
        g_pos = self.map.get_node_coords(self.goal_node)
        dist = self._haversine_distance(s_pos[0], s_pos[1], g_pos[0], g_pos[1])

        return True, f"🎲 Points randomized | Distance: {dist:.2f} km"

    def smart_randomize_endpoints(self):
        """Find connected endpoints using graph analysis."""
        if not self.map.graph:
            return False, "No map loaded"

        start, goal, attempts = find_valid_endpoints(self.map.graph)

        if not start or not goal:
            return False, "Could not find connected points"

        self.start_node = start
        self.goal_node = goal
        self._update_markers()

        # Calculate distance
        s_pos = self.map.get_node_coords(self.start_node)
        g_pos = self.map.get_node_coords(self.goal_node)
        dist = self._haversine_distance(s_pos[0], s_pos[1], g_pos[0], g_pos[1])

        return True, f"✅ Connected points found (attempt {attempts}) | Distance: {dist:.2f} km"

    def _update_markers(self):
        """Update start/goal markers on map."""
        # Clear old markers
        if self.start_marker:
            self.start_marker.delete()
        if self.goal_marker:
            self.goal_marker.delete()

        # Add new markers
        s_pos = self.map.get_node_coords(self.start_node)
        g_pos = self.map.get_node_coords(self.goal_node)

        self.start_marker = self.map_widget.set_marker(
            s_pos[0], s_pos[1],
            text="START",
            text_color="white",
            marker_color_circle="green",
            marker_color_outside="darkgreen",
        )
        self.goal_marker = self.map_widget.set_marker(
            g_pos[0], g_pos[1],
            text="GOAL",
            text_color="white",
            marker_color_circle="red",
            marker_color_outside="darkred",
        )

    def check_path_exists(self):
        """Check if path exists between start and goal."""
        if not self.start_node or not self.goal_node:
            return False, None

        return check_connectivity(self.map.graph, self.start_node, self.goal_node)

    def clear_paths(self):
        """Clear all paths from map."""
        self.map_widget.delete_all_path()
        self.current_paths.clear()

    def clear_all(self):
        """Clear everything from map."""
        self.map_widget.delete_all_marker()
        self.map_widget.delete_all_path()
        self.start_marker = None
        self.goal_marker = None
        self.current_paths.clear()
        self.debug_markers.clear()
        self.start_node = None
        self.goal_node = None
        self.click_mode = "start"

    def _haversine_distance(self, lat1, lon1, lat2, lon2):
        """Calculate distance between two points in km."""
        R = 6371  # Earth radius in km
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (math.sin(dlat/2)**2 +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(dlon/2)**2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        return R * c

    def fit_bounds_to_path(self, coords):
        """Adjust map view to fit the path."""
        if not coords:
            return

        lats = [c[0] for c in coords]
        lons = [c[1] for c in coords]

        center_lat = (min(lats) + max(lats)) / 2
        center_lon = (min(lons) + max(lons)) / 2

        self.map_widget.set_position(center_lat, center_lon)

        # Calculate zoom
        lat_range = max(lats) - min(lats)
        lon_range = max(lons) - min(lons)
        max_range = max(lat_range, lon_range)

        if max_range < 0.01:
            zoom = 15
        elif max_range < 0.05:
            zoom = 13
        elif max_range < 0.1:
            zoom = 12
        elif max_range < 0.5:
            zoom = 10
        else:
            zoom = 9

        self.map_widget.set_zoom(zoom)
