import logging

logger = logging.getLogger("bfs")

#BFS

def searching(problem, filterActionNames = None):
    # Your code here:
    start_node = (problem.initial_state, [(problem.initial_state,'None')])
    logger.debug(start_node)
    queue = [start_node]
    result = dict()
    
    # Your code here:
    expanded = 0
    goal_checked = 0
    generated = 0
    pruned = 0

    while len(queue):
        current_node = queue.pop(0)
        state, path = current_node
        if len(path) == 8: 
            return "cannot find solution"
        
        goal_checked += 1
        logger.debug(f'expanding state ({expanded}th): {state}')
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

        # Add successor nodes into queue (no loop check; randomly tie-break)
        expanded += 1
        logger.debug("finding legal actions:")
        actions = problem.getLegalActions(state,path)
        logger.debug(actions)
        filtered_action_names = filterActionNames(problem,actions)
        for action in filtered_action_names:
            succ_state = problem.generatorSuccessor(state, actions[action],path)
            # if str(succ_state) not in visited:
            generated += 1
            queue.append((succ_state, path + [(succ_state,action)]))

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