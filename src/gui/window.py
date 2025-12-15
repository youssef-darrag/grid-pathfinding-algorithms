import tkinter as tk
from tkinter import ttk, messagebox
import tkintermapview
import time

from algorithms import ALGORITHMS, COMPARE_MODE, run_algorithm
from core.map import Map


class PathfinderWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Map Pathfinding Visualizer")
        self.root.geometry("1280x720")

        self.map = Map()
        self.start_node = None
        self.goal_node = None

        self._setup_ui()
        self.root.after(100, lambda: self.load_map_action(force=False))

    def load_map_action(self, force=False):
        place = self.loc_entry.get()
        self._set_status(f"Loading {place}...")
        self.root.update()

        success, msg = self.map.load_map(place, force)

        print(success, msg)

        if success:
            # Center view
            center = self.map.node_keys[0]
            lat, lon = self.map.get_node_coords(center)
            self.map_widget.set_position(lat, lon)
            self.map_widget.set_zoom(9)
            self.run_btn.config(state="normal")
            self._set_status(f"✅ {msg}")
        else:
            self._set_status("❌ Load failed.")
            messagebox.showerror("Error", msg)

    def randomize_action(self):
        if not self.map.graph:
            return

        self.start_node, self.goal_node = self.map.get_random_endpoints()

        # Clear map
        self.map_widget.delete_all_marker()
        self.map_widget.delete_all_path()

        # Draw markers
        s_pos = self.map.get_node_coords(self.start_node)
        g_pos = self.map.get_node_coords(self.goal_node)

        self.map_widget.set_marker(
            s_pos[0],
            s_pos[1],
            text="Start",
            text_color="green",
            marker_color_circle="green",
        )
        self.map_widget.set_marker(
            g_pos[0], g_pos[1], text="Goal", text_color="red", marker_color_circle="red"
        )
        self._set_status("Points randomized.")

    def run_pathfinding(self):
        if not self.start_node or not self.goal_node:
            return

        algo = self.algo_var.get()
        self.map_widget.delete_all_path()
        self.root.update()

        if algo == COMPARE_MODE:
            self._run_comparison()
        else:
            result = self._run_single_algorithm(algo)
            self._display_comparison_stats([result])

    def _run_single_algorithm(self, algo, color="blue", width=5):
        start_time = time.perf_counter()

        # Run Algorithm
        path, visited = run_algorithm(
            algo,
            self.map.graph,
            self.start_node,
            self.goal_node,
            self.map.node_coords,
        )

        duration = (time.perf_counter() - start_time) * 1000

        result = {
            "name": algo,
            "time_ms": duration,
            "visited": visited,
            "length_km": None,
            "path_nodes": 0,
            "color": color,
        }

        if path:
            coords = self.map.get_path_coords(path)
            self.map_widget.set_path(coords, color=color, width=width)
            length = self.map.get_path_length(path)
            result["length_km"] = length / 1000
            result["path_nodes"] = len(path)

        return result

    def _run_comparison(self):
        colors = ["blue", "red", "green", "purple"]
        results = []

        for i, name in enumerate(ALGORITHMS.keys()):
            result = self._run_single_algorithm(
                name, color=colors[i % len(colors)], width=3
            )
            results.append(result)

        self._display_comparison_stats(results)

    def _setup_ui(self):
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # -- Map Section --
        self.map_frame = tk.Frame(self.root)
        self.map_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.map_widget = tkintermapview.TkinterMapView(self.map_frame, corner_radius=0)
        self.map_widget.set_tile_server(
            "https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga",
            max_zoom=22,
        )
        self.map_widget.pack(fill="both", expand=True)

        # -- Controls Section --
        self.controls = ttk.LabelFrame(self.root, text="Controls", padding=15)
        self.controls.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
        self.controls.columnconfigure(1, weight=1)

        # Inputs
        ttk.Label(self.controls, text="Location:").grid(row=0, column=0, sticky="w")
        self.loc_entry = ttk.Entry(self.controls, width=30)
        self.loc_entry.insert(0, "Cairo, Egypt")
        self.loc_entry.grid(row=0, column=1, sticky="w", padx=5)

        ttk.Button(
            self.controls,
            text="Reload Map (Online)",
            command=lambda: self.load_map_action(force=True),
        ).grid(row=0, column=2)

        # Algo Select
        ttk.Label(self.controls, text="Algorithm:").grid(row=1, column=0, sticky="w")
        self.algo_var = tk.StringVar(value=list(ALGORITHMS.keys())[0])
        self.algo_box = ttk.Combobox(
            self.controls,
            textvariable=self.algo_var,
            values=list(ALGORITHMS.keys()) + [COMPARE_MODE],
            state="readonly",
        )
        self.algo_box.grid(row=1, column=1, sticky="w", padx=5)

        # Action Buttons
        btn_frame = ttk.Frame(self.controls)
        btn_frame.grid(row=2, column=0, columnspan=3, pady=10, sticky="ew")
        ttk.Button(
            btn_frame, text="📍 Randomize Points", command=self.randomize_action
        ).pack(side="left", padx=5)
        self.run_btn = ttk.Button(
            btn_frame, text="▶ START", command=self.run_pathfinding, state="disabled"
        )
        self.run_btn.pack(side="left", fill="x", expand=True, padx=5)

        # stats frame
        self.stats_frame = ttk.LabelFrame(self.controls, text="Statistics", padding=5)
        self.stats_frame.grid(row=3, column=0, columnspan=3, sticky="ew", pady=(5, 0))

        self.stats_text = tk.Text(
            self.stats_frame, height=5, font=("Consolas", 10), state="disabled"
        )
        self.stats_text.pack(fill="x", expand=True)

    def _display_comparison_stats(self, results):
        self.stats_text.config(state="normal")
        self.stats_text.delete("1.0", tk.END)

        header = f"{'Algorithm':<10} {'Time (ms)':<12} {'Visited':<10} {'Path Nodes':<12} {'Distance (km)':<15} {'Color'}\n"
        self.stats_text.insert(tk.END, header)
        self.stats_text.insert(tk.END, "-" * 70 + "\n")

        for r in results:
            if r["length_km"]:
                line = f"{r['name']:<10} {r['time_ms']:<12.2f} {r['visited']:<10} {r['path_nodes']:<12} {r['length_km']:<15.2f} {r['color']}\n"
            else:
                line = f"{r['name']:<10} {r['time_ms']:<12.2f} {r['visited']:<10} {'N/A':<12} {'No path':<15} {r['color']}\n"
            self.stats_text.insert(tk.END, line)

        self.stats_text.config(state="disabled")

    def _set_status(self, text):
        self.stats_text.config(state="normal")
        self.stats_text.delete("1.0", tk.END)
        self.stats_text.insert(tk.END, text)
        self.stats_text.config(state="disabled")
