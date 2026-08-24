import random


def generate_random_maze(grid, rows, start, end):
    # 1. Clear grid entirely, but spare the start and end nodes
    for row in grid:
        for node in row:
            if node != start and node != end:
                node.reset()

    # 2. Set Start/End defaults if they do not exist
    if not start:
        start = grid[4][4]
    if not end:
        end = grid[rows - 5][rows - 5]

    # 2.5 Ensure they display their respective colors
    start.make_start()
    end.make_end()

    # 3. Randomly scatter walls and mud
    for row in grid:
        for node in row:
            if node != start and node != end:
                chance = random.random()
                if chance < 0.32:
                    node.make_wall()
                elif chance < 0.47:
                    node.make_mud()

    # 4. "The Bulldozer": Carve a guaranteed path to target
    curr_r, curr_c = start.get_pos()
    end_r, end_c = end.get_pos()

    while (curr_r, curr_c) != (end_r, end_c):
        moves = []
        if curr_r < end_r:
            moves.append((1, 0))
        if curr_r > end_r:
            moves.append((-1, 0))
        if curr_c < end_c:
            moves.append((0, 1))
        if curr_c > end_c:
            moves.append((0, -1))

        dr, dc = random.choice(moves)
        curr_r += dr
        curr_c += dc

        b_node = grid[curr_r][curr_c]
        if b_node != end and b_node != start:
            # 85% chance to clear space, 15% to leave mud on path
            if random.random() < 0.85:
                b_node.reset()
            else:
                b_node.make_mud()

    return start, end
