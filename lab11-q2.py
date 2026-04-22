def solve_send_more_money_csp():
    """
    Optimized CSP solver for:
        SEND
      + MORE
      ------
       MONEY

    Variables: S, E, N, D, M, O, R, Y
    Domains: 0..9 with all-different constraint
    Extra constraints: S != 0, M != 0
    """

    letters = ["S", "E", "N", "D", "M", "O", "R", "Y"]
    assigned = {}
    used_digits = set()
    stats = {
        "assign_attempts": 0,
        "column_checks": 0,
    }

    def domain(var):
        d = set(range(10)) - used_digits
        if var in ("S", "M"):
            d.discard(0)
        return d

    def assign(var, digit):
        stats["assign_attempts"] += 1
        if var in assigned:
            return assigned[var] == digit
        if digit in used_digits:
            return False
        if var in ("S", "M") and digit == 0:
            return False
        assigned[var] = digit
        used_digits.add(digit)
        return True

    def unassign(var):
        if var in assigned:
            used_digits.remove(assigned[var])
            del assigned[var]

    def values_for(var):
        return sorted(domain(var))

    def solve_column(col, carry):
        stats["column_checks"] += 1
        # Process columns right to left:
        # 0: D + E = Y + 10*c1
        # 1: N + R + c1 = E + 10*c2
        # 2: E + O + c2 = N + 10*c3
        # 3: S + M + c3 = O + 10*c4
        # 4: c4 == M

        if col == 0:
            return solve_equation("D", "E", "Y", carry, 1)
        if col == 1:
            return solve_equation("N", "R", "E", carry, 2)
        if col == 2:
            return solve_equation("E", "O", "N", carry, 3)
        if col == 3:
            return solve_equation("S", "M", "O", carry, 4)
        if col == 4:
            # Final carry becomes the leftmost digit M.
            return "M" in assigned and carry == assigned["M"]
        return False

    def solve_equation(a, b, c, carry_in, next_col):
        # a + b + carry_in = c + 10 * carry_out
        vars_needed = [v for v in (a, b, c) if v not in assigned]

        # MRV-style ordering: assign the tightest domain first.
        vars_needed.sort(key=lambda x: len(domain(x)))

        def assign_needed(i):
            if i == len(vars_needed):
                av, bv, cv = assigned[a], assigned[b], assigned[c]
                total = av + bv + carry_in
                if total % 10 != cv:
                     return False
                carry_out = total // 10
                return solve_column(next_col, carry_out)

            var = vars_needed[i]
            for digit in values_for(var):
                if not assign(var, digit):
                    continue
                if assign_needed(i + 1):
                    return True
                unassign(var)
            return False

        return assign_needed(0)

    print("Starting optimized CSP backtracking search...")
    found = solve_column(0, 0)

    if not found:
        print("No solution found.")
        return

    S = assigned["S"]
    E = assigned["E"]
    N = assigned["N"]
    D = assigned["D"]
    M = assigned["M"]
    O = assigned["O"]
    R = assigned["R"]
    Y = assigned["Y"]

    send = 1000 * S + 100 * E + 10 * N + D
    more = 1000 * M + 100 * O + 10 * R + E
    money = 10000 * M + 1000 * O + 100 * N + 10 * E + Y

    print("Solution Found (CSP optimized)!")
    print(f"S={S}, E={E}, N={N}, D={D}, M={M}, O={O}, R={R}, Y={Y}")
    print(f"\n  {send}")
    print(f"+ {more}")
    print("-------")
    print(f" {money}")
    print("\nSearch effort stats:")
    print(f"  Assignment attempts: {stats['assign_attempts']}")
    print(f"  Column checks      : {stats['column_checks']}")


solve_send_more_money_csp()