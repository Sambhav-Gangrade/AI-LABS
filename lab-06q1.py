cities = [
    "Syracuse", "Buffalo", "Pittsburgh", "Cleveland", "Columbus",
    "Detroit", "Chicago", "Indianapolis", "Boston", "New York",
    "Philadelphia", "Providence", "Baltimore", "Portland"
]

INF = 9999
n = 14
adj_matrix = [[INF] * n for _ in range(n)]

def connect(city1, city2, miles):
    idx1 = cities.index(city1)
    idx2 = cities.index(city2)
    adj_matrix[idx1][idx2] = miles
    adj_matrix[idx2][idx1] = miles


connect("Syracuse", "Buffalo", 150)
connect("Syracuse", "Boston", 312)
connect("Syracuse", "New York", 253)
connect("Syracuse", "Philadelphia", 254)
connect("Buffalo", "Detroit", 256)
connect("Buffalo", "Cleveland", 189)
connect("Buffalo", "Pittsburgh", 215)
connect("Boston", "New York", 215)
connect("Boston", "Providence", 50) 
connect("Boston", "Portland", 107)
connect("New York", "Philadelphia", 101)
connect("New York", "Providence", 181)
connect("Philadelphia", "Baltimore", 101)
connect("Philadelphia", "Pittsburgh", 305)
connect("Baltimore", "Pittsburgh", 247)
connect("Pittsburgh", "Cleveland", 134)
connect("Pittsburgh", "Columbus", 185)
connect("Cleveland", "Detroit", 169)
connect("Cleveland", "Columbus", 144)
connect("Cleveland", "Chicago", 345)
connect("Detroit", "Chicago", 283)
connect("Columbus", "Indianapolis", 176)
connect("Indianapolis", "Chicago", 182)

heuristics = {
    "Boston": 0, "Providence": 50, "Portland": 107, "New York": 215,
    "Philadelphia": 270, "Baltimore": 360, "Syracuse": 260, "Buffalo": 400,
    "Pittsburgh": 470, "Cleveland": 550, "Columbus": 640, "Detroit": 610,
    "Indianapolis": 780, "Chicago": 860
}

def get_neighbors(u_idx):
    neighbors = []
    for v_idx in range(n):
        if adj_matrix[u_idx][v_idx] != INF:
            neighbors.append((v_idx, adj_matrix[u_idx][v_idx]))
    return neighbors

def get_path(parents, start_idx, goal_idx):
    path = []
    curr = goal_idx
    while curr != -1:
        path.append(cities[curr])
        curr = parents[curr]
    return path[::-1]

def greedy_bfs(start, goal):
    start_idx = cities.index(start)
    goal_idx = cities.index(goal)

    open_list = [(heuristics[start], start_idx)]
    parents = [-1] * n
    visited = [False] * n
    explored_count = 0
    
    while open_list:
    
        open_list.sort(key=lambda x: x[0])
        h, u = open_list.pop(0)
        
        if visited[u]:
            continue
        visited[u] = True
        explored_count += 1
        
        if u == goal_idx:
            return get_path(parents, start_idx, goal_idx), explored_count
        
        for v, weight in get_neighbors(u):
            if not visited[v]:
                
                parents[v] = u
                open_list.append((heuristics[cities[v]], v))
                
    return None, explored_count

def a_star(start, goal):
    start_idx = cities.index(start)
    goal_idx = cities.index(goal)
    
    open_list = [(heuristics[start], 0, start_idx)]
    parents = [-1] * n
    g_scores = [INF] * n
    g_scores[start_idx] = 0
    visited = [False] * n
    explored_count = 0
    
    while open_list:
        
        open_list.sort(key=lambda x: x[0])
        f, g, u = open_list.pop(0)
        
        if visited[u]:
            continue
        visited[u] = True
        explored_count += 1
        
        if u == goal_idx:
            return get_path(parents, start_idx, goal_idx), explored_count
        
        for v, weight in get_neighbors(u):
            new_g = g + weight
            if new_g < g_scores[v]:
                g_scores[v] = new_g
                new_f = new_g + heuristics[cities[v]]
                parents[v] = u
                open_list.append((new_f, new_g, v))
                
    return None, explored_count

g_path, g_count = greedy_bfs("Chicago", "Boston")
a_path, a_count = a_star("Chicago", "Boston")

print("Greedy Best-First Search:")
print(f"Path: {g_path}")
print(f"Cities Explored: {g_count}")
print("-" * 30)
print("A* Search:")
print(f"Path: {a_path}")
print(f"Cities Explored: {a_count}")