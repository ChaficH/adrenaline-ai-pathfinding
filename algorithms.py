import pygame
from queue import PriorityQueue, Queue
from config import START_NODE


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
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)
        nodes_explored += 1

        if current == end:
            path_data = reconstruct_path(came_from, end, draw_func)
            end.make_end()
            return {"algo": "A* Search", "explored": nodes_explored, **path_data}

        if current != start:
            current.make_head()

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
                    if neighbor != end:
                        neighbor.make_open()

        draw_func()
        if current != start:
            current.make_closed()

    return None


def algorithm_bfs(draw_func, grid, start, end):
    nodes_explored = 0
    queue = Queue()
    queue.put(start)
    came_from = {}
    visited = {start}

    while not queue.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = queue.get()
        nodes_explored += 1

        if current == end:
            path_data = reconstruct_path(came_from, end, draw_func)
            end.make_end()
            return {"algo": "BFS", "explored": nodes_explored, **path_data}

        if current != start:
            current.make_head()

        for neighbor in current.neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                queue.put(neighbor)
                if neighbor != end:
                    neighbor.make_open()

        draw_func()
        if current != start:
            current.make_closed()

    return None


def algorithm_dfs(draw_func, grid, start, end):
    nodes_explored = 0
    stack = [start]
    came_from = {}
    visited = {start}

    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = stack.pop()
        nodes_explored += 1

        if current == end:
            path_data = reconstruct_path(came_from, end, draw_func)
            end.make_end()
            return {"algo": "DFS", "explored": nodes_explored, **path_data}

        if current != start:
            current.make_head()

        for neighbor in current.neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                stack.append(neighbor)
                if neighbor != end:
                    neighbor.make_open()

        draw_func()
        if current != start:
            current.make_closed()

    return None
