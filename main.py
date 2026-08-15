import pygame
import math
import random
from queue import PriorityQueue, Queue

# --- 1. INITIALIZATION & CONFIGURATION ---
pygame.init()

GRID_WIDTH = 800
UI_WIDTH = 340
TOTAL_WIDTH = GRID_WIDTH + UI_WIDTH
HEIGHT = 800

WIN = pygame.display.set_mode((TOTAL_WIDTH, HEIGHT))
pygame.display.set_caption("Adrenaline: AI Pathfinding Visualizer (Capstone)")

# Fonts
TITLE_FONT = pygame.font.SysFont("Segoe UI", 28, bold=True)
UI_FONT = pygame.font.SysFont("Segoe UI", 18, bold=True)
INFO_FONT = pygame.font.SysFont("Segoe UI", 16)
METRIC_FONT = pygame.font.SysFont("Courier New", 17, bold=True)

# Colors - Aesthetic Theme
OBSIDIAN = (18, 18, 18)       
UI_BG = (25, 25, 30)          
WALL = (44, 62, 80)           
START_NODE = (0, 255, 170)    
END_NODE = (255, 0, 85)       
SEARCH_HEAD = (0, 255, 255)   
FRONTIER = (138, 43, 226)     
VISITED = (20, 80, 150)       
PATH = (255, 215, 0)          
MUD = (121, 85, 72)           
ERASER_COLOR = (255, 100, 100) 
MUD_TEXT = (255, 152, 0)      
GRID_LINES = (35, 35, 35)
TEXT_COLOR = (240, 240, 240)

# Button Colors
BTN_DEFAULT = (60, 60, 70)
BTN_HOVER = (90, 90, 105)

# --- 2. UI BUTTON CLASS ---
class Button:
    def __init__(self, x, y, width, height, text, action_name, color=BTN_DEFAULT):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action_name = action_name
        self.is_hovered = False
        self.base_color = color

    def draw(self, win):
        color = BTN_HOVER if self.is_hovered else self.base_color
        pygame.draw.rect(win, color, self.rect, border_radius=8)
        pygame.draw.rect(win, (100, 100, 100), self.rect, 1, border_radius=8)
        
        text_surf = UI_FONT.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        win.blit(text_surf, text_rect)

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

# --- 3. NODE (CELL) CLASS ---
class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = OBSIDIAN
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
        self.weight = 1 

    def get_pos(self): return self.row, self.col
    def is_wall(self): return self.color == WALL
    def is_mud(self): return self.weight == 10 

    def reset(self): 
        self.color = OBSIDIAN
        self.weight = 1
    def make_head(self): self.color = SEARCH_HEAD 
    def make_closed(self): self.color = VISITED
    def make_open(self): self.color = FRONTIER
    def make_wall(self): 
        self.color = WALL
        self.weight = float('inf') 
    def make_mud(self):
        self.color = MUD
        self.weight = 10 
    def make_start(self): self.color = START_NODE
    def make_end(self): self.color = END_NODE
    def make_path(self): self.color = PATH

    def draw(self, win):
        if self.weight == 10 and self.color not in [OBSIDIAN, MUD]:
            pygame.draw.rect(win, MUD, (self.x, self.y, self.width, self.width))
            margin = 5
            inner_rect = (self.x + margin, self.y + margin, self.width - (2 * margin), self.width - (2 * margin))
            pygame.draw.rect(win, self.color, inner_rect)
        else:
            pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_wall(): # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].is_wall(): # UP
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_wall(): # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].is_wall(): # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

# --- 4. ALGORITHMS & METRICS MATH ---
def h_score(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw_func):
    total_cost = 0 
    steps = 0
    mud_crossed = 0
    
    while current in came_from:
        total_cost += current.weight
        steps += 1
        if current.is_mud():
            mud_crossed += 1
            
        current = came_from[current]
        
        if current.color != START_NODE:
            current.make_path()
        draw_func()
        
    return {"cost": total_cost, "steps": steps, "mud_crossed": mud_crossed}

