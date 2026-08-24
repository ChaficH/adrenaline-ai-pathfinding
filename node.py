import pygame
from config import (
    OBSIDIAN,
    WALL,
    START_NODE,
    END_NODE,
    SEARCH_HEAD,
    FRONTIER,
    VISITED,
    PATH,
    MUD
)


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

    def get_pos(self):
        return self.row, self.col

    def is_wall(self):
        return self.color == WALL

    def is_mud(self):
        return self.weight == 10

    def reset(self):
        self.color = OBSIDIAN
        self.weight = 1

    def make_head(self):
        self.color = SEARCH_HEAD

    def make_closed(self):
        self.color = VISITED

    def make_open(self):
        self.color = FRONTIER

    def make_wall(self):
        self.color = WALL
        self.weight = float('inf')

    def make_mud(self):
        self.color = MUD
        self.weight = 10

    def make_start(self):
        self.color = START_NODE

    def make_end(self):
        self.color = END_NODE

    def make_path(self):
        self.color = PATH

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
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_wall():  # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].is_wall():  # UP
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_wall():  # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].is_wall():  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])
