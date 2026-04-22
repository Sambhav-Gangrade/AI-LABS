import random
import math


def random_state(n=8):
    """Generates a random board (1 queen per column)."""
    return [random.randint(0, n - 1) for _ in range(n)]

def evaluate(state):
    """
    Heuristic: Number of pairs of attacking queens.
    Goal is 0.
    """
    conflicts = 0
    n = len(state)
    for i in range(n):
        for j in range(i + 1, n):
            # Same row
            if state[i] == state[j]:
                conflicts += 1
            # Same diagonal
            elif abs(state[i] - state[j]) == abs(i - j):
                conflicts += 1
    return conflicts

def get_neighbors(state):
    """Generates all neighbors by moving each queen to every other row."""
    n = len(state)
    neighbors = []
    for col in range(n):
        for row in range(n):
            if state[col] != row:
                neighbor = list(state)
                neighbor[col] = row
                neighbors.append(neighbor)
    return neighbors



def steepest_ascent(state, max_steps=1000):
    """
    Q1: Moves to the BEST neighbor.
    Returns: (final_state, final_cost, steps, is_solved)
    """
    current = state
    current_cost = evaluate(current)
    steps = 0
    
    for _ in range(max_steps):
        if current_cost == 0:
            return current, current_cost, steps, True
            
        neighbors = get_neighbors(current)

        best_neighbor = min(neighbors, key=evaluate)
        best_neighbor_cost = evaluate(best_neighbor)
        
        if best_neighbor_cost >= current_cost:
            return current, current_cost, steps, False
            
        current = best_neighbor
        current_cost = best_neighbor_cost
        steps += 1
        
    return current, current_cost, steps, False

def first_choice(state, max_steps=1000):
    """
    Q2: Moves to the FIRST neighbor that is better.
    """
    current = state
    current_cost = evaluate(current)
    steps = 0
    
    for _ in range(max_steps):
        if current_cost == 0:
            return current, current_cost, steps, True
        
        neighbors = get_neighbors(current)
        random.shuffle(neighbors)
        
        found_better = False
        for neighbor in neighbors:
            cost = evaluate(neighbor)
            if cost < current_cost:
                current = neighbor
                current_cost = cost
                found_better = True
                break
        
        if not found_better:
            return current, current_cost, steps, False
            
        steps += 1
        
    return current, current_cost, steps, False

def random_restart(n=8, max_restarts=100):
    """
    Q2: Restarts with a new random board if it gets stuck.
    """
    total_steps = 0
    for _ in range(max_restarts):
        initial = random_state(n)
        state, cost, steps, solved = steepest_ascent(initial)
        total_steps += steps
        if solved:
            return state, cost, total_steps, True
            
    return state, cost, total_steps, False

def simulated_annealing(state, max_steps=10000, initial_temp=100, cooling_rate=0.95):
    """
    Q2: Probabilistically accepts worse moves to escape local optima.
    """
    current = state
    current_cost = evaluate(current)
    steps = 0
    temp = initial_temp
    
    for _ in range(max_steps):
        if current_cost == 0:
            return current, current_cost, steps, True
        
        if temp <= 0:
            return current, current_cost, steps, False
            
        
        n = len(current)
        col = random.randint(0, n-1)
        row = random.randint(0, n-1)
        neighbor = list(current)
        neighbor[col] = row
        
        neighbor_cost = evaluate(neighbor)
        delta_e = current_cost - neighbor_cost 
        
        if delta_e > 0 or random.random() < math.exp(delta_e / temp):
            current = neighbor
            current_cost = neighbor_cost
            
        steps += 1
        temp *= cooling_rate
        
    return current, current_cost, steps, False


def run_experiment(algorithm_name, algorithm_func, runs=50):
    print(f"--- Running Experiment: {algorithm_name} ---")
    solved_count = 0
    total_steps_solved = 0
    total_steps_failed = 0
    
    print(f"{'Run':<5} {'Start Cost':<12} {'End Cost':<10} {'Steps':<8} {'Status'}")
    print("-" * 50)

    for i in range(runs):
        initial_state = random_state()
        initial_cost = evaluate(initial_state)
        
        if algorithm_name == "Random Restart":
            final_state, final_cost, steps, solved = algorithm_func()
        else:
            final_state, final_cost, steps, solved = algorithm_func(initial_state)
        
        status = "SOLVED" if solved else "FAIL"
        if i < 5:
            print(f"{i+1:<5} {initial_cost:<12} {final_cost:<10} {steps:<8} {status}")
            
        if solved:
            solved_count += 1
            total_steps_solved += steps
        else:
            total_steps_failed += steps

    avg_steps_success = total_steps_solved / solved_count if solved_count > 0 else 0
    print("-" * 50)
    print(f"Success Rate: {solved_count}/{runs} ({(solved_count/runs)*100}%)")
    print(f"Avg Steps (Successes): {avg_steps_success:.2f}")
    print("\n")



if __name__ == "__main__":
    
    run_experiment("Steepest Ascent", steepest_ascent)
    run_experiment("First Choice", first_choice)
    run_experiment("Random Restart", random_restart)
    run_experiment("Simulated Annealing", simulated_annealing)