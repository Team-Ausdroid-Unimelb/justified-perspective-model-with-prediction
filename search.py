import logging

def BFS(problem):
    # Your code here:
    start_node = (problem.initial_state, [])
    logging.debug(start_node)
    queue = [start_node]

    while len(queue):
        current_node = queue.pop(0)
        state, path = current_node

        # Goal Check
        if problem.isGoal(state):
            print("Goal")
            return path

        # Add successor nodes into queue (no loop check; randomly tie-break)
        logging.debug("finding legal actions:")
        actions = problem.getLegalActions(state)
        logging.debug(actions)
        for action in actions.keys():
            succ_state = problem.generatorSuccessor(state, actions[action],path)
            print(f"prestate: {state};\n action: {action};\n state: {succ_state}\n\n")
            queue.append((succ_state, path + [(action,state)]))

    return False