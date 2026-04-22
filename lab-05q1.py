class State():
    def __init__(self, boysLeft, girlsLeft, boat, boysRight, girlsRight, action):
        self.boysLeft = boysLeft
        self.girlsLeft = girlsLeft
        self.boat = boat
        self.boysRight = boysRight
        self.girlsRight = girlsRight
        self.action = action
        self.parent = None

    def is_goal(self):
        return self.boysLeft == 0 and self.girlsLeft == 0

    def is_valid(self):
        if self.girlsLeft < 0 or self.girlsRight < 0 or self.boysLeft < 0 or self.boysRight < 0:
            return False
        if (self.girlsLeft > 0 and self.girlsLeft < self.boysLeft):
            return False
        if (self.girlsRight > 0 and self.girlsRight < self.boysRight):
            return False
        return True

    def __eq__(self, other):
        return (self.boysLeft == other.boysLeft and 
                self.girlsLeft == other.girlsLeft and 
                self.boat == other.boat and 
                self.boysRight == other.boysRight and 
                self.girlsRight == other.girlsRight)


def successors(cur_state):
    children = list()
    moves = [(2, 0, "Two Girls"), (0, 2, "Two Boys"), 
             (1, 1, "One of each"), (1, 0, "One Girl"), (0, 1, "One Boy")]
    
    if cur_state.boat == 'left':
        for g, b, name in moves:
            new_state = State(cur_state.boysLeft - b, cur_state.girlsLeft - g, 'right',
                              cur_state.boysRight + b, cur_state.girlsRight + g,
                              f"Send {name} from Left to Right")
            if new_state.is_valid():
                new_state.parent = cur_state
                children.append(new_state)
    else:
        for g, b, name in moves:
            new_state = State(cur_state.boysLeft + b, cur_state.girlsLeft + g, 'left',
                              cur_state.boysRight - b, cur_state.girlsRight - g,
                              f"Send {name} from Right to Left")
            if new_state.is_valid():
                new_state.parent = cur_state
                children.append(new_state)
    return children


def is_cycle(node):
    ancestor = node.parent
    while ancestor:
        if node == ancestor:
            return True
        ancestor = ancestor.parent
    return False


# --- Modified DLS to return (result, count) ---
def depth_limited_search(node, depth):
    count = 1  # Count current node

    if node.is_goal():
        return node, count
    elif depth == 0:
        return None, count
    else:
        for child in successors(node):
            if not is_cycle(child):
                result, child_count = depth_limited_search(child, depth - 1)
                count += child_count
                if result:
                    return result, count
        return None, count


def iterative_deepening_search(root, max_depth):
    total_explored = 0
    for i in range(max_depth + 1):
        print(f"Searching at Depth {i}...")
        result, count = depth_limited_search(root, i)
        total_explored += count
        if result:
            print(f"Total states explored: {total_explored}")
            return result
    print(f"Total states explored: {total_explored}")
    return None


def print_solution(solution):
    path = []
    curr = solution
    while curr:
        path.append(curr)
        curr = curr.parent
    path.reverse()

    print(f"{'Step':<5} | {'Action':<35} | {'State (B,G,Boat,B,G)':<20}")
    print("-" * 70)
    for i, state in enumerate(path):
        state_str = f"<{state.boysLeft},{state.girlsLeft},{state.boat},{state.boysRight},{state.girlsRight}>"
        print(f"{i:<5} | {state.action:<35} | {state_str:<20}")


def main():
    initial_state = State(3, 3, 'left', 0, 0, "Start")

    print("--- Depth Limited Search ---")
    sol_dls, count = depth_limited_search(initial_state, 3)
    if sol_dls:
        print_solution(sol_dls)
        print(f"States explored in DLS: {count}")
    else:
        print("No solution found at depth 3.")
        print(f"States explored in DLS: {count}")

    print("\n--- Iterative Deepening Search ---")
    sol_ids = iterative_deepening_search(initial_state, 20)
    if sol_ids:
        print("\nOptimal Solution Found:")
        print_solution(sol_ids)
    else:
        print("No solution found within max depth.")


if __name__ == "__main__":
    main()