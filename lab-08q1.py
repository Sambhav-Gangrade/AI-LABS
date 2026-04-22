import random
import time

DIST = [
    [  0,  10,  15,  20,  25,  30,  35,  40],
    [ 12,   0,  35,  15,  20,  25,  30,  45],
    [ 25,  30,   0,  10,  40,  20,  15,  35],
    [ 18,  25,  12,   0,  15,  30,  20,  10],
    [ 22,  18,  28,  20,   0,  15,  25,  30],
    [ 35,  22,  18,  28,  12,   0,  40,  20],
    [ 30,  35,  22,  18,  28,  32,   0,  15],
    [ 40,  28,  35,  22,  18,  25,  12,   0],
]

CITY_NAME = "ABCDEFGH"


def tour_cost(tour):
    return sum(DIST[tour[i]][tour[(i + 1) % len(tour)]] for i in range(len(tour)))


def tour_string(tour):
    return " -> ".join(CITY_NAME[c] for c in tour) + f" -> {CITY_NAME[tour[0]]}"


def random_tour():
    rest = list(range(1, 8))
    random.shuffle(rest)
    return [0] + rest


def get_neighbors(tour):
    neighbors = []
    n = len(tour)
    for i in range(1, n - 1):
        for j in range(i + 1, n):
            new_tour = tour[:]
            new_tour[i:j + 1] = reversed(new_tour[i:j + 1])
            neighbors.append(new_tour)
    return neighbors


def local_beam_search(k, max_iterations=500, seed=42):
    random.seed(seed)
    beam = [random_tour() for _ in range(k)]
    best = min(beam, key=tour_cost)
    best_cost = tour_cost(best)
    history = [best_cost]
    no_improve = 0

    print(f"\n{'─'*60}")
    print(f"  LOCAL BEAM SEARCH  |  k = {k}")
    print(f"{'─'*60}")
    print(f"  Initial best tour : {tour_string(best)}")
    print(f"  Initial best cost : {best_cost}")

    for iteration in range(1, max_iterations + 1):
        all_neighbors = []
        for state in beam:
            all_neighbors.extend(get_neighbors(state))

        all_neighbors.sort(key=tour_cost)
        beam = all_neighbors[:k]

        iteration_best_cost = tour_cost(beam[0])
        history.append(iteration_best_cost)

        if iteration_best_cost < best_cost:
            best = beam[0][:]
            best_cost = iteration_best_cost
            no_improve = 0
        else:
            no_improve += 1

        if no_improve >= 30:
            print(f"  Converged at iteration {iteration}")
            break

    print(f"  Final best tour   : {tour_string(best)}")
    print(f"  Final best cost   : {best_cost}")
    return best, best_cost, history, iteration


def run_beam_comparison():
    print("\n" + "="*60)
    print("   PART 1 - LOCAL BEAM SEARCH (TSP)")
    print("="*60)

    results = {}
    for k in [3, 5, 10]:
        t0 = time.perf_counter()
        best_tour, best_cost, history, iters = local_beam_search(k)
        elapsed = time.perf_counter() - t0
        results[k] = {"tour": best_tour, "cost": best_cost, "iters": iters, "time": elapsed}

    print("\n\n  -- COMPARATIVE SUMMARY --")
    print(f"  {'k':>4}  {'Best Cost':>10}  {'Iterations':>11}  {'Time (s)':>9}")
    print(f"  {'─'*4}  {'─'*10}  {'─'*11}  {'─'*9}")
    for k, r in results.items():
        print(f"  {k:>4}  {r['cost']:>10}  {r['iters']:>11}  {r['time']:>9.4f}")
    return results


def tournament_selection(population, k=3):
    candidates = random.sample(population, k)
    return min(candidates, key=tour_cost)


def order_crossover_1point(p1, p2):
    n = len(p1)
    cut = random.randint(1, n - 1)
    child = [None] * n
    child[:cut] = p1[:cut]
    filled = set(child[:cut])
    pos = cut
    for city in p2:
        if city not in filled:
            child[pos % n] = city
            pos += 1
            if pos - cut == n - cut:
                break
    return child


