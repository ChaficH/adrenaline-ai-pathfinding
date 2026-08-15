# Adrenaline: AI Pathfinding Visualizer

An interactive pathfinding engine and algorithm comparison tool built with Python and Pygame. The visualizer runs **A* Search**, **Breadth-First Search (BFS)**, and **Depth-First Search (DFS)** across a 40×40 weighted grid, featuring cost-weighted terrain and live performance analytics.

---

## Features

- **Pathfinding Algorithms**:
  - **A* Search**: Utilizes Manhattan distance heuristic and dynamic cost evaluation to compute optimal paths.
  - **Breadth-First Search (BFS)**: Unweighted shortest-path exploration.
  - **Depth-First Search (DFS)**: Deep traversal exploration demonstrating unoptimized pathing.
- **Cost-Weighted Terrain**:
  - **Standard Grid**: Cost = 1
  - **Mud Tiles**: Cost = 10 (triggers weighted re-routing in A*)
  - **Walls**: Impassable obstacles
- **Procedural Maze Generation**: Implements a "Bulldozer" carving algorithm ensuring at least one solvable path while generating natural mud and wall distributions.
- **Live Analytics Dashboard**: Real-time tracking of:
  - Total nodes explored
  - Path length (steps)
  - Mud tiles crossed
  - Total traversal cost

---

## Tech Stack

- **Language**: Python 3.x
- **Library**: Pygame
- **Core Concepts**: Graph Algorithms, Priority Queues, Manhattan Distance Heuristics, Object-Oriented UI

---

## Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone [https://github.com/ChaficH/adrenaline-ai-pathfinding.git](https://github.com/ChaficH/adrenaline-ai-pathfinding.git)
   cd adrenaline-ai-pathfinding
