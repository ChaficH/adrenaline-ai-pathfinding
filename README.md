# Adrenaline: AI Pathfinding Visualizer

An interactive pathfinding engine and algorithm comparison tool built with Python and Pygame[cite: 1, 2]. The visualizer runs **A* Search**, **Breadth-First Search (BFS)**, and **Depth-First Search (DFS)** across a 40×40 weighted grid[cite: 1, 2], featuring cost-weighted terrain and live performance analytics[cite: 1, 2].

---

## Features

- **Pathfinding Algorithms**:
  - **A* Search**: Utilizes Manhattan distance heuristic and dynamic cost evaluation to compute optimal paths[cite: 2].
  - **Breadth-First Search (BFS)**: Unweighted shortest-path exploration[cite: 1, 2].
  - **Depth-First Search (DFS)**: Deep traversal exploration demonstrating unoptimized pathing[cite: 1, 2].
- **Cost-Weighted Terrain**:
  - **Standard Grid**: Cost = 1[cite: 2]
  - **Mud Tiles**: Cost = 10 (triggers weighted re-routing in A*)[cite: 1, 2]
  - **Walls**: Impassable obstacles[cite: 1, 2]
- **Procedural Maze Generation**: Implements a "Bulldozer" carving algorithm ensuring at least one solvable path while generating natural mud and wall distributions[cite: 1, 2].
- **Live Analytics Dashboard**: Real-time tracking of:
  - Total nodes explored[cite: 1, 2]
  - Path length (steps)[cite: 2]
  - Mud tiles crossed[cite: 2]
  - Total traversal cost[cite: 1, 2]

---

## Tech Stack

- **Language**: Python 3.x[cite: 1, 2]
- **Library**: Pygame[cite: 1, 2]
- **Core Concepts**: Graph Algorithms, Priority Queues, Manhattan Distance Heuristics, Object-Oriented UI[cite: 1, 2]

---

## Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone [https://github.com/ChaficH/adrenaline-ai-pathfinding.git](https://github.com/ChaficH/adrenaline-ai-pathfinding.git)
   cd adrenaline-ai-pathfinding
   ```

2. **Create a virtual environment (optional but recommended)**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python main.py
   ```

---

## Controls & Usage

| Action | Control |
| :--- | :--- |
| **Set Start Node** | Left Click (first click)[cite: 2] |
| **Set Target Node** | Left Click (second click)[cite: 2] |
| **Draw Obstacles / Paint** | Left Click + Drag[cite: 2] |
| **Erase Node** | Right Click or Eraser Brush[cite: 2] |
| **Cycle Brush Mode** | Click `Cycle Brush` (Wall / Mud / Erase)[cite: 2] |
| **Generate Maze** | Click `Generate Random Maze`[cite: 2] |
| **Execute Search** | Click `Run A*`, `Run BFS`, or `Run DFS`[cite: 2] |
| **Reset Map / Paths** | Click `Clear Path Lines` or `Clear Entire Board`[cite: 2] |

---

## License

Distributed under the MIT License. See `LICENSE` for more information.
