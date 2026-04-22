def is_goal(state):
    _, A, B = state
    return A == "Clean" and B == "Clean"


def get_results(state, action):
    loc, A, B = state
    results = []

    if action == "Suck":
        if loc == "A":
            if A == "Dirty":
                results.append(("A", "Clean", B))
                results.append(("A", "Clean", "Clean"))
            else:
                results.append(("A", "Dirty", B))
                results.append(state)
        else:
            if B == "Dirty":
                results.append(("B", A, "Clean"))
                results.append(("B", "Clean", "Clean"))
            else:
                results.append(("B", A, "Dirty"))
                results.append(state)

    elif action == "Left":
        results.append(("A", A, B))

    elif action == "Right":
        results.append(("B", A, B))

    return results


def and_or_search(state, path):
    if is_goal(state):
        return {"type": "GOAL", "state": state}

    if state in path:
        return None

    for action in ["Suck", "Left", "Right"]:
        results = get_results(state, action)
        subplans = []

        success = True
        for r in results:
            plan = and_or_search(r, path + [state])
            if plan is None:
                success = False
                break
            subplans.append(plan)

        if success:
            return {
                "type": "OR",
                "state": state,
                "action": action,
                "results": subplans
            }

    return None



def print_plan(plan, indent=0):
    space = "  " * indent

    if plan["type"] == "GOAL":
        print(f"{space}✔ Goal reached: {plan['state']}")
        return

    print(f"{space}State: {plan['state']}")
    print(f"{space}→ Action: {plan['action']}")

    for i, sub in enumerate(plan["results"]):
        print(f"{space}  Outcome {i+1}:")
        print_plan(sub, indent + 2)


initial_state = ("A", "Dirty", "Dirty")

plan = and_or_search(initial_state, [])

print("\n=== AND-OR Plan ===\n")
print_plan(plan)