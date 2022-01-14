import model

# all the direction that agent can go
domains = {
    'dir':{'basic_type': 'enumerate','values':['W','NW','N','NE','E','SE','S','SW']},
    'x':{'basic_type': 'integer','values':[0,4]},
    'y':{'basic_type': 'integer','values':[0,4]},
    # 'boolean':{'basic_type':model.D_TYPE.ENUMERATE,'values':[True,False]},
    'agent':{'basic_type':'','values':[]},
}



i_state = {
    'dir-a':'SW',
    'dir-b':'SW',
    'x-a': 3,
    'x-b': 2,
    'x-p': 1,
    'y-a': 3,
    'y-b': 2,
    'y-p': 1,
}

g_states = {
    'dir-b':'S',
}

agent_index = ['a','b']
obj_index = ['p']
variables = {'dir':['a','b'],'x':['a','b','p'],'y':['a','b','p']}

actions= {
    'turn_clockwise':{
        'parameters': [('?i','agent')],
        'precondition': [],
        'effect': [("dir?i","dir?i+1")]
    },
    'turn_counter_clockwise':{
        'parameters': [('?i','agent')],
        'precondition': [],
        'effect': [("dir?i","dir?i-1")]
    } ,
}










if __name__ == "__main__":
    problem = initialize_problem()
    i_state = problem.i_state
    
    # actions = problem.getLegalActions(i_state)
    # print(actions)
    
    # print(problem.generatorSuccessor(i_state,actions['turn_clockwise-a']))
    
    print(BFS(problem))
    

    