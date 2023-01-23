import logging

logger = logging.getLogger("iw")



#IW
def searching(problem, filterActionNames = None):
    
    
    logger.info(f'starting searching using iw')
    logger.info(f'the initial is {problem.initial_state}')
    logger.info(f'the variables are {problem.variables}')
    logger.info(f'the domains are {problem.domains}')
    
    
    
    # Your code here:
    
    
    start_node = (problem.initial_state, [(problem.initial_state,'None')])
    logger.debug(start_node)
    
    expanded = 0
    generated = 0
    pruned = 0
    novelty = 1
    # visited = {}
    max_novelty = _max_novelty(problem)
    logger.info(f'max novelty is {max_novelty}')
    
    while novelty <= max_novelty:
        queue = [start_node]
        
        
        
        logger.info(f'start to solve with novelty {novelty}')
        
        novelty_table = set([])
        logger.info(f'novelty table is {novelty_table}')
        
        while len(queue):
            current_node = queue.pop(0)
            state, path = current_node
            # if len(path) == 8: 
            #     return "cannot find solution"
            expanded += 1
            logger.info(f'novelty table is {novelty_table}')
            if novelty_check(novelty_table,state,novelty):
            
                # logger.debug(f'expanding state ({expanded}th): {state}')
                # logger.info(f'expanding {expanded}')
                
                # visited[str(state)]=1
                # Goal Check
                if problem.isGoal(state,path):
                    logger.info(f'Goal found')
                    logger.info(path)
                    actions = [ a  for s,a in path]
                    actions = actions[1:]
                    logger.info(f'plan is: {actions}')
                    logger.info(f'[number of node pruned]: {pruned}')
                    logger.info(f'[number of node expansion]: {expanded}')
                    logger.info(f'[number of node generated]: {generated}')
                    logger.info(f'[number of epistemic formula evaluation: {problem.epistemic_calls}]')
                    logger.info(f'[time in epistemic formulas evaluation: {problem.epistemic_call_time}]')
                    return actions

                # Add successor nodes into queue (no loop check; randomly tie-break)
                logger.debug("finding legal actions:")
                actions = problem.getLegalActions(state,path)
                logger.debug(actions)
                filtered_action_names = filterActionNames(problem,actions)
                for action in filtered_action_names:
                    succ_state = problem.generatorSuccessor(state, actions[action],path)
                    # if str(succ_state) not in visited:
                    generated += 1
                    queue.append((succ_state, path + [(succ_state,action)]))
            else:
                pruned +=1
        logger.info(f'Problem is not solvable with novelty {novelty}')
        
        novelty +=1
        
        
    logger.info(f'Problem is not solvable')
    logger.info(f'[number of node pruned]: {pruned}')
    logger.info(f'[number of node expansion]: {expanded}')
    logger.info(f'[number of node generated]: {generated}')
    logger.info(f'[number of epistemic formulas evaluation: {problem.epistemic_calls}]')
    logger.info(f'[time in epistemic formulas evaluation: {problem.epistemic_call_time}]')
    return False

def novelty_check(novelty_table = {}, state = {},novelty_bound=1):
    temp_novelty_list = []
    for temp_bound in range(novelty_bound+1):
        temp_novelty_list += _create_checklist(state,temp_bound)
    
    # print(temp_novelty_list)
    temp_novel_set = set(temp_novelty_list)
    # print(temp_novel_set)
    for item in temp_novel_set:
        if item not in novelty_table:
            novelty_table.update(temp_novel_set)
            return True 
    logger.debug(f'prune this node because: \n{temp_novelty_list}\n{novelty_table}\n')    
    return False

def _create_checklist(state = {},novelty_bound=1):
    logger.info(f'state: {state}')
    logger.info(f'novelty_bound: {novelty_bound}')
    novel_item = []

    if novelty_bound == 0:
        return []
    else:
        
        for key,value in state.items():
            
            rest = _create_checklist(state=state, novelty_bound=novelty_bound-1)
            if rest == []: 
                novel_item = novel_item + [f"|{key,value}"]
            else:
                novel_item = novel_item + [ f"|{key,value}{t}" for t in rest ]
    return novel_item

def _max_novelty(problem):
    variable_list = problem.variables
    novelty = 1
    for value,item in variable_list.items():
        values = problem.domains[item.v_domain_name].d_values
        novelty *= len(values)
    return novelty

if __name__ == '__main__':
    novelty_table_temp = set(['|a', '|b'])
    print(novelty_check(novelty_table = novelty_table_temp, state = {'a','b'},novelty_bound=2))
    print(novelty_table_temp)