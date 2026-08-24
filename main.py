import pygame
from config import GRID_WIDTH, TOTAL_WIDTH, HEIGHT, ROWS
from ui import Button, make_grid, draw_window, get_clicked_pos
from algorithms import algorithm_astar, algorithm_bfs, algorithm_dfs
from maze import generate_random_maze

# --- INITIALIZATION & WINDOW SETUP ---
WIN = pygame.display.set_mode((TOTAL_WIDTH, HEIGHT))
pygame.display.set_caption("Adrenaline: AI Pathfinding Visualizer (Capstone)")


def main(win):
    grid = make_grid(ROWS, GRID_WIDTH)

    start = None
    end = None
    run = True
    brush_type = "WALL"

    metrics = {"algo": "Waiting...", "explored": 0, "steps": 0, "mud_crossed": 0, "cost": 0}

    btn_x = GRID_WIDTH + 30
    buttons = [
        Button(btn_x, 160, 280, 40, "Cycle Brush (Wall/Mud/Erase)", "TOGGLE"),
        Button(btn_x, 210, 280, 40, "Generate Random Maze", "GEN_MAZE", (80, 50, 90)),
        Button(btn_x, 265, 280, 40, "Run A* Algorithm", "RUN_ASTAR", (40, 80, 50)),
        Button(btn_x, 315, 280, 40, "Run BFS Algorithm", "RUN_BFS", (40, 50, 80)),
        Button(btn_x, 365, 280, 40, "Run DFS Algorithm", "RUN_DFS", (80, 40, 50)),
        Button(btn_x, 420, 280, 35, "Clear Path Lines", "CLEAR_PATH"),
        Button(btn_x, 465, 280, 35, "Clear Entire Board", "CLEAR_BOARD", (100, 30, 30))
    ]

    while run:
        if not start:
            status = "1. Left Click to place START"
        elif not end:
            status = "2. Left Click to place TARGET"
        else:
            status = "3. Draw Map & Choose Algorithm"

        draw_func = lambda: draw_window(win, grid, ROWS, GRID_WIDTH, buttons, "Searching...", brush_type, metrics)
        draw_window(win, grid, ROWS, GRID_WIDTH, buttons, status, brush_type, metrics)

        mouse_pos = pygame.mouse.get_pos()
        for btn in buttons:
            btn.check_hover(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if mouse_pos[0] >= GRID_WIDTH:
                    for btn in buttons:
                        if btn.is_clicked(mouse_pos):
                            if btn.action_name == "TOGGLE":
                                if brush_type == "WALL":
                                    brush_type = "MUD"
                                elif brush_type == "MUD":
                                    brush_type = "ERASE"
                                else:
                                    brush_type = "WALL"

                            elif btn.action_name == "GEN_MAZE":
                                start, end = generate_random_maze(grid, ROWS, start, end)
                                metrics = {"algo": "Maze Generated", "explored": 0, "steps": 0, "mud_crossed": 0, "cost": 0}

                            elif btn.action_name == "RUN_ASTAR" and start and end:
                                metrics = {"algo": "A* Search", "explored": "...", "steps": "...", "mud_crossed": "...", "cost": "..."}
                                for row in grid:
                                    for node in row:
                                        node.update_neighbors(grid)
                                result = algorithm_astar(draw_func, grid, start, end)
                                if result:
                                    metrics = result
                                else:
                                    metrics["cost"] = "FAILED"

                            elif btn.action_name == "RUN_BFS" and start and end:
                                metrics = {"algo": "BFS", "explored": "...", "steps": "...", "mud_crossed": "...", "cost": "..."}
                                for row in grid:
                                    for node in row:
                                        node.update_neighbors(grid)
                                result = algorithm_bfs(draw_func, grid, start, end)
                                if result:
                                    metrics = result
                                else:
                                    metrics["cost"] = "FAILED"

                            elif btn.action_name == "RUN_DFS" and start and end:
                                metrics = {"algo": "DFS", "explored": "...", "steps": "...", "mud_crossed": "...", "cost": "..."}
                                for row in grid:
                                    for node in row:
                                        node.update_neighbors(grid)
                                result = algorithm_dfs(draw_func, grid, start, end)
                                if result:
                                    metrics = result
                                else:
                                    metrics["cost"] = "FAILED"

                            elif btn.action_name == "CLEAR_PATH":
                                for row in grid:
                                    for node in row:
                                        if node.weight == 10:
                                            node.color = MUD
                                        elif not node.is_wall() and node != start and node != end:
                                            node.reset()
                                metrics = {"algo": "Cleared", "explored": 0, "steps": 0, "mud_crossed": 0, "cost": 0}

                            elif btn.action_name == "CLEAR_BOARD":
                                start = None
                                end = None
                                grid = make_grid(ROWS, GRID_WIDTH)
                                metrics = {"algo": "Waiting...", "explored": 0, "steps": 0, "mud_crossed": 0, "cost": 0}

            if pygame.mouse.get_pressed()[0]:
                if mouse_pos[0] < GRID_WIDTH:
                    row, col = get_clicked_pos(mouse_pos, ROWS, GRID_WIDTH)
                    node = grid[row][col]

                    if not start and node != end:
                        start = node
                        start.make_start()
                    elif not end and node != start:
                        end = node
                        end.make_end()
                    elif node != start and node != end:
                        if brush_type == "WALL":
                            node.make_wall()
                        elif brush_type == "MUD":
                            node.make_mud()
                        elif brush_type == "ERASE":
                            node.reset()

            elif pygame.mouse.get_pressed()[2]:
                if mouse_pos[0] < GRID_WIDTH:
                    row, col = get_clicked_pos(mouse_pos, ROWS, GRID_WIDTH)
                    node = grid[row][col]
                    node.reset()
                    if node == start:
                        start = None
                    if node == end:
                        end = None

    pygame.quit()


if __name__ == "__main__":
    main(WIN)
