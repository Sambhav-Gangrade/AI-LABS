def get_neighbors(state):
    neighbors = []
    idx = state.index(0)
    row, col = idx // 3, idx % 3
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r_move, c_move in moves:
        new_row, new_col = row + r_move, col + c_move
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_idx = new_row * 3 + new_col
            new_state = list(state)
            new_state[idx], new_state[new_idx] = new_state[new_idx], new_state[idx]
            neighbors.append(tuple(new_state))
    return neighbors

def dfs_solver(start, goal):
    stack = [(start, 0)]
    visited = {start}
    explored_count = 0
    while stack:
        current_state, depth = stack.pop()
        explored_count += 1
        if current_state == goal:
            return explored_count, depth
        for neighbor in get_neighbors(current_state):
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append((neighbor, depth + 1))
    return -1, -1

start_state = (7, 2, 4, 5, 0, 6, 8, 3, 1)
goal_state = (0, 1, 2, 3, 4, 5, 6, 7, 8)

explored, cost = dfs_solver(start_state, goal_state)
print(f"DFS Explored States: {explored}")
print(f"DFS Cost: {cost}")