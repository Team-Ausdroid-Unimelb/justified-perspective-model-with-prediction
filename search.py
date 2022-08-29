import logging

logger = logging.getLogger("search")

def BFS(problem):
    # Your code here:
    start_node = (problem.initial_state, [(problem.initial_state,'None')])
    logger.debug(start_node)
    queue = [start_node]
    # visited = {}

    while len(queue):
        current_node = queue.pop(0)
        state, path = current_node
        if len(path) == 22: return "cannot find solution"
        logger.debug(f'expanding state: {state}')
        # visited[str(state)]=1
        # Goal Check
        if problem.isGoal(state,path):
            logger.info(f'Goal found')
            logger.info(path)
            actions = [ a  for s,a in path]
            actions = actions[1:]
            logger.info(f'plan is: {actions}')
            return actions

        # Add successor nodes into queue (no loop check; randomly tie-break)
        logger.debug("finding legal actions:")
        actions = problem.getLegalActions(state)
        logger.debug(actions)
        for action in actions.keys():
            succ_state = problem.generatorSuccessor(state, actions[action],path)
            # if str(succ_state) not in visited:
            queue.append((succ_state, path + [(succ_state,action)]))

    return False