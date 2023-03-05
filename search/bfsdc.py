import logging

logger = logging.getLogger("bfsdc")
logger.setLevel(logging.DEBUG)

# NOVELTY_KEY_WORD = "@"

class SearchNode:
    state = None
    epistemic_item_set = set([])
    path = []

    def __init__(self,state,epistemic_item_set,path):
        self.state = state
        self.epistemic_item_set = epistemic_item_set
        self.path = path



#BFS with duplicate check on the state + epistemic formula
# for novelty checking purpose, we need to move the goal check process at where the node is generated
def searching(problem, filterActionNames = None):
    
    
    logger.info(f'starting searching using bfsdc')
    logger.info(f'the initial is {problem.initial_state}')
    logger.info(f'the variables are {problem.variables}')
    logger.info(f'the domains are {problem.domains}')
    
    result = dict()
    
    # Your code here:
    expanded = 0
    goal_checked = 0
    generated = 0
    pruned = 0
    visited = []
    short_visited = []

    
    # check whether the initial state is the goal state
    init_state = problem.initial_state
    init_path = [(problem.initial_state,'None')]
    init_epistemic_item_set = set([])
    init_node = SearchNode(init_state,init_epistemic_item_set,init_path)

    queue = [init_node]
    
    while len(queue):
        # logger.debug(f"queue length {len(queue)}")
        current_node = queue.pop(0)
        state = current_node.state
        epistemic_item_set = current_node.epistemic_item_set
        path = current_node.path
        goal_checked += 1
        
        # Goal Check
        is_goal, temp_epistemic_item_set = problem.isGoalN(state,path)
        if is_goal:
            logger.info(f'Goal found')
            logger.info(path)
            actions = [ a  for s,a in path]
            actions = actions[1:]
            logger.info(f'plan is: {actions}')
            logger.info(f'[number of node pruned]: {pruned}')
            logger.info(f'[number of node goal_checked]: {goal_checked}')
            logger.info(f'[number of node expansion]: {expanded}')
            logger.info(f'[number of node generated]: {generated}')
            logger.info(f'[number of epistemic formula evaluation: {problem.epistemic_calls}]')
            logger.info(f'[time in epistemic formulas evaluation: {problem.epistemic_call_time}]')
            
            result.update({'plan':actions})
            result.update({'solvable': True})
            result.update({'pruned':pruned})
            result.update({'goal_checked':goal_checked})
            result.update({'expanded':expanded})
            result.update({'generated':generated})
            result.update({'epistemic_calls':problem.epistemic_calls})
            result.update({'epistemic_call_time':problem.epistemic_call_time.total_seconds()})
            
            
            return result
        
        # check whether the node has been visited before
        temp_epistemic_item_set.update(epistemic_item_set)
        temp_epistemic_item_set.update(state)
        # temp_str = state_to_string(temp_epistemic_item_set)
        if not temp_epistemic_item_set in visited:
            
            expanded +=1
            # print(expanded)
            # update the visited list
            # short_visited.append(temp_str)
            visited.append(temp_epistemic_item_set)
            # logger.debug(f"visited: {short_visited}")
            # logger.debug(f"short visited: {short_visited}")
            # logger.debug(f"{temp_epistemic_item_set}")
            # logger.debug(f"{state_to_string(temp_epistemic_item_set)}")
            
            # logger.debug("finding legal actions:")
            actions = problem.getLegalActions(state,path)
            # logger.debug(actions)
            filtered_action_names = filterActionNames(problem,actions)
            # logger.debug(filtered_action_names)
            for action in filtered_action_names:
                pre_flag,temp_epistemic_item_set = problem.checkPreconditionsN(state,actions[action],path)
                if pre_flag: 
                    succ_state = problem.generatorSuccessor(state, actions[action],path)
                    generated += 1
                    succ_node = SearchNode(succ_state,temp_epistemic_item_set,path + [(succ_state,action)])
                    queue.append(succ_node)
        else:
            pruned += 1
        
        
    logger.info(f'Problem is not solvable')
    logger.info(f'[number of node pruned]: {pruned}')
    logger.info(f'[number of node goal_checked]: {goal_checked}')
    logger.info(f'[number of node expansion]: {expanded}')
    logger.info(f'[number of node generated]: {generated}')
    logger.info(f'[number of epistemic formulas evaluation: {problem.epistemic_calls}]')
    logger.info(f'[time in epistemic formulas evaluation: {problem.epistemic_call_time}]')
    
    result.update({'plan':[]})
    result.update({'solvable': False})
    result.update({'pruned':pruned})
    result.update({'goal_checked':goal_checked})
    result.update({'expanded':expanded})
    result.update({'generated':generated})
    result.update({'epistemic_calls':problem.epistemic_calls})
    result.update({'epistemic_call_time':problem.epistemic_call_time.total_seconds()})
    
    return result


def state_to_string(dicts):
    output = ""
    for value in dicts.values():
        output += str(value)
    return output

