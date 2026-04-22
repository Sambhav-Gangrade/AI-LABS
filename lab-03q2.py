RULES = [
    {
        "percept": {
            "Train": True,
            "Obstacle": True,
            "Emergency": True
        },
        "action": {
            "Gate": "Lower",
            "Siren": "ON",
            "Train Signal": "RED"
        }
    },
    {
        "percept": {
            "Train": True,
            "Obstacle": True,
            "Emergency": False
        },
        "action": {
            "Gate": "Lower",
            "Siren": "ON",
            "Train Signal": "RED"
        }
    },
    {
        "percept": {
            "Train": True,
            "Obstacle": False,
            "Emergency": False
        },
        "action": {
            "Gate": "Lower",
            "Siren": "ON",
            "Train Signal": "GREEN"
        }
    },
    {
        "percept": {
            "Train": False,
            "Obstacle": False,
            "Emergency": False
        },
        "action": {
            "Gate": "Raise",
            "Siren": "OFF",
            "Train Signal": "GREEN"
        }
    }
]

def level_crossing_agent(percept):
    for rule in RULES:
        if rule["percept"] == percept:
            return rule["action"]

    return {"Gate": "Lower", "Siren": "ON", "Train Signal": "RED"}
scenarios = [
    ("Idle State",               {"Train": False, "Obstacle": False, "Emergency": False}),
    ("Train Approaching",         {"Train": True,  "Obstacle": False, "Emergency": False}),
    ("Obstacle Detected",         {"Train": True,  "Obstacle": True,  "Emergency": False}),
    ("Emergency Lever Pulled",    {"Train": True,  "Obstacle": False, "Emergency": True}),
    ("Obstacle, No Train",        {"Train": False, "Obstacle": True,  "Emergency": False}),
    ("Emergency Only",            {"Train": False, "Obstacle": False, "Emergency": True}),
    ("All Clear Again",           {"Train": False, "Obstacle": False, "Emergency": False})
]

print(f"{'Step':<5} | {'Scenario':<25} | {'Train':<6} | {'Obstacle':<8} | {'Emergency':<9} | Actions")
print("-" * 67)

for step, (desc, percept) in enumerate(scenarios, start=1):
    action = level_crossing_agent(percept)

    print(
        f"{step:<5} | {desc:<25} | "
        f"{str(percept['Train']):<6} | "
        f"{str(percept['Obstacle']):<8} | "
        f"{str(percept['Emergency']):<9} | "
        f"Gate: {action['Gate']}, Siren: {action['Siren']}, Train Signal: {action['Train Signal']}"
    )

print("Complete")
