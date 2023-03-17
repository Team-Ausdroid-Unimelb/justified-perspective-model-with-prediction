import logging

logger = logging.getLogger("iw")

NOVELTY_KEY_WORD = "@"


#IW
def searching(problem, filterActionNames = None):
    
    
    logger.info(f'starting searching using iw')
    logger.info(f'the initial is {problem.initial_state}')
    logger.info(f'the variables are {problem.variables}')
    logger.info(f'the domains are {problem.domains}')
    
    
    result = dict()
    # Your code here:
    
    
    start_node = (problem.initial_state, [(problem.initial_state,'None')])
    logger.debug(start_node)
    
    expanded = 0
    generated = 0
    pruned = 0
    goal_checked = 0
    
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
            
            novelty_flag = False
            # logger.debug(f'novelty table is {novelty_table}')
            # if novelty_check(novelty_table,state,novelty):

            
            # logger.debug(f'expanding state ({expanded}th): {state}')
            # logger.info(f'expanding {expanded}')
            
            # visited[str(state)]=1
            # Goal Check
            goal_checked += 1
            is_goal, epistemic_item_set = problem.isGoalN(state,path)
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
            
            # check novelty
            epistemic_item_set.update(state)
            logger.debug(f'checking for goal')
            if novelty_check(novelty_table,epistemic_item_set,novelty):
                novelty_flag = True
            
            # Add successor nodes into queue (no loop check; randomly tie-break)
            expanded += 1
            logger.debug("finding legal actions:")
            actions = problem.getLegalActions(state,path)
            logger.debug(actions)
            filtered_action_names = filterActionNames(problem,actions)
            for action in filtered_action_names:
                pre_flag,epistemic_item_set = problem.checkPreconditionsN(state,actions[action],path)
                if pre_flag: 
                    succ_state = problem.generateSuccessor(state, actions[action],path)
                    epistemic_item_set.update(state)
                    logger.debug(f'checking for precondition of {action}')
                    if novelty_check(novelty_table,epistemic_item_set,novelty):
                        novelty_flag = True
                    # if str(succ_state) not in visited:
                    generated += 1
                    if novelty_flag:
                        queue.append((succ_state, path + [(succ_state,action)]))
                    else:
                        logger.debug("node pruned due to failed novelty check")
                        pruned +=1
        logger.info(f'Problem is not solvable with novelty {novelty}')
        
        novelty +=1
        
        
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

def novelty_check(novelty_table = {}, state = {},novelty_bound=1):
    logger.debug(f'before novelty check: {novelty_table}')
    logger.debug(f'checking {state}')
    novelty_flag = False
    temp_novelty_list = []
    for temp_bound in range(novelty_bound+1):
        temp_novelty_list += _create_checklist(state,temp_bound)
    
    # print(temp_novelty_list)
    temp_novel_set = set(temp_novelty_list)
    # print(temp_novel_set)
    for item in temp_novel_set:
        if item not in novelty_table:
            novelty_table.update(temp_novel_set)
            novelty_flag = True 
    # logger.debug(f'prune this node because: \n{temp_novelty_list}\n{novelty_table}\n')   
    logger.debug(f'after novelty check: {novelty_table}') 
    return novelty_flag



def _create_checklist(state = {},novelty_bound=1):
    # logger.debug(f'state: {state}')
    # logger.debug(f'novelty_bound: {novelty_bound}')
    novel_item = []

    if novelty_bound == 0:
        return []
    else:
        
        for key,value in state.items():
            
            rest = _create_checklist(state=state, novelty_bound=novelty_bound-1)
            if rest == []: 
                novel_item = novel_item + [f"|{_toNoveltyItem(key,value)}"]
            else:
                novel_item = novel_item + [ f"|{_toNoveltyItem(key,value)}{t}" for t in rest ]
    return novel_item

def _max_novelty(problem):
    variable_list = problem.variables
    novelty = 1
    for value,item in variable_list.items():
        values = problem.domains[item.v_domain_name].d_values
        novelty *= len(values)
    return novelty

def _toNoveltyItem(key,value):
    return f'{key}{NOVELTY_KEY_WORD}{value}'


if __name__ == '__main__':
    novelty_table_temp = set(['|a', '|b'])
    print(novelty_check(novelty_table = novelty_table_temp, state = {'a','b'},novelty_bound=2))
    print(novelty_table_temp)