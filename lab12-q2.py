from collections import deque


PUZZLE = [
    [0,0,0, 0,0,6, 0,0,0],
    [0,5,9, 0,0,0, 0,0,8],
    [2,0,0, 0,0,8, 0,0,0],
    [0,4,5, 0,0,0, 0,0,0],
    [0,0,3, 0,0,0, 0,0,0],
    [0,0,6, 0,0,3, 0,5,0],
    [0,0,0, 0,0,7, 0,0,0],
    [0,0,0, 0,0,0, 0,0,0],
    [0,0,0, 0,5,0, 0,0,2],
]
domains = {}
for r in range(9):
    for c in range(9):
        key = (r, c)
        val = PUZZLE[r][c]
        domains[key] = {val} if val != 0 else set(range(1, 10))

def peers(r, c):
    p = set()
    for i in range(9):
        if i != c: p.add((r, i)) 
        if i != r: p.add((i, c))   
    br, bc = (r // 3) * 3, (c // 3) * 3
    for dr in range(3):
        for dc in range(3):
            nr, nc = br + dr, bc + dc
            if (nr, nc) != (r, c):
                p.add((nr, nc))     # same box
    return list(p)


arcs = []
for r in range(9):
    for c in range(9):
        for peer in peers(r, c):
            arcs.append(((r, c), peer))

print(f"Total arcs generated: {len(arcs)}")


def revise(domains, xi, xj):
    """Remove values from xi's domain that have no support in xj."""
    revised = False
    for val in list(domains[xi]):
       
        if not any(v != val for v in domains[xj]):
            domains[xi].remove(val)
            revised = True
    return revised

def ac3(domains, arcs):
    queue = deque(arcs)
    eliminations = 0

    while queue:
        xi, xj = queue.popleft()

        before = len(domains[xi])
        if revise(domains, xi, xj):
            after = len(domains[xi])
            eliminations += (before - after)

            if len(domains[xi]) == 0:
                return eliminations, "INVALID"  

            r, c = xi
            for peer in peers(r, c):
                if peer != xj:
                    queue.append((peer, xi))

    return eliminations, "OK"

eliminations, status = ac3(domains, arcs)

solved_cells  = sum(1 for d in domains.values() if len(d) == 1)
ambig_cells   = sum(1 for d in domains.values() if len(d) > 1)


def print_grid(domains, puzzle):
    hline = "+-------+-------+-------+"
    print(hline)
    for r in range(9):
        row = "| "
        for c in range(9):
            sz = len(domains[(r, c)])
            orig = puzzle[r][c]
            cell = "*" if orig != 0 else str(sz) 
            row += cell + " "
            if c % 3 == 2 and c < 8:
                row += "| "
        print(row + "|")
        if r % 3 == 2:
            print(hline)

print("\n── Domain-size grid (1=solved, 2+=ambiguous, *=given) ──")
print_grid(domains, PUZZLE)

print(f"\n── AC-3 Summary ──")
print(f"  Total arcs:      {len(arcs)}")
print(f"  Eliminations:    {eliminations}")
print(f"  Cells solved:    {solved_cells} / 81")
print(f"  Still ambiguous: {ambig_cells}")

if status == "INVALID":
    print("\n  RESULT: INVALID — a domain hit 0, puzzle is unsolvable")
elif solved_cells == 81:
    print("\n  RESULT: FULLY SOLVED by AC-3 alone!")
else:
    print(f"\n  RESULT: STUCK — AC-3 ran out of deductions.")