import model

# all the direction that agent can go
domains = {
    'dir':{'basic_type': model.D_TYPE.ENUMERATE,'values':['W','NW','N','NE','E','SE','S','SW']},
    'x':{'basic_type': model.D_TYPE.INTEGER,'values':[0,4]},
    'y':{'basic_type': model.D_TYPE.INTEGER,'values':[0,4]},
    # 'boolean':{'basic_type':model.D_TYPE.ENUMERATE,'values':[True,False]},
    'agent':{'basic_type':'','values':[]},
}



initial_state = {
    'dir-a':'SW',
    'dir-b':'SW',
    'x-a': 3,
    'x-b': 2,
    'x-p': 1,
    'y-a': 3,
    'y-b': 2,
    'y-p': 1,
}

goal_states = {
    'dir-b':'S',
}

agent_index = ['a','b']
obj_index = ['p']
variables = {'dir':['a','b'],'x':['a','b','c'],'y':['a','b','c']}

actions= {
    'turn_clockwise':{
        'parameters': [('?i',model.E_TYPE.AGENT)],
        'precondition': [],
        'effects': [("dir?i","dir?i+1")]
    },
    'turn_counter_clockwise':{
        'parameters': [('?i',model.E_TYPE.AGENT)],
        'precondition': [],
        'effects': [("dir?i","dir?i-1")]
    } ,
}



def initialize_problem():
    
    entity_list = {}
    for i in agent_index:
        e_temp = model.Entity(i,model.E_TYPE.AGENT)
        entity_list.update({i:e_temp})
    for i in obj_index:
        e_temp = model.Entity(i,model.E_TYPE.OBJECT)
        entity_list.update({i:e_temp})        
    # print(entity_list)
    
    variable_list = {}
    for v_name,targets in variables.items():
        for i in targets:
            v_temp = model.Variable(f"{v_name}-{i}",v_name,i)
            variable_list.update({f"{v_name}-{i}":v_temp})
    # print(variable_list)
        
    # grounding all actions or do not ground any actions?    
    action_list = {}
    for a_name, parts in actions.items():
        a_temp = model.Action(a_name, parts['parameters'], parts['precondition'], parts['effects'])
        action_list.update({a_name:a_temp})
        
    
    domain_list = {}
    for d_name in domains.keys():
        # print(d_name)
        domain_temp = model.Domain(d_name,domains[d_name]['values'],d_name=='agent',domains[d_name]['basic_type'])
        domain_list.update({d_name:domain_temp})
    # print(domain_list)

    
        
    problem = model.Problem(entity_list,variable_list,action_list,domain_list,initial_state,goal_states)
    return problem
    # return


def BFS(problem):
    # Your code here:
    start_node = (problem.initial_state, [])
    queue = [start_node]

    while len(queue):
        current_node = queue.pop(0)
        state, path = current_node

        # Goal Check
        if problem.isGoal(state):
            print("GOal")
            return path

        # Add successor nodes into queue (no loop check; randomly tie-break)
        actions = problem.getLegalActions(state)
        for action in actions.keys():
            succ_state = problem.generatorSuccessor(state, actions[action])
            print(f"prestate: {state};\n action: {action};\n state: {succ_state}\n\n")
            queue.append((succ_state, path + [action]))

    return False


if __name__ == "__main__":
    problem = initialize_problem()
    initial_state = problem.initial_state
    
    # actions = problem.getLegalActions(initial_state)
    # print(actions)
    
    # print(problem.generatorSuccessor(initial_state,actions['turn_clockwise-a']))
    
    print(BFS(problem))
    

    