import pygame
from node import Node
from config import (
    GRID_WIDTH,
    UI_WIDTH,
    HEIGHT,
    TITLE_FONT,
    UI_FONT,
    INFO_FONT,
    METRIC_FONT,
    OBSIDIAN,
    UI_BG,
    WALL,
    START_NODE,
    END_NODE,
    SEARCH_HEAD,
    FRONTIER,
    PATH,
    MUD,
    ERASER_COLOR,
    MUD_TEXT,
    GRID_LINES,
    TEXT_COLOR,
    BTN_DEFAULT,
    BTN_HOVER
)


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

    if brush_type == "WALL":
        brush_color = START_NODE
    elif brush_type == "MUD":
        brush_color = MUD
    else:
        brush_color = ERASER_COLOR

    brush_label = UI_FONT.render(f"Active Brush: {brush_type}", True, brush_color)
    win.blit(brush_label, (GRID_WIDTH + 20, 120))

    for btn in buttons:
        btn.draw(win)

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
        for node in row:
            node.draw(win)
    draw_grid_lines(win, rows, grid_width)
    draw_ui_panel(win, buttons, current_status, brush_type, metrics)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    x, y = pos
    row = x // gap
    col = y // gap
    return row, col
