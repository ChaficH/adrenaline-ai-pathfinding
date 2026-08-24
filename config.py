import pygame

# Initialize pygame modules (required for font rendering)
pygame.init()

# --- WINDOW & GRID DIMENSIONS ---
GRID_WIDTH = 800
UI_WIDTH = 340
TOTAL_WIDTH = GRID_WIDTH + UI_WIDTH
HEIGHT = 800
ROWS = 40

# --- FONTS ---
TITLE_FONT = pygame.font.SysFont("Segoe UI", 28, bold=True)
UI_FONT = pygame.font.SysFont("Segoe UI", 18, bold=True)
INFO_FONT = pygame.font.SysFont("Segoe UI", 16)
METRIC_FONT = pygame.font.SysFont("Courier New", 17, bold=True)

# --- COLORS (Aesthetic Theme) ---
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

# --- BUTTON COLORS ---
BTN_DEFAULT = (60, 60, 70)
BTN_HOVER = (90, 90, 105)
