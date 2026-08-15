# Adrenaline: AI Pathfinding Visualizer

An interactive AI pathfinding engine and algorithmic visualizer built in Python with Pygame. It simulates and benchmarks search algorithms (**A\***, **Breadth-First Search**, and **Depth-First Search**) in real-time across cost-weighted grid environments.

---

## Features

- **Search Algorithms**:
  - **A\* Search**: Informed heuristic search ($f(n) = g(n) + h(n)$ using Manhattan distance) optimizing path cost across weighted terrain.
  - **Breadth-First Search (BFS)**: Unweighted shortest-path exploration.
  - **Depth-First Search (DFS)**: Uninformed graph traversal exploration.
- **Dynamic Terrain**:
  - **Impassable Walls**: Infinite traversal cost obstacles.
  - **Mud Tiles**: Weighted terrain (traversal cost = 10) for evaluating weighted vs. unweighted algorithmic behavior.
- **Procedural Maze Generation**: Custom "Bulldozer" path-carving algorithm guaranteeing solvable maps with random obstacles and mud traps.
- **Live Analytics Dashboard**: Real-time telemetry reporting explored nodes, path length (steps), mud tiles crossed, and total path cost.

---

## Tech Stack

- **Language**: Python 3.x
- **Graphics / UI**: Pygame
- **Data Structures**: PriorityQueue (`heapq`), Queue, LIFO Stack

---

## Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone [https://github.com/ChaficH/adrenaline-ai-pathfinding-visualizer.git](https://github.com/ChaficH/adrenaline-ai-pathfinding-visualizer.git)
   cd adrenaline-ai-pathfinding-visualizer
