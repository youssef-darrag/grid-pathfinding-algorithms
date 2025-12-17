# 🗺️ Real-World Map Finding Visualizer

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Tkinter](https://img.shields.io/badge/Tkinter-GUI-orange.svg)](https://docs.python.org/3/library/tkinter.html)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Open Issues](https://img.shields.io/github/issues/username/map-finding-visualizer)](https://github.com/username/map-finding-visualizer/issues)

An interactive desktop application built with Python and Tkinter that visualizes various pathfinding algorithms on real-world maps using OpenStreetMap data. Compare how different search algorithms (BFS, DFS, DLS, IDS, UCS, A*) explore and find paths between geographic locations.

![Demo Screenshot](demo/screenshot.png) *Replace with your actual screenshot*

## ✨ Features

- **🌍 Real-World Maps**: Interactive maps using TkinterMapView with OpenStreetMap integration
- **🔍 Multiple Algorithms**: Visualize 6 different pathfinding algorithms:
  - Breadth-First Search (BFS)
  - Depth-First Search (DFS)
  - Depth-Limited Search (DLS)
  - Iterative Deepening Search (IDS)
  - Uniform Cost Search (UCS)
  - A* Search
- **🎨 Interactive GUI**: Clean, user-friendly interface with real-time visualization
- **📊 Live Statistics**: Watch algorithm metrics update in real-time:
  - Path distance
  - Nodes explored
  - Execution time
  - Algorithm status
- **📍 Location Search**: Search any address or coordinate worldwide
- **⚙️ Customizable Settings**: Adjust algorithm parameters and visualization speed

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Tkinter

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/youssef-darrag/grid-pathfinding-algorithms.git
cd map-finding-visualizer
```

2. **Create and activate virtual environment** (recommended)
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
python main.py
```

## 📋 Requirements

All dependencies are listed in `requirements.txt`:
```
tkintermapview==2.25.1
osmnx==1.6.0
networkx==3.1
```

## 🎮 Usage Guide

### 1. Launch the Application
- Run `python3 main.py` from the command line
- The main window will open with a world map

### 2. Set Start and End Locations
- **Method 1: Click on Map**
  - Click the first time to set start point
  - Click the second time to set end point
- **Method 2: Search Address**
  - Use the search bar to find locations
  - Click "Set as Start" or "Set as End" buttons
- **Method 2: Randomized search**
  - Click Random Search button to choose 2 random points within 0.5km radius
  - Click Smart Search button to choose 2 random points without breaking the rules of strongly connected components and DAGs

### 3. Select Algorithm
- Choose from the algorithm dropdown:
  - BFS (Breadth-First Search)
  - DFS (Depth-First Search)
  - DLS (Depth-Limited Search) - requires depth limit
  - IDS (Iterative Deepening Search)
  - UCS (Uniform Cost Search)
  - A* (A Star) - with selectable heuristic

### 5. Run Visualization
- Click **"Find Path"** to start algorithm
- Watch real-time exploration on map:
  - **Green**: Start point
  - **Red**: End point
  - **Blue**: Explored nodes
  - **Yellow**: Frontier nodes
  - **Purple**: Final path
- Click **Reload map** to reload a different part of the map
- Use **Clear path** to clear current paths
- Click **Clear All** to clear current visualization

### 6. View Results
- Check statistics panel for:
  - Algorithm status
  - Path distance
  - Nodes explored
  - Execution time
  - Color of path
- Compare multiple algorithms by running them sequentially

## 🏗️ Project Structure

```
grid-pathfinding-algorithms/
│
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── map_data.graphml           # Cached map data
│
├── src/                       # Source code
│   ├── algorithms/           # Algorithm implementations
│   │   ├── __init__.py      # Package initialization
│   │   ├── astar.py         # A* algorithm
│   │   ├── bfs.py           # Breadth-First Search
│   │   ├── dfs.py           # Depth-First Search
│   │   ├── dls.py           # Depth-Limited Search
│   │   ├── ids.py           # Iterative Deepening Search
│   │   └── ucs.py           # Uniform Cost Search
│   │
│   ├── core/                 # Core functionality
│   │   ├── __init__.py
│   │   ├── map.py           # Map loading and management
│   │   ├── map_diagnostics.py # Map analysis utilities
│   │   └── utils.py         # Helper functions
│   │
│   └── gui/                  # Graphical User Interface
│       └── window.py        # Main application window
│
├── cache/                    # Cache directory for map data
├── docs/                     # Documentation
└── venv/                     # Virtual environment (not in git)
```


## 📊 Performance Tips

1. **Map Size**: Smaller areas (< 2km radius) load faster
2. **Caching**: OSMrx caches downloaded maps locally
3. **Step Delay**: Increase for smoother visualization on complex maps
4. **Graph Simplification**: Reduce graph complexity for faster processing

## 🚧 Known Limitations

- **Large Maps**: Very large areas may slow down visualization
- **Internet Required**: Needs internet for map tile loading (first time)
- **Memory Usage**: Complex algorithms on large graphs use significant memory
- **OSM Data Quality**: Dependent on OpenStreetMap completeness in area


## 🙏 Acknowledgments

- [OpenStreetMap](ttps://github.com/youssef-darrag) contributors for free map data
- [Tom Schimansky](https://github.com/TomSchimansky) for TkinterMapView
- [Geoff Boeing](https://github.com/gboeing) for OSMnx
- [NetworkX](https://networkx.org/) team for graph library
