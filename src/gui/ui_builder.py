"""
UI Builder - Constructs UI components
"""

import tkinter as tk
from tkinter import ttk
import tkintermapview


class UIBuilder:
    """Builds and organizes UI components."""

    @staticmethod
    def create_map_widget(parent):
        """Create and configure map widget."""
        map_frame = tk.Frame(parent)
        map_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        map_widget = tkintermapview.TkinterMapView(map_frame, corner_radius=0)
        map_widget.set_tile_server(
            "https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga",
            max_zoom=22,
        )
        map_widget.pack(fill="both", expand=True)

        return map_widget

    @staticmethod
    def create_controls_panel(parent, callbacks):
        """
        Create controls panel with all buttons and inputs.

        Args:
            parent: Parent widget
            callbacks: dict with callback functions

        Returns:
            tuple: (controls_frame, widgets_dict)
        """
        controls = ttk.LabelFrame(parent, text="🎮 Controls", padding=15)
        controls.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
        controls.columnconfigure(1, weight=1)

        widgets = {}

        # Row 0: Location Input
        ttk.Label(controls, text="📍 Location:").grid(
            row=0, column=0, sticky="w", pady=5
        )

        loc_entry = ttk.Entry(controls, width=30)
        loc_entry.insert(0, "Cairo, Egypt")
        loc_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        widgets["location_entry"] = loc_entry

        reload_btn = ttk.Button(
            controls, text="🔄 Reload Map", command=callbacks.get("on_reload_map")
        )
        reload_btn.grid(row=0, column=2, padx=5, pady=5)
        widgets["reload_btn"] = reload_btn

        # Row 1: Algorithm Selection & Mode
        ttk.Label(controls, text="🧠 Algorithm:").grid(
            row=1, column=0, sticky="w", pady=5
        )

        algo_frame = ttk.Frame(controls)
        algo_frame.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        from algorithms import ALGORITHMS, COMPARE_MODE

        algo_var = tk.StringVar(value=list(ALGORITHMS.keys())[0])
        algo_box = ttk.Combobox(
            algo_frame,
            textvariable=algo_var,
            values=list(ALGORITHMS.keys()) + [COMPARE_MODE],
            state="readonly",
            width=20,
        )
        algo_box.pack(side="left", fill="x", expand=True)
        widgets["algorithm_var"] = algo_var
        widgets["algorithm_box"] = algo_box

        if callbacks.get("on_algo_change"):
            algo_box.bind("<<ComboboxSelected>>", callbacks["on_algo_change"])

        mode_label = ttk.Label(
            algo_frame, text="Mode: Setting START 🟢", foreground="green"
        )
        mode_label.pack(side="left", padx=(10, 0))
        widgets["mode_label"] = mode_label

        # Random buttons
        random_btn = ttk.Button(
            controls, text="🎲 Random",
            command=callbacks.get("on_randomize"),
            state="disabled"
        )
        random_btn.grid(row=1, column=2, padx=5, pady=5)
        widgets["random_btn"] = random_btn

        smart_random_btn = ttk.Button(
            controls, text="🎯 Smart",
            command=callbacks.get("on_smart_randomize"),
            state="disabled"
        )
        smart_random_btn.grid(row=1, column=3, padx=5, pady=5)
        widgets["smart_random_btn"] = smart_random_btn

        # Row 2: Animation Controls (NEW)
        anim_frame = ttk.LabelFrame(controls, text="🎬 Animation", padding=5)
        anim_frame.grid(row=2, column=0, columnspan=4, sticky="ew", padx=5, pady=5)

        animate_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            anim_frame,
            text="Enable Animation",
            variable=animate_var,
        ).pack(side="left", padx=5)
        widgets["animate_var"] = animate_var

        ttk.Label(anim_frame, text="Speed:").pack(side="left", padx=(10, 5))

        speed_var = tk.StringVar(value="Fast")
        speed_combo = ttk.Combobox(
            anim_frame,
            textvariable=speed_var,
            values=["Slow", "Medium", "Fast", "Instant"],
            state="readonly",
            width=10,
        )
        speed_combo.pack(side="left", padx=5)
        widgets["speed_var"] = speed_var

        ttk.Label(
            anim_frame,
            text="💡 Shows algorithm exploration in real-time",
            foreground="gray"
        ).pack(side="left", padx=10)

        # Row 3: Debug & Diagnostics
        options_frame = ttk.Frame(controls)
        options_frame.grid(row=3, column=0, columnspan=4, sticky="ew", padx=5, pady=5)

        diagnose_btn = ttk.Button(
            options_frame, text="🔍 Diagnose",
            command=callbacks.get("on_diagnose"),
            state="disabled"
        )
        diagnose_btn.pack(side="left", padx=(0, 5))
        widgets["diagnose_btn"] = diagnose_btn

        debug_var = tk.BooleanVar(value=False)
        debug_check = ttk.Checkbutton(
            options_frame,
            text="🐛 Debug Mode (show click snapping)",
            variable=debug_var,
        )
        debug_check.pack(side="left", padx=5)
        widgets["debug_var"] = debug_var

        # Row 4: Action Buttons
        btn_frame = ttk.Frame(controls)
        btn_frame.grid(row=4, column=0, columnspan=4, pady=10, sticky="ew")
        btn_frame.columnconfigure(0, weight=1)

        run_btn = ttk.Button(
            btn_frame, text="▶ RUN PATHFINDING",
            command=callbacks.get("on_run"),
            state="disabled"
        )
        run_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))
        widgets["run_btn"] = run_btn

        ttk.Button(
            btn_frame, text="🗑️ Clear All",
            command=callbacks.get("on_clear_all")
        ).pack(side="left", padx=5)

        ttk.Button(
            btn_frame, text="🧹 Clear Paths",
            command=callbacks.get("on_clear_paths")
        ).pack(side="left", padx=5)

        # Row 5: Statistics
        stats_frame = ttk.LabelFrame(
            controls, text="📊 Statistics & Results", padding=10
        )
        stats_frame.grid(row=5, column=0, columnspan=4, sticky="ew", pady=(5, 0))

        stats_container = ttk.Frame(stats_frame)
        stats_container.pack(fill="both", expand=True)

        scrollbar = ttk.Scrollbar(stats_container)
        scrollbar.pack(side="right", fill="y")

        stats_text = tk.Text(
            stats_container,
            height=7,
            font=("Consolas", 9),
            state="disabled",
            wrap="none",
            yscrollcommand=scrollbar.set,
        )
        stats_text.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=stats_text.yview)
        widgets["stats_text"] = stats_text

        return controls, widgets

    @staticmethod
    def update_status(stats_text, message):
        """Update status/stats text widget."""
        stats_text.config(state="normal")
        stats_text.delete("1.0", tk.END)
        stats_text.insert(tk.END, message)
        stats_text.config(state="disabled")

    @staticmethod
    def create_diagnostic_window(parent, report_text):
        """Create diagnostic popup window."""
        diag_window = tk.Toplevel(parent)
        diag_window.title("🔍 Graph Diagnostics")
        diag_window.geometry("650x550")

        text_frame = ttk.Frame(diag_window, padding=10)
        text_frame.pack(fill="both", expand=True)

        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side="right", fill="y")

        text_widget = tk.Text(
            text_frame,
            font=("Consolas", 10),
            wrap="word",
            yscrollcommand=scrollbar.set,
        )
        text_widget.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=text_widget.yview)

        text_widget.insert("1.0", report_text)
        text_widget.config(state="disabled")

        ttk.Button(
            diag_window, text="Close", command=diag_window.destroy
        ).pack(pady=10)

        return diag_window
