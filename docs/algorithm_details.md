# Algorithms Overview

## 1. BFS (Breadth-First Search)
- Search Strategy: Level-by-level exploration
- Data Structure: Queue (FIFO)
- Completeness: Guaranteed to find a solution if one exists
- Optimality: Finds the shortest path (minimum number of steps) for uniform-cost problems
- Time Complexity: O(b^d), where b is branching factor, d is solution depth
- Space Complexity: O(b^d)
- Implementation Notes: Explores all nodes at the current depth before moving deeper

---

## 2. DFS (Depth-First Search)
- Search Strategy: Branch-by-branch exploration
- Data Structure: Stack (LIFO)
- Completeness: Not guaranteed (may get stuck in infinite depth)
- Optimality: Does not guarantee shortest path
- Time Complexity: O(b^m), where m is maximum depth
- Space Complexity: O(b×m)
- Implementation Notes: Explores as far as possible along each branch before backtracking

---

## 3. DLS (Depth-Limited Search)
- Search Strategy: Depth-first search with a maximum depth limit
- Data Structure: Stack with depth tracking
- Completeness: Only if solution exists within depth limit
- Optimality: Does not guarantee shortest path
- Time Complexity: O(b^l), where l is depth limit
- Space Complexity: O(b×l)
- Implementation Notes: Prevents infinite loops in DFS

---

## 4. IDS (Iterative Deepening Search)
- Search Strategy: Repeated depth-limited DFS with increasing depth limits
- Data Structure: Stack (for each DFS iteration)
- Completeness: Yes (like BFS)
- Optimality: Yes (for uniform-cost problems)
- Time Complexity: O(b^d)
- Space Complexity: O(b×d)
- Implementation Notes: Combines benefits of BFS (optimality) and DFS (memory efficiency)

---

## 5. UCS (Uniform-Cost Search)
- Search Strategy: Cost-based expansion
- Data Structure: Priority queue (ordered by path cost)
- Completeness: Yes (if solution exists and costs are non-negative)
- Optimality: Yes (finds least-cost path)
- Time Complexity: O(b^(1+⌊C/ε⌋)), where C is optimal cost, ε is minimum edge cost
- Space Complexity: O(b^(1+⌊C*/ε⌋))
- Implementation Notes: Generalization of BFS for non-uniform costs

---

## 6. A* Search
- Search Strategy: Best-first search using heuristic evaluation
- Data Structure: Priority queue (ordered by f(n) = g(n) + h(n))
- Heuristic Function: Manhattan distance: h(n) = |x_goal - x_n| + |y_goal - y_n|
- Admissibility: Manhattan distance is admissible (never overestimates)
- Completeness: Yes (with finite branching factor)
- Optimality: Yes (with admissible heuristic)
- Implementation Notes: More efficient than UCS when good heuristic is available