import logging
import util


LOGGER_NAME = "search:bfsdcp"
LOGGER_LEVEL = logging.DEBUG
LOGGER_LEVEL = logging.INFO
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



    #BFS with duplicate check on the state + epistemic formula
    # for novelty checking purpose, we need to move the goal check process at where the node is generated
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
            # logger.debug(f"queue length {len(queue)}")
            current_node = queue.pop(0)
            state = current_node.state
            p_dict = current_node.epistemic_item_set
            path = current_node.path
            self.goal_checked += 1
            
            # Goal Check
            is_goal,perspectives_dict,epistemic_dict,goal_dict = problem.isGoal(state,path)
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
            
            perspectives_dict.update(p_dict)
            
            # self.logger.debug(p_dict)
            # self.logger.debug(self.visited)
            # check whether the node has been visited before
            # temp_epistemic_item_set.update(epistemic_item_set)
            # temp_epistemic_item_set.update(state)
            # temp_str = state_to_string(temp_epistemic_item_set)
            if not perspectives_dict in self.visited:
                
                self.expanded +=1
                # print(expanded)
                # update the visited list
                # short_visited.append(temp_str)
                self.visited.append(perspectives_dict)
                # self.logger.debug(f"visited: {short_visited}")
                # self.logger.debug(f"short visited: {short_visited}")
                # self.logger.debug(f"{temp_epistemic_item_set}")
                # self.logger.debug(f"{state_to_string(temp_epistemic_item_set)}")
                
                # self.logger.debug("finding legal actions:")
                actions = problem.getAllActions(state,path)
                # self.logger.debug(actions)
                filtered_action_names = filterActionNames(problem,actions)
                # self.logger.debug(filtered_action_names)
                for action in filtered_action_names:
                    pre_flag,perspectives_dict,epistemic_dict,pre_dict = problem.checkPreconditions(state,actions[action],path)
                    if pre_flag: 
                        succ_state = problem.generateSuccessor(state, actions[action],path)
                        succ_node = self.SearchNode(succ_state,perspectives_dict,path + [(succ_state,action)])
                        self.generated += 1
                        queue.append(succ_node)
            else:
                self.pruned += 1
            
            
        self.logger.info(f'Problem is not solvable')
        self.result.update({'plan':[]})
        self.result.update({'solvable': False})
        self._finalise_result(problem)
        return self.result


    def state_to_string(dicts):
        output = ""
        for value in dicts.values():
            output += str(value)
        return output

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
