# Adrenaline: AI Pathfinding Visualizer

An interactive AI pathfinding engine and algorithmic visualizer built in Python with Pygame[cite: 1, 2]. It simulates and benchmarks search algorithms (**A\***, **Breadth-First Search**, and **Depth-First Search**) in real-time across cost-weighted grid environments[cite: 1, 2].

---

## Features

- **Search Algorithms**:
  - **A\* Search**: Informed heuristic search ($f(n) = g(n) + h(n)$ using Manhattan distance) optimizing path cost across weighted terrain.
  - **Breadth-First Search (BFS)**: Unweighted shortest-path exploration[cite: 1, 2].
  - **Depth-First Search (DFS)**: Uninformed graph traversal exploration[cite: 1, 2].
- **Dynamic Terrain**:
  - **Impassable Walls**: Infinite traversal cost obstacles[cite: 1, 2].
  - **Mud Tiles**: Weighted terrain (traversal cost = 10) for evaluating weighted vs. unweighted algorithmic behavior[cite: 1, 2].
- **Procedural Maze Generation**: Custom "Bulldozer" path-carving algorithm guaranteeing solvable maps with random obstacles and mud traps[cite: 1, 2].
- **Live Analytics Dashboard**: Real-time telemetry reporting explored nodes, path length (steps), mud tiles crossed, and total path cost[cite: 1, 2].

---

## Tech Stack

- **Language**: Python 3.x
- **Graphics / UI**: Pygame[cite: 1, 2]
- **Core Algorithms**: A* Search, Breadth-First Search (BFS), Depth-First Search (DFS)[cite: 1, 2]

---

## Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone [https://github.com/ChaficH/adrenaline-ai-pathfinding.git](https://github.com/ChaficH/adrenaline-ai-pathfinding.git)
   cd adrenaline-ai-pathfinding
