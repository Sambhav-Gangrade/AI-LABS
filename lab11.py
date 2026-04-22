adjacency = {
    "Kuchchh":       ["Banaskantha", "Patan", "Surendranagar", "Rajkot", "Jamnagar"],
    "Banaskantha":   ["Kuchchh", "Patan", "Sabarkantha", "Mehsana"],
    "Patan":         ["Kuchchh", "Banaskantha", "Mehsana", "Surendranagar"],
    "Mehsana":       ["Banaskantha", "Patan", "Sabarkantha", "GandhiNagar", "Ahmedabad", "Surendranagar"],
    "Sabarkantha":   ["Banaskantha", "Mehsana", "GandhiNagar", "Kheda", "Panchmahal"],
    "GandhiNagar":   ["Mehsana", "Sabarkantha", "Ahmedabad", "Kheda"],
    "Ahmedabad":     ["Mehsana", "GandhiNagar", "Surendranagar", "Kheda", "Anand", "Bhavnagar"],
    "Surendranagar": ["Kuchchh", "Patan", "Mehsana", "Ahmedabad", "Bhavnagar", "Rajkot"],
    "Kheda":         ["GandhiNagar", "Sabarkantha", "Ahmedabad", "Anand", "Vadodara", "Panchmahal"],
    "Anand":         ["Ahmedabad", "Kheda", "Vadodara", "Bharuch"],
    "Panchmahal":    ["Sabarkantha", "Kheda", "Vadodara", "Dahod"],
    "Dahod":         ["Panchmahal", "Vadodara"],
    "Vadodara":      ["Kheda", "Anand", "Panchmahal", "Dahod", "Bharuch", "Narmada"],
    "Jamnagar":      ["Kuchchh", "Rajkot", "Porbandar"],
    "Rajkot":        ["Kuchchh", "Jamnagar", "Surendranagar", "Amreli", "Bhavnagar"],
    "Porbandar":     ["Jamnagar", "Rajkot", "Junaghad"],
    "Junaghad":      ["Porbandar", "Rajkot", "Amreli"],
    "Amreli":        ["Rajkot", "Junaghad", "Bhavnagar"],
    "Bhavnagar":     ["Surendranagar", "Ahmedabad", "Rajkot", "Amreli", "Bharuch"],
    "Bharuch":       ["Anand", "Vadodara", "Bhavnagar", "Narmada", "Surat"],
    "Narmada":       ["Vadodara", "Bharuch", "Surat"],
    "Surat":         ["Bharuch", "Narmada", "Navsari", "Dangs"],
    "Navsari":       ["Surat", "Valsad", "Dangs"],
    "Dangs":         ["Surat", "Navsari"],
    "Valsad":        ["Navsari"],
}

def is_valid(district, color, assignment):
    for neighbor in adjacency[district]:
        if assignment.get(neighbor) == color:
            return False
    return True
.0

def backtrack(assignment, districts, colors):

    if len(assignment) == len(districts):
        return assignment


    unassigned = [d for d in districts if d not in assignment]
    district = unassigned[0]  

    for color in colors:
        if is_valid(district, color, assignment):
            assignment[district] = color
            result = backtrack(assignment, districts, colors)
            if result:
                return result
            del assignment[district]

    return None

districts = list(adjacency.keys())
colors = ["Red", "Green", "Blue", "Yellow"]

solution = backtrack({}, districts, colors)

if solution:
    print(f"Solution found using {len(set(solution.values()))} colors:\n")
    for district, color in solution.items():
        print(f"  {district:<15} -> {color}")
else:
    print("No solution found.")