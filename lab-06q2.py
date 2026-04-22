
MAZE = [
    [2, 0, 0, 0, 1],
    [0, 1, 0, 0, 3],
    [0, 3, 0, 1, 1],
    [0, 1, 0, 0, 1],
    [3, 0, 0, 0, 3],
]

ROWS, COLS = 5, 5


MOVES = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def get_dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_positions():
    start = None
    rewards = []
    exits = []
    for r in range(ROWS):
        for c in range(COLS):
            if MAZE[r][c] == 2: start = (r, c)
            if MAZE[r][c] == 3: rewards.append((r, c))

            if MAZE[r][c] != 1 and (r in [0, 4] or c in [0, 4]):
                exits.append((r, c))
    return start, rewards, exits

def astar(start, goal):

  
    open_list = [(get_dist(start, goal), 0, start, [])]
    visited = set()

    while open_list:
    
        open_list.sort(key=lambda x: x[0])
        _, g, current, path = open_list.pop(0)

        if current in visited: continue
        visited.add(current)
        
        path = path + [current]

        if current == goal:
            return path 

        for dr, dc in MOVES:
            nr, nc = current[0] + dr, current[1] + dc
            if 0 <= nr < ROWS and 0 <= nc < COLS and MAZE[nr][nc] != 1:
                if (nr, nc) not in visited:
                    new_g = g + 1
                    new_f = new_g + get_dist((nr, nc), goal)
                    open_list.append((new_f, new_g, (nr, nc), path))
    return []

def main():
    start, rewards, exits = get_positions()
    current = start
    full_path = []

    print(f"Start: {start}")
    print(f"Rewards to find: {rewards}")

    
    while rewards:
       
        rewards.sort(key=lambda r: get_dist(current, r))
        next_reward = rewards.pop(0) 
        
        print(f"\nTargeting Reward at {next_reward}...")
        path_segment = astar(current, next_reward)
        
      
        if full_path: full_path.extend(path_segment[1:])
        else: full_path.extend(path_segment)    
            
        current = next_reward

  
    exits.sort(key=lambda e: get_dist(current, e))
    best_exit = exits[0]
    
    print(f"\nAll rewards collected. Exiting to {best_exit}...")
    path_segment = astar(current, best_exit)
    full_path.extend(path_segment[1:])

    print("-" * 30)
    print("FINAL PATH SEQUENCE:")
    print(full_path)
    print(f"Total Steps: {len(full_path) - 1}")

if __name__ == "__main__":
    main()