def order_crossover_2point(p1, p2):
    n = len(p1)
    i, j = sorted(random.sample(range(n), 2))
    child = [None] * n
    child[i:j + 1] = p1[i:j + 1]
    filled = set(child[i:j + 1])
    pos = (j + 1) % n
    for city in p2[j + 1:] + p2[:j + 1]:
        if city not in filled:
            child[pos] = city
            filled.add(city)
            pos = (pos + 1) % n
    return child


def mutate(tour, mutation_rate=0.15):
    if random.random() < mutation_rate:
        i, j = random.sample(range(1, len(tour)), 2)
        tour[i], tour[j] = tour[j], tour[i]
    return tour


def genetic_algorithm(crossover_points=1, pop_size=50, generations=300,
                      mutation_rate=0.15, elite_size=2, seed=42):
    random.seed(seed)
    label = f"{crossover_points}-point crossover"
    crossover_fn = order_crossover_1point if crossover_points == 1 else order_crossover_2point

    population = [random_tour() for _ in range(pop_size)]
    population.sort(key=tour_cost)

    best = population[0][:]
    best_cost = tour_cost(best)
    history = [best_cost]
    no_improve = 0

    print(f"\n{'─'*60}")
    print(f"  GENETIC ALGORITHM  |  {label}")
    print(f"{'─'*60}")
    print(f"  Population size  : {pop_size}")
    print(f"  Generations      : {generations}")
    print(f"  Mutation rate    : {mutation_rate}")
    print(f"  Elite size       : {elite_size}")
    print(f"  Initial best     : {tour_string(best)}  cost={best_cost}")

    for gen in range(1, generations + 1):
        new_population = population[:elite_size]

        while len(new_population) < pop_size:
            parent1 = tournament_selection(population)
            parent2 = tournament_selection(population)
            child = mutate(crossover_fn(parent1, parent2), mutation_rate)
            new_population.append(child)

        new_population.sort(key=tour_cost)
        population = new_population

        gen_best_cost = tour_cost(population[0])
        history.append(gen_best_cost)

        if gen_best_cost < best_cost:
            best = population[0][:]
            best_cost = gen_best_cost
            no_improve = 0
        else:
            no_improve += 1

        if no_improve >= 50:
            print(f"  Converged at generation {gen}")
            break

    print(f"  Final best tour  : {tour_string(best)}")
    print(f"  Final best cost  : {best_cost}")
    return best, best_cost, history, gen


def run_ga_comparison():
    print("\n" + "="*60)
    print("   PART 2 - GENETIC ALGORITHM (TSP)")
    print("="*60)

    results = {}
    for cp in [1, 2]:
        t0 = time.perf_counter()
        best_tour, best_cost, history, gens = genetic_algorithm(crossover_points=cp)
        elapsed = time.perf_counter() - t0
        results[cp] = {"tour": best_tour, "cost": best_cost, "gens": gens, "time": elapsed}

    print("\n\n  -- COMPARATIVE SUMMARY --")
    print(f"  {'Crossover':>12}  {'Best Cost':>10}  {'Generations':>12}  {'Time (s)':>9}")
    print(f"  {'─'*12}  {'─'*10}  {'─'*12}  {'─'*9}")
    for cp, r in results.items():
        print(f"  {f'{cp}-point':>12}  {r['cost']:>10}  {r['gens']:>12}  {r['time']:>9.4f}")
    return results


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("   TRAVELING SALESPERSON PROBLEM - FULL SOLUTION")
    print("=" * 60)

    beam_results = run_beam_comparison()
    ga_results   = run_ga_comparison()

    print("\n" + "="*60)
    print("  OVERALL BEST SOLUTIONS")
    print("="*60)

    all_results = {}
    for k, r in beam_results.items():
        all_results[f"Beam k={k}"] = r["cost"]
    for cp, r in ga_results.items():
        all_results[f"GA {cp}-pt"] = r["cost"]

    for label, cost in sorted(all_results.items(), key=lambda x: x[1]):
        print(f"  {label:>12}  ->  cost = {cost}")

    best_label = min(all_results, key=all_results.get)
    print(f"\n  Best method overall: {best_label}  (cost = {all_results[best_label]})\n")