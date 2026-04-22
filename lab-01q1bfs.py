import heapq

# 1. DATA REPRESENTATION: Adjacency Matrix
# We map each city name to a unique index (0 to 13)
cities = [
    "Syracuse", "Buffalo", "Pittsburgh", "Cleveland", "Columbus", 
    "Detroit", "Chicago", "Indianapolis", "Boston", "New York", 
    "Philadelphia", "Providence", "Baltimore", "Portland"
]
city_to_index = {city: i for i, city in enumerate(cities)}
index_to_city = {i: city for i, city in enumerate(cities)}

n = len(cities)
# Initialize matrix with infinity
INF = float('inf')
adj_matrix = [[INF] * n for _ in range(n)]

# Helper to add bidirectional edges
def add_edge(u_name, v_name, miles):
    u, v = city_to_index[u_name], city_to_index[v_name]
    adj_matrix[u][v] = miles
    adj_matrix[v][u] = miles

# Populate the matrix based on your map image
add_edge("Syracuse", "Buffalo", 150)
add_edge("Syracuse", "Boston", 312)
add_edge("Syracuse", "New York", 254)
add_edge("Syracuse", "Philadelphia", 253)
add_edge("Buffalo", "Detroit", 256)
add_edge("Buffalo", "Cleveland", 189)
add_edge("Buffalo", "Pittsburgh", 215)
add_edge("Boston", "New York", 215)
add_edge("Boston", "Providence", 50)
add_edge("Boston", "Portland", 107)
add_edge("New York", "Philadelphia", 97)
add_edge("New York", "Providence", 181)
add_edge("Philadelphia", "Baltimore", 101)
add_edge("Philadelphia", "Pittsburgh", 305)
add_edge("Baltimore", "Pittsburgh", 247)
add_edge("Pittsburgh", "Cleveland", 134)
add_edge("Pittsburgh", "Columbus", 185)
add_edge("Cleveland", "Detroit", 169)
add_edge("Cleveland", "Columbus", 144)
add_edge("Cleveland", "Chicago", 345) # Visual interpretation of the map line
add_edge("Detroit", "Chicago", 283)
add_edge("Columbus", "Indianapolis", 176)
add_edge("Indianapolis", "Chicago", 182)

# 2. ALGORITHM IMPLEMENTATION (Matching Pseudocode)
class Node:
    def __init__(self, state_index, parent=None, path_cost=0):
        self.state = state_index
        self.parent = parent
        self.path_cost = path_cost
    
    # Comparator for Priority Queue (based on path_cost)
    def __lt__(self, other):
        return self.path_cost < other.path_cost

def expand(node_u):
    """Yields child nodes connected to the current node."""
    u_idx = node_u.state
    for v_idx in range(n):
        cost = adj_matrix[u_idx][v_idx]
        if cost != INF:
            # Create child node
            new_cost = node_u.path_cost + cost
            yield Node(state_index=v_idx, parent=node_u, path_cost=new_cost)

def best_first_search(start_city, goal_city):
    # Setup
    start_idx = city_to_index[start_city]
    goal_idx = city_to_index[goal_city]
    
    # 1. node <- NODE(STATE=problem.INITIAL)
    start_node = Node(start_idx, path_cost=0)
    
    # 2. frontier <- priority queue ordered by f (path_cost), with node as element
    frontier = []
    heapq.heappush(frontier, start_node)
    
    # 3. reached <- lookup table with key problem.INITIAL and value node
    # We store {state_index: Node} to track best paths found so far
    reached = {start_idx: start_node}
    
    nodes_explored_count = 0

    print(f"Starting Search: {start_city} -> {goal_city}")
    print("-" * 40)

    # 4. while not IS-EMPTY(frontier) do
    while frontier:
        # 5. node <- POP(frontier)
        current_node = heapq.heappop(frontier)
        nodes_explored_count += 1
        
        current_city_name = index_to_city[current_node.state]
        
        # 6. if problem.IS-GOAL(node.STATE) then return node
        if current_node.state == goal_idx:
            return current_node, nodes_explored_count

        # 7. for each child in EXPAND(problem, node) do
        for child in expand(current_node):
            s = child.state
            
            # 8. if s is not in reached or child.PATH-COST < reached[s].PATH-COST then
            if s not in reached or child.path_cost < reached[s].path_cost:
                # 9. reached[s] <- child
                reached[s] = child
                # 10. add child to frontier
                heapq.heappush(frontier, child)
                # (Optional visualization print)
                # print(f"   Discovered: {index_to_city[s]} (Total Cost: {child.path_cost})")

    # 11. return failure
    return None, nodes_explored_count

# Helper to reconstruct path
def print_solution(node, explored_count):
    if not node:
        print("Failure: No path found.")
        return

    path = []
    curr = node
    while curr:
        path.append(index_to_city[curr.state])
        curr = curr.parent
    path.reverse()
    
    print(f"Goal Reached: {index_to_city[node.state]}")
    print(f"Total Path Cost: {node.path_cost} miles")
    print(f"Path: {' -> '.join(path)}")
    print(f"Nodes Explored (Popped from Frontier): {explored_count}")

# 3. EXECUTION
solution_node, count = best_first_search("Syracuse", "Chicago")
print("-" * 40)
print_solution(solution_node, count)