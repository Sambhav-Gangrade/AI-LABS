import matplotlib.pyplot as plt
import matplotlib.patches as patches


environment={
    "A":"Dirty",
    "B":"Dirty",
    "C":"Dirty"
}

rules={
    ("A", "Dirty"):"Clean",
    ("A", "Clean"): "Right",
    ("B", "Dirty"): "Clean",
    ("B", "Clean"): "Right",
    ("C", "Dirty"): "Clean",
    ("C", "Clean"): "Left"
}

room_positions={
    "A":(0,0),
    "B":(1,0),
    "C":(2,0)
}

action_cost={
    "Clean":5,
    "Right":-1,
    "Left":-1
}

rooms=list(environment.keys())
agent_position="A"
score=0

def reflex_agent(location,state):
    percept=(location,state)
    return rules.get(percept)

def draw_environment(env,agent_loc,step,score):
    fig,ax=plt.subplots()
    ax.set_xlim(0,3)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(f"Step {step} - The Agent is in {agent_loc} | Score is {score}")

    for room,pos in room_positions.items():
        x,y=pos
        color="red" if env[room]=="Dirty" else "green"
        rect=patches.Rectangle((x,y),1,1,facecolor=color,edgecolor="black")
        ax.add_patch(rect)  
        ax.text(x+0.5,y+0.5,room,ha='center',va='center',color='white')
    agent_x,agent_y=room_positions[agent_loc]
    agent_patch=patches.Circle((agent_x+0.5,agent_y+0.5),0.1,color="blue")
    ax.add_patch(agent_patch)
    plt.pause(0.7)
    plt.close() 


plt.ion()
steps=11
print(f"{'step':<5} | {'room':<5} | {'state':<5} | {'action':<5}")
print('-'*67)
for step in range(steps):
    state=environment[agent_position]
    
    action=reflex_agent(agent_position,state)
    
    score += action_cost.get(action)
    
    print(f"{step+1:<5} | {agent_position:<5} | {state:<5} | {action:<5}")

    draw_environment(environment,agent_position,step+1,score)
    
    if action=="Clean":
        environment[agent_position]="Clean"

    elif action=="Right":
        idx = rooms.index(agent_position)
        if idx < len(rooms) - 1:
            agent_position = rooms[idx + 1]
            
    elif action=="Left":
        idx = rooms.index(agent_position)
        if idx > 0:
            agent_position = rooms[idx - 1]

plt.ioff()
print("Our agent has successfully managed cleanliness across all rooms")