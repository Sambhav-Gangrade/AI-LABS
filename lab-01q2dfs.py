graph = {
    'Raj': ['Priya', 'Akash', 'Sunil'],
    'Priya': ['Raj', 'Aarav', 'Neha_Center'],
    'Aarav': ['Priya', 'Neha_Right', 'Arjun_Right'],
    'Akash': ['Raj', 'Sunil', 'Neha_Center'],
    'Sunil': ['Raj', 'Akash', 'Sneha'],
    'Neha_Center': ['Priya', 'Akash', 'Sneha', 'Rahul', 'Neha_Right'],
    'Neha_Right': ['Aarav', 'Neha_Center', 'Rahul', 'Arjun_Right'],
    'Sneha': ['Sunil', 'Neha_Center', 'Rahul', 'Maya'],
    'Rahul': ['Neha_Center', 'Neha_Right', 'Sneha', 'Arjun_Right', 'Arjun_Bottom', 'Maya', 'Pooja'],
    'Arjun_Right': ['Aarav', 'Neha_Right', 'Rahul', 'Pooja'],
    'Maya': ['Sneha', 'Rahul', 'Arjun_Bottom'],
    'Arjun_Bottom': ['Maya', 'Rahul', 'Pooja'],
    'Pooja': ['Rahul', 'Arjun_Right', 'Arjun_Bottom']
}

def bfs_tree(start_node):
    visited = {start_node}
    queue = [start_node]
    edges = []
    
    while queue:
        current = queue.pop(0)
        for neighbor in graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                edges.append((current, neighbor))
                queue.append(neighbor)
    
    print(f"BFS Tree Edges (starting from {start_node}):")
    for u, v in edges:
        print(f"{u} -> {v}")

def dfs_tree(start_node):
    visited = set()
    stack = [(start_node, None)]
    edges = []
    
    while stack:
        current, parent = stack.pop()
        if current not in visited:
            visited.add(current)
            if parent:
                edges.append((parent, current))
            
            for neighbor in reversed(graph[current]):
                if neighbor not in visited:
                    stack.append((neighbor, current))
                    
    print(f"\nDFS Tree Edges (starting from {start_node}):")
    for u, v in edges:
        print(f"{u} -> {v}")

bfs_tree('Raj')
dfs_tree('Raj')