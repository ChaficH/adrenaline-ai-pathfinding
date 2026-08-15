# Adrenaline: AI Pathfinding Visualizer

An interactive AI pathfinding engine and algorithmic visualizer built in Python with Pygame. It simulates and benchmarks **A***, **Breadth-First Search (BFS)**, and **Depth-First Search (DFS)** in real time across cost-weighted grid environments.

## Features

### Search Algorithms

* **A* Search** — Informed heuristic search using `f(n) = g(n) + h(n)` with Manhattan distance, optimizing path cost across weighted terrain.
* **Breadth-First Search (BFS)** — Unweighted shortest-path exploration.
* **Depth-First Search (DFS)** — Uninformed graph traversal exploration.

### Dynamic Terrain

* **Impassable Walls** — Infinite traversal cost obstacles.
* **Mud Tiles** — Weighted terrain with a traversal cost of `10`, allowing comparison between weighted and unweighted search behavior.
* **Interactive Map Editing** — Draw walls, mud, or erase terrain directly on the grid.

### Procedural Maze Generation

* Custom **Bulldozer path-carving algorithm**.
* Randomly generates walls and mud tiles.
* Guarantees a traversable path between the start and target nodes.

### Live Analytics Dashboard

Real-time execution telemetry including:

* Nodes explored
* Path length
* Mud tiles crossed
* Total path cost
* Currently running algorithm

## Tech Stack

* **Language:** Python 3.x
* **Graphics / UI:** Pygame
* **Algorithms:** A*, BFS, DFS
* **Data Structures:** Priority Queue, Queue, Stack, Hash Sets

## Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/ChaficH/adrenaline-ai-pathfinding.git
cd adrenaline-ai-pathfinding
```

### 2. Install dependencies

```bash
pip install pygame
```

### 3. Run the application

```bash
python main.py
```

## How It Works

The visualizer operates on a **40 × 40 grid**, where each cell represents a node. The environment supports both impassable obstacles and weighted terrain.

* **Normal tile:** Cost `1`
* **Mud tile:** Cost `10`
* **Wall:** Impassable

A* evaluates both the accumulated path cost and the estimated distance to the target using the Manhattan-distance heuristic. BFS explores the grid without considering terrain cost, while DFS performs depth-first graph traversal.

Each algorithm records execution metrics such as nodes explored, path length, mud tiles crossed, and total path cost.

## Project Structure

```text
adrenaline-ai-pathfinding/
│
├── main.py
├── README.md
└── requirements.txt
```

## Controls

1. **Left Click** — Place the Start and Target nodes.
2. **Cycle Brush** — Switch between Wall, Mud, and Erase.
3. **Generate Random Maze** — Generate a random solvable environment.
4. **Run A*** — Execute A* Search.
5. **Run BFS** — Execute Breadth-First Search.
6. **Run DFS** — Execute Depth-First Search.
7. **Clear Path Lines** — Remove search results while preserving the map.
8. **Clear Entire Board** — Reset the entire grid.

## Project Goal

The goal of **Adrenaline** is to provide an interactive way to understand and compare pathfinding algorithms under different environmental conditions, particularly the effect of **weighted terrain on path selection and search efficiency**.

The visualization makes the differences between informed and uninformed search strategies observable through both the animated search process and quantitative execution metrics.
