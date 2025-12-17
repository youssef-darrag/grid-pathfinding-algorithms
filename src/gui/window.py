"""
Main Window - Simplified and modular with animation support
"""

import tkinter as tk
from tkinter import messagebox

from algorithms import COMPARE_MODE
from gui.map_controller import MapController
from gui.algorithm_executor import AlgorithmExecutor
from gui.ui_builder import UIBuilder
from core.map_diagnostics import get_graph_stats, format_diagnostic_report


class PathfinderWindow:
    """Main application window."""

    def __init__(self, root):
        self.root = root
        self.root.title("🗺️ Real-World Pathfinding Visualizer")
        self.root.geometry("1400x850")  # Slightly taller for animation controls

        # Configure grid
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Build UI
        self._setup_ui()

        # Initialize after UI is ready
        self.root.after(100, self._initial_load)

    def _setup_ui(self):
        """Setup the user interface."""
        # Create map widget
        self.map_widget = UIBuilder.create_map_widget(self.root)

        # Initialize controllers
        self.map_ctrl = MapController(self.map_widget)
        self.algo_exec = AlgorithmExecutor(self.map_ctrl, self.root)  # Pass root for UI updates

        # Create controls panel
        callbacks = {
            "on_reload_map": self._on_reload_map,
            "on_randomize": self._on_randomize,
            "on_smart_randomize": self._on_smart_randomize,
            "on_diagnose": self._on_diagnose,
            "on_run": self._on_run_pathfinding,
            "on_clear_paths": self._on_clear_paths,
            "on_clear_all": self._on_clear_all,
        }

        self.controls, self.widgets = UIBuilder.create_controls_panel(
            self.root, callbacks
        )

        # Set initial status
        self._set_status("👋 Welcome! Loading map...")

    def _initial_load(self):
        """Load map on startup."""
        self._load_map(force=False)

    def _load_map(self, force=False):
        """Load map data."""
        location = self.widgets["location_entry"].get()
        self._set_status(f"⏳ Loading {location}...")
        self.root.update()

        success, msg = self.map_ctrl.load_map(location, force)

        if success:
            # Enable controls
            self.widgets["run_btn"].config(state="normal")
            self.widgets["random_btn"].config(state="normal")
            self.widgets["smart_random_btn"].config(state="normal")
            self.widgets["diagnose_btn"].config(state="normal")

            # Enable map clicking
            self.map_widget.add_left_click_map_command(self._on_map_click)

            # Show stats
            stats = get_graph_stats(self.map_ctrl.map.graph)
            status = (
                f"✅ {msg} | "
                f"Nodes: {stats['nodes']:,} | "
                f"Edges: {stats['edges']:,} | "
                f"Components: {stats['weak_components']}"
            )
            if stats['weak_components'] > 1:
                status += " ⚠️"

            self._set_status(status)
        else:
            self._set_status("❌ Load failed")
            messagebox.showerror("Error", msg)

    # Event Handlers

    def _on_reload_map(self):
        """Handle reload map button."""
        self._load_map(force=True)

    def _on_map_click(self, coords):
        """Handle map click."""
        debug_mode = self.widgets["debug_var"].get()
        success, msg = self.map_ctrl.handle_map_click(coords, debug_mode)

        if success:
            self._set_status(msg)
            # Update mode label
            if self.map_ctrl.click_mode == "goal":
                self.widgets["mode_label"].config(
                    text="Mode: Setting GOAL 🎯", foreground="red"
                )
            else:
                self.widgets["mode_label"].config(
                    text="Mode: Setting START 🟢", foreground="green"
                )
        else:
            if "cancelled" not in msg.lower():
                messagebox.showerror("Error", msg)

    def _on_randomize(self):
        """Handle randomize button."""
        success, msg = self.map_ctrl.randomize_endpoints()
        self._set_status(msg)

    def _on_smart_randomize(self):
        """Handle smart randomize button."""
        self._set_status("🔍 Finding connected points...")
        self.root.update()

        success, msg = self.map_ctrl.smart_randomize_endpoints()

        if not success:
            messagebox.showerror(
                "Error",
                "Could not find connected points!\n"
                "The graph might be too fragmented."
            )

        self._set_status(msg)

    def _on_diagnose(self):
        """Handle diagnose button."""
        if not self.map_ctrl.map.graph:
            messagebox.showwarning("Warning", "Please load a map first!")
            return

        stats = get_graph_stats(self.map_ctrl.map.graph)

        if self.map_ctrl.start_node and self.map_ctrl.goal_node:
            is_connected, diagnostic = self.map_ctrl.check_path_exists()
            report = format_diagnostic_report(stats, diagnostic)
        else:
            report = format_diagnostic_report(stats)
            report += "\n\n⚠️ No start/goal points selected yet"

        UIBuilder.create_diagnostic_window(self.root, report)

    def _on_run_pathfinding(self):
        """Handle run pathfinding button."""
        if not self.map_ctrl.start_node or not self.map_ctrl.goal_node:
            messagebox.showwarning(
                "Warning", "⚠️ Please set both start and goal points!"
            )
            return

        # Check connectivity first
        is_connected, diagnostic = self.map_ctrl.check_path_exists()

        if not is_connected:
            msg = "❌ No path exists between selected points!\n\n"
            msg += "Reasons:\n"

            if not diagnostic["start_exists"]:
                msg += "• Start node not in graph\n"
            if not diagnostic["goal_exists"]:
                msg += "• Goal node not in graph\n"
            if diagnostic["start_exists"] and diagnostic["goal_exists"]:
                if not diagnostic["same_component"]:
                    msg += f"• Different network components\n"
                elif not diagnostic["path_exists"]:
                    msg += "• No directed path (one-way streets)\n"

            msg += "\n💡 Try 'Smart Random' button!"

            result = messagebox.askyesno(
                "Path Not Found", msg + "\n\nShow diagnostics?"
            )
            if result:
                self._on_diagnose()
            return

        # Get animation settings
        animate = self.widgets["animate_var"].get()
        speed_delays = {
            "Slow": 0.1,
            "Medium": 0.05,
            "Fast": 0.000001,
            "Instant": 0.0
        }
        delay = speed_delays.get(self.widgets["speed_var"].get(), 0.0)

        # Run algorithm(s)
        algo = self.widgets["algorithm_var"].get()
        self.map_ctrl.clear_paths()
        self.root.update()

        if algo == COMPARE_MODE:
            self._run_comparison(animate, delay)
        else:
            self._run_single(algo, animate, delay)

    def _run_single(self, algo_name, animate=False, delay=0.0):
        """Run single algorithm."""
        self._set_status(f"🔄 Running {algo_name}...")
        self.root.update()

        result = self.algo_exec.run_single_algorithm(
            algo_name,
            animate=animate,
            delay=delay
        )
        formatted = AlgorithmExecutor.format_results([result])
        self._set_status(formatted)

    def _run_comparison(self, animate=False, delay=0.0):
        """Run all algorithms for comparison."""
        self._set_status("🔄 Running comparison...")
        self.root.update()

        results = self.algo_exec.run_comparison(animate=animate, delay=delay)
        formatted = AlgorithmExecutor.format_results(results)
        self._set_status(formatted)

    def _on_clear_paths(self):
        """Handle clear paths button."""
        # Stop any running animation
        if self.algo_exec.is_running:
            self.algo_exec.stop_execution()
            # Give time for animation to stop
            self.root.after(100, lambda: self._do_clear_paths())
        else:
            self._do_clear_paths()

    def _do_clear_paths(self):
        """Actually clear the paths."""
        self.map_ctrl.clear_paths()
        self.algo_exec._clear_visited_markers()
        self._set_status("🧹 Paths cleared")

    def _on_clear_all(self):
        """Handle clear all button."""
        # Stop any running animation
        if self.algo_exec.is_running:
            self.algo_exec.stop_execution()
            # Give time for animation to stop
            self.root.after(100, lambda: self._do_clear_all())
        else:
            self._do_clear_all()

    def _do_clear_all(self):
        """Actually clear everything."""
        self.map_ctrl.clear_all()
        self.algo_exec._clear_visited_markers()
        self.widgets["mode_label"].config(
            text="Mode: Setting START 🟢", foreground="green"
        )
        self._set_status("🗑️ Map cleared | Click to set new points")

    # Helper Methods

    def _set_status(self, message):
        """Update status text."""
        UIBuilder.update_status(self.widgets["stats_text"], message)
