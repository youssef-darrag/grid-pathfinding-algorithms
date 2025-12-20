# 🗺️ GeoPath Visualizer

A comprehensive pathfinding visualization tool with **two modes**:
1. **Real-World Map Mode** - Visualize algorithms on actual road networks using OSMnx
2. **Grid Mode** - Classic grid-based pathfinding with Pygame

---

## 🎯 Features

### Real-World Map Visualizer
- 🗺️ Uses actual road networks from OpenStreetMap
- 🖱️ Click-to-select start and goal points
- 🎬 Step-by-step animation of algorithm exploration
- 📊 Performance metrics and comparison
- 🔍 Graph diagnostics and connectivity analysis
- 🎯 Smart randomization for connected points

### Grid Visualizer
- 🎮 Interactive Pygame visualization
- 🎲 Random grid generation
- 🔵 Real-time node exploration
- 📈 Performance metrics
- 🎨 Clean visual feedback

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/youssef-darrag/real-world-path-visualizer.git
cd real-world-path-visualizer

# Install dependencies
pip install -r requirements.txt
```

### Run Map Visualizer

```bash
python3 src/main_map.py
```

### Run Grid Visualizer

```bash
python3 src/main_grid.py
```

---

## 📚 Algorithms Implemented

Both visualizers support:
- **A*** (A-Star) - Optimal, uses heuristic
- **BFS** (Breadth-First Search) - Optimal, no heuristic
- **DFS** (Depth-First Search) - Non-optimal
- **UCS** (Uniform Cost Search) - Optimal
- **DLS** (Depth-Limited Search) - Depth-bounded
- **IDS** (Iterative Deepening Search) - Optimal

---

## 🎮 Usage

### Map Visualizer

1. **Load a location** - Default: "Cairo, Egypt"
2. **Set start/goal**:
   - Click map to select points
   - Use "Random" for random selection
   - Use "Smart Random" for guaranteed connected points
3. **Enable animation** (optional) - See real-time exploration
4. **Select algorithm** - Choose from dropdown
5. **Run** - Watch the algorithm find the path!

### Grid Visualizer

1. **Launch** - Grid generates automatically
2. **Click algorithm button** - A*, BFS, DFS, etc.
3. **Watch visualization** - Blue nodes = explored, Yellow = path
4. **New Grid** - Generate different maze
5. **Reset** - Clear current visualization

---

## 📊 Performance Metrics

Both visualizers show:
- **Execution time** (milliseconds)
- **Nodes explored** (search space)
- **Path length** (solution quality)
- **Memory usage** (space complexity)
- **Optimality** (is path optimal?)

---

## 🏗️ Project Structure

```
grid-pathfinding-algorithms/
├── src/
│   ├── main_map.py              # Map visualizer entry
│   ├── main_grid.py             # Grid visualizer entry
│   ├── algorithms/              # Map-based algorithms
│   ├── gui/                     # Map visualizer UI
│   ├── grid_visualizer/         # Grid visualizer
│   └── core/                    # Shared utilities
├── requirements.txt
└── README.md
```

---

## 🛩 INSIGHTS

### Real-World Map Mode
- Interactive map with actual roads
- Click-to-select points
- Animated exploration
- Multiple path comparison

### Grid Mode
- Classic grid visualization
- Obstacle generation
- Real-time algorithm animation
- Performance comparison

---

## 🔧 Configuration

### Map Visualizer Settings
- **Animation Speed**: Slow, Medium, Fast, Instant
- **Debug Mode**: Show click snapping
- **Grid Size**: Configurable in code

### Grid Visualizer Settings
- **Cell Size**: Default 35px
- **Grid Dimensions**: 15×20
- **Obstacle Density**: 20%

---

## 📖 Algorithm Details

### A* (A-Star)
- **Optimal**: Yes
- **Complete**: Yes
- **Time**: O(b^d)
- **Space**: O(b^d)
- Uses Manhattan distance (grid) or Haversine distance (map)

### BFS
- **Optimal**: Yes (unweighted)
- **Complete**: Yes
- **Time**: O(b^d)
- **Space**: O(b^d)
- Explores level by level

### DFS
- **Optimal**: No
- **Complete**: Yes (finite)
- **Time**: O(b^m)
- **Space**: O(bm)
- Goes deep first

### DLS
- **Optimal**: No
- **Complete**: NO
- **Time**: O(b^l)
- **Space**: O(bl)
- DFS with depth limit

### IDS
- **Optimal**: YES (unweighted)
- **Complete**: YES
- **Time**: O(b^d)
- **Space**: O(bd)
- Repeated DLS with increasing limits

### UCS
- **Optimal**: Yes
- **Complete**: Yes
- **Time**: O(b^d)
- **Space**: O(b^d)
- Considers edge costs

---

## 🐛 Troubleshooting

### Map won't load
- Check internet connection (first load downloads map)
- Try different location
- Check firewall settings

### Grid visualizer won't start
- Ensure Pygame is installed: `pip install pygame`
- Check Python version (3.8+)

### Animation freezing
- Use "Fast" or "Instant" speed
- Disable animation for large graphs
- Reduce grid size

---

## 👥 Authors

Youssef  - [GitHub](https://github.com/youssef-darrag) <br />
Salma    - [GitHub](https://github.com/salmasamh)      <br />
Hoda     - [GitHub](https://github.com/hudah-hamza)    <br />
Yomna    - [GitHub](https://github.com/yomnazedan14-ux)<br />
Mahmoud  - [GitHub](https://github.com/MahmoudOmiesh)  <br />
Mohammed - [GitHub](https://github.com/moohammedali)   <br />

---

## 🙏 Acknowledgments

- OSMnx for map data
- tkintermapview for map widget
- Pygame for grid visualization
- NetworkX for graph operations
