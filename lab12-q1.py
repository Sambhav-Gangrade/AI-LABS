
conflicts = {
    'P1': ['P2','P3','P6'],
    'P2': ['P1','P3','P4'],
    'P3': ['P1','P2','P5'],
    'P4': ['P2','P6'],
    'P5': ['P3','P6'],
    'P6': ['P1','P4','P5'],
}

teams = list(conflicts.keys())
rooms = ['R1', 'R2', 'R3']

domains = {team: set(rooms) for team in teams}

def revise(domains, xi, xj):
    removed = []
    for v in list(domains[xi]):
        has_support = any(w != v for w in domains[xj])
        if not has_support:
            domains[xi].remove(v)
            removed.append(v)
    return removed


def ac3(domains, conflicts):
    queue = []
    for xi in conflicts:
        for xj in conflicts[xi]:
            queue.append((xi, xj))

    arc_number = 0
    print("── Arc Processing Trace ──────────────────────")

    while queue:
        xi, xj = queue.pop(0)      
        arc_number += 1
        removed = revise(domains, xi, xj)

        if removed:
            print(f"  Arc {arc_number}: ({xi},{xj}) → removed {removed} from {xi} | {xi}={domains[xi]}")
            if len(domains[xi]) == 0:
                print(f"  CONTRADICTION: {xi} has empty domain!")
                return False
            for xk in conflicts[xi]:
                if xk != xj:
                    queue.append((xk, xi))
        else:
            print(f"  Arc {arc_number}: ({xi},{xj}) → no change | {xi}={domains[xi]}")

    return True

print("INITIAL DOMAINS:")
for t in teams:
    print(f"  {t} = {domains[t]}")
print()

result = ac3(domains, conflicts)

print()
print("── Result ────────────────────────────────────────")
if result:
    print("Arc-consistent: YES — no domains changed (expected)")
    for t in teams:
        print(f"  {t} = {domains[t]}")

print()
print("=" * 50)
print("WHAT IF P1 is pre-assigned to R1?")
print("=" * 50)

domains2 = {team: set(rooms) for team in teams}
domains2['P1'] = {'R1'}

print("\nDOMAINS AFTER PRE-ASSIGNMENT:")
for t in teams:
    print(f"  {t} = {domains2[t]}")
print()

result2 = ac3(domains2, conflicts)

print()
print("── Result ────────────────────────────────────────")
if result2:
    solved = all(len(domains2[t]) == 1 for t in teams)
    print(f"Arc-consistent: YES  |  Fully solved: {solved}")
    for t in teams:
        status = "FIXED" if len(domains2[t]) == 1 else f"{len(domains2[t])} choices left"
        print(f"  {t} = {domains2[t]}  ({status})")
else:
    print("Arc-consistent: NO — contradiction found")