def algorithm_astar(draw_func, grid, start, end):
    count = 0
    nodes_explored = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h_score(start.get_pos(), end.get_pos())
    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)
        nodes_explored += 1

        if current == end:
            path_data = reconstruct_path(came_from, end, draw_func)
            end.make_end()
            return {"algo": "A* Search", "explored": nodes_explored, **path_data}

        if current != start: current.make_head()

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + neighbor.weight
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h_score(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    if neighbor != end: neighbor.make_open()

        draw_func()
        if current != start: current.make_closed()
        
    return None

def algorithm_bfs(draw_func, grid, start, end):
    nodes_explored = 0
    queue = Queue()
    queue.put(start)
    came_from = {}
    visited = {start}

    while not queue.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit()

        current = queue.get()
        nodes_explored += 1

        if current == end:
            path_data = reconstruct_path(came_from, end, draw_func)
            end.make_end()
            return {"algo": "BFS", "explored": nodes_explored, **path_data}

        if current != start: current.make_head()

        for neighbor in current.neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                queue.put(neighbor)
                if neighbor != end: neighbor.make_open()

        draw_func()
        if current != start: current.make_closed()
        
    return None

def algorithm_dfs(draw_func, grid, start, end):
    nodes_explored = 0
    stack = [start]
    came_from = {}
    visited = {start}

    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit()

        current = stack.pop()
        nodes_explored += 1

        if current == end:
            path_data = reconstruct_path(came_from, end, draw_func)
            end.make_end()
            return {"algo": "DFS", "explored": nodes_explored, **path_data}

        if current != start: current.make_head()

        for neighbor in current.neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                stack.append(neighbor)
                if neighbor != end: neighbor.make_open()

        draw_func()
        if current != start: current.make_closed()
        
    return None

# --- 5. GRID & UI DRAWING ---
def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid

def draw_grid_lines(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GRID_LINES, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GRID_LINES, (j * gap, 0), (j * gap, width))

def draw_legend_item(win, x, y, color, text):
    pygame.draw.rect(win, color, (x, y, 20, 20))
    pygame.draw.rect(win, (255, 255, 255), (x, y, 20, 20), 1)
    label = INFO_FONT.render(text, True, TEXT_COLOR)
    win.blit(label, (x + 30, y))

def draw_ui_panel(win, buttons, current_status, brush_type, metrics):
    ui_rect = pygame.Rect(GRID_WIDTH, 0, UI_WIDTH, HEIGHT)
    pygame.draw.rect(win, UI_BG, ui_rect)
    pygame.draw.line(win, (100, 100, 100), (GRID_WIDTH, 0), (GRID_WIDTH, HEIGHT), 3)

    title = TITLE_FONT.render("AI Pathfinding Engine", True, SEARCH_HEAD)
    win.blit(title, (GRID_WIDTH + 20, 20))
    
    status_label = UI_FONT.render("Current Step:", True, (150, 150, 150))
    win.blit(status_label, (GRID_WIDTH + 20, 60))
    status_text = INFO_FONT.render(current_status, True, PATH)
    win.blit(status_text, (GRID_WIDTH + 20, 85))

    if brush_type == "WALL": brush_color = START_NODE
    elif brush_type == "MUD": brush_color = MUD
    else: brush_color = ERASER_COLOR
        
    brush_label = UI_FONT.render(f"Active Brush: {brush_type}", True, brush_color)
    win.blit(brush_label, (GRID_WIDTH + 20, 120))

    for btn in buttons: btn.draw(win)

    # --- THE ADVANCED ANALYTICS DASHBOARD ---
    dash_y = 525
    dash_rect = pygame.Rect(GRID_WIDTH + 20, dash_y, UI_WIDTH - 40, 150)
    pygame.draw.rect(win, (35, 35, 40), dash_rect, border_radius=8)
    pygame.draw.rect(win, SEARCH_HEAD, dash_rect, 2, border_radius=8)
    
    dash_title = UI_FONT.render("Live Execution Analytics", True, SEARCH_HEAD)
    win.blit(dash_title, (GRID_WIDTH + 30, dash_y + 10))

    algo_text = INFO_FONT.render(f"Algorithm: {metrics['algo']}", True, TEXT_COLOR)
    win.blit(algo_text, (GRID_WIDTH + 30, dash_y + 35))

    exp_text = METRIC_FONT.render(f"Nodes Explored : {metrics['explored']}", True, (200, 200, 200))
    stp_text = METRIC_FONT.render(f"Path Length    : {metrics['steps']} steps", True, (200, 200, 200))
    
    mud_color = MUD_TEXT if metrics['mud_crossed'] not in ["...", 0] else (200, 200, 200)
    mud_text = METRIC_FONT.render(f"Mud Crossed    : {metrics['mud_crossed']} tiles", True, mud_color)
    cst_text = METRIC_FONT.render(f"TOTAL COST     : {metrics['cost']}", True, PATH) 
    
    win.blit(exp_text, (GRID_WIDTH + 30, dash_y + 55))
    win.blit(stp_text, (GRID_WIDTH + 30, dash_y + 75))
    win.blit(mud_text, (GRID_WIDTH + 30, dash_y + 95))
    win.blit(cst_text, (GRID_WIDTH + 30, dash_y + 120))

    # --- MAP LEGEND ---
    legend_y = HEIGHT - 110
    draw_legend_item(win, GRID_WIDTH + 20, legend_y, START_NODE, "Start")
    draw_legend_item(win, GRID_WIDTH + 110, legend_y, END_NODE, "Target")
    draw_legend_item(win, GRID_WIDTH + 200, legend_y, SEARCH_HEAD, "Head")
    
    draw_legend_item(win, GRID_WIDTH + 20, legend_y + 35, WALL, "Wall")
    draw_legend_item(win, GRID_WIDTH + 110, legend_y + 35, MUD, "Mud (Cost 10)")
    draw_legend_item(win, GRID_WIDTH + 20, legend_y + 70, FRONTIER, "Frontier")
    draw_legend_item(win, GRID_WIDTH + 110, legend_y + 70, PATH, "Best Path")

def draw_window(win, grid, rows, grid_width, buttons, current_status, brush_type, metrics):
    win.fill(OBSIDIAN)
    for row in grid:
        for node in row: node.draw(win)
    draw_grid_lines(win, rows, grid_width)
    draw_ui_panel(win, buttons, current_status, brush_type, metrics)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    x, y = pos
    row = x // gap
    col = y // gap
    return row, col

# --- 6. MAIN APPLICATION LOOP ---
def main(win):
    ROWS = 40 
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
        if not start: status = "1. Left Click to place START"
        elif not end: status = "2. Left Click to place TARGET"
        else: status = "3. Draw Map & Choose Algorithm"

        draw_func = lambda: draw_window(win, grid, ROWS, GRID_WIDTH, buttons, "Searching...", brush_type, metrics)
        draw_window(win, grid, ROWS, GRID_WIDTH, buttons, status, brush_type, metrics)
        
        mouse_pos = pygame.mouse.get_pos()
        for btn in buttons: btn.check_hover(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if mouse_pos[0] >= GRID_WIDTH:
                    for btn in buttons:
                        if btn.is_clicked(mouse_pos):
                            if btn.action_name == "TOGGLE":
                                if brush_type == "WALL": brush_type = "MUD"
                                elif brush_type == "MUD": brush_type = "ERASE"
                                else: brush_type = "WALL"

                            elif btn.action_name == "GEN_MAZE":
                                # 1. Clear grid entirely, BUT spare the start and end nodes
                                for row in grid:
                                    for node in row: 
                                        if node != start and node != end:
                                            node.reset()
                                
                                # 2. Set Start/End defaults if they don't exist
                                if not start: 
                                    start = grid[4][4]
                                if not end: 
                                    end = grid[ROWS-5][ROWS-5]
                                
                                # 2.5 Force them to display their correct colors 
                                start.make_start()
                                end.make_end()
                                
                                # 3. Randomly Scatter walls and mud
                                for row in grid:
                                    for node in row:
                                        if node != start and node != end:
                                            chance = random.random()
                                            if chance < 0.32: node.make_wall()
                                            elif chance < 0.47: node.make_mud()
                                            
                                # 4. "The Bulldozer": Carve guaranteed path to target
                                curr_r, curr_c = start.get_pos()
                                end_r, end_c = end.get_pos()
                                
                                while (curr_r, curr_c) != (end_r, end_c):
                                    moves = []
                                    if curr_r < end_r: moves.append((1, 0))
                                    if curr_r > end_r: moves.append((-1, 0))
                                    if curr_c < end_c: moves.append((0, 1))
                                    if curr_c > end_c: moves.append((0, -1))
                                    
                                    dr, dc = random.choice(moves)
                                    curr_r += dr
                                    curr_c += dc
                                    
                                    b_node = grid[curr_r][curr_c]
                                    if b_node != end and b_node != start:
                                        # 85% chance to clear space, 15% to leave mud on path
                                        if random.random() < 0.85: b_node.reset()
                                        else: b_node.make_mud()
                                        
                                metrics = {"algo": "Maze Generated", "explored": 0, "steps": 0, "mud_crossed": 0, "cost": 0}
                                
                            elif btn.action_name == "RUN_ASTAR" and start and end:
                                metrics = {"algo": "A* Search", "explored": "...", "steps": "...", "mud_crossed": "...", "cost": "..."}
                                for row in grid:
                                    for node in row: node.update_neighbors(grid)
                                result = algorithm_astar(draw_func, grid, start, end)
                                if result: metrics = result
                                else: metrics["cost"] = "FAILED"
                                
                            elif btn.action_name == "RUN_BFS" and start and end:
                                metrics = {"algo": "BFS", "explored": "...", "steps": "...", "mud_crossed": "...", "cost": "..."}
                                for row in grid:
                                    for node in row: node.update_neighbors(grid)
                                result = algorithm_bfs(draw_func, grid, start, end)
                                if result: metrics = result
                                else: metrics["cost"] = "FAILED"
                                
                            elif btn.action_name == "RUN_DFS" and start and end:
                                metrics = {"algo": "DFS", "explored": "...", "steps": "...", "mud_crossed": "...", "cost": "..."}
                                for row in grid:
                                    for node in row: node.update_neighbors(grid)
                                result = algorithm_dfs(draw_func, grid, start, end)
                                if result: metrics = result
                                else: metrics["cost"] = "FAILED"
                                
                            elif btn.action_name == "CLEAR_PATH":
                                for row in grid:
                                    for node in row:
                                        if node.weight == 10: node.color = MUD
                                        elif not node.is_wall() and node != start and node != end: node.reset()
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
                if node == start: start = None
                if node == end: end = None

    pygame.quit()

if __name__ == "__main__":
    main(WIN)