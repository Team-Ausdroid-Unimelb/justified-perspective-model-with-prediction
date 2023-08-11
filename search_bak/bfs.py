import logging
import util


LOGGER_NAME = "search:bfs"
LOGGER_LEVEL = logging.DEBUG
# logger = logging.getLogger("bfsdc")
# logger.setLevel(logging.DEBUG)

# NOVELTY_KEY_WORD = "@"

class Search:
    def __init__(self,handler):
        self.logger = util.setup_logger(LOGGER_NAME,handler,LOGGER_LEVEL) 
        self.expanded = 0
        self.goal_checked = 0
        self.generated = 0
        self.pruned = 0
        self.visited = []
        self.short_visited = []
        self.result = dict()

    class SearchNode:
        state = None
        epistemic_item_set = set([])
        path = []

        def __init__(self,state,epistemic_item_set,path):
            self.state = state
            self.epistemic_item_set = epistemic_item_set
            self.path = path

    def searching(self,problem, filterActionNames = None):
        self.logger.info(f'starting searching using bfsdc')
        self.logger.info(f'the initial is {problem.initial_state}')
        self.logger.info(f'the variables are {problem.variables}')
        self.logger.info(f'the domains are {problem.domains}')
        
        # check whether the initial state is the goal state
        init_state = problem.initial_state
        init_path = [(problem.initial_state,'None')]
        init_epistemic_item_set = set([])
        init_node = self.SearchNode(init_state,init_epistemic_item_set,init_path)
        
        queue = [init_node]

        while len(queue):


            current_node = queue.pop(0)
            state = current_node.state
            epistemic_item_set = current_node.epistemic_item_set
            path = current_node.path
            self.goal_checked += 1

            # Goal Check
            is_goal, temp_epistemic_item_set = problem.isGoalN(state,path)
            if is_goal:
                # self.logger.info(path)
                actions = [ a  for s,a in path]
                actions = actions[1:]
                self.logger.info(f'plan is: {actions}')
                self.logger.info(f'Goal found')
                self.result.update({'solvable': True})
                self.result.update({'plan':actions})
                self._finalise_result(problem)
                return self.result

            # self.logger.debug("finding legal actions:")
            actions = problem.getAllActions(state,path)
            # self.logger.debug(actions)
            filtered_action_names = filterActionNames(problem,actions)
            # self.logger.debug(filtered_action_names)
            for action in filtered_action_names:
                pre_flag,temp_epistemic_item_set = problem.checkPreconditionsN(state,actions[action],path)
                if pre_flag: 
                    succ_state = problem.generateSuccessor(state, actions[action],path)
                    succ_node = self.SearchNode(succ_state,temp_epistemic_item_set,path + [(succ_state,action)])
                    self.generated += 1
                    queue.append(succ_node)

        self.logger.info(f'Problem is not solvable')
        self.result.update({'plan':[]})
        self.result.update({'solvable': False})
        self._finalise_result(problem)
        return self.result
    
    def _finalise_result(self,problem):
        # logger output
        self.logger.info(f'[number of node pruned]: {self.pruned}')
        self.logger.info(f'[number of node goal_checked]: {self.goal_checked}')
        self.logger.info(f'[number of node expansion]: {self.expanded}')
        self.logger.info(f'[number of node generated]: {self.generated}')
        self.logger.info(f'[number of epistemic formulas evaluation: {problem.epistemic_calls}]')
        self.logger.info(f'[time in epistemic formulas evaluation: {problem.epistemic_call_time}]')
        # file output
        self.result.update({'pruned':self.pruned})
        self.result.update({'goal_checked':self.goal_checked})
        self.result.update({'expanded':self.expanded})
        self.result.update({'generated':self.generated})
        self.result.update({'epistemic_calls':problem.epistemic_calls})
        self.result.update({'epistemic_call_time':problem.epistemic_call_time.total_seconds()})