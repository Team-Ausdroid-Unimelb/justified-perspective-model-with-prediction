import logging
import util


LOGGER_NAME = "search:seq_bfsdc"
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

    #BFS with duplicate check on the state + epistemic formula
    # for novelty checking purpose, we need to move the goal check process at where the node is generated
    def searching(self,problem, filterActionNames = None):
        
        self.logger.info(f'starting searching using SEQ_bfsdc')
        self.logger.info(f'the initial is {problem.initial_state}')
        self.logger.info(f'the variables are {problem.variables}')
        self.logger.info(f'the domains are {problem.domains}')
        
        init_state = problem.initial_state
        init_path = [(problem.initial_state,'None')]
        init_epistemic_item_set = set([])
        
        group_eq_dict = self.group_epistemic_goals(problem)

        
        while not group_eq_dict == {}:
            item = group_eq_dict.popitem()
            problem.goal_states.update({"epistemic_g":item[1]})
            self.logger.info("solving subgoal ")
            
            init_node = self.SearchNode(init_state,init_epistemic_item_set,init_path)
            
            queue = [init_node]
            self.visited = []
            partial_goal_found = False
            

            while len(queue):
                # logger.debug(f"queue length {len(queue)}")
                current_node = queue.pop(0)
                state = current_node.state
                epistemic_item_set = current_node.epistemic_item_set
                path = current_node.path
                self.goal_checked += 1
                
                # Goal Check
                is_goal,perspectives_dict,epistemic_dict,goal_dict = problem.isGoal(state,path)
                if is_goal:
                    # self.logger.info(path)
                    # actions = [ a  for s,a in path]
                    # actions = actions[1:]
                    # self.logger.info(f'plan is: {actions}')
                    # self.logger.info(f'Goal found')
                    # self.result.update({'solvable': True})
                    # self.result.update({'plan':actions})
                    # self._finalise_result(problem)
                    init_path = path
                    init_state = state
                    init_epistemic_item_set = epistemic_item_set
                    partial_goal_found = True
                    break
                    # return self.result
                
                # check whether the node has been visited before
                goal_dict.update(epistemic_item_set)
                goal_dict.update(state)
                # temp_str = state_to_string(temp_epistemic_item_set)
                if not goal_dict in self.visited:
                    
                    self.expanded +=1
                    self.visited.append(goal_dict)

                    
                    # self.logger.debug("finding legal actions:")
                    actions = problem.getAllActions(state,path)
                    # self.logger.debug(actions)
                    filtered_action_names = filterActionNames(problem,actions)
                    # self.logger.debug(filtered_action_names)
                    for action in filtered_action_names:
                        pre_flag,perspectives_dict,epistemic_dict,pre_dict = problem.checkPreconditions(state,actions[action],path)
                        if pre_flag: 
                            succ_state = problem.generateSuccessor(state, actions[action],path)
                            succ_node = self.SearchNode(succ_state,pre_dict,path + [(succ_state,action)])
                            self.generated += 1
                            queue.append(succ_node)
                else:
                    self.pruned += 1
            

            if not partial_goal_found:
        
                self.logger.info(f'Problem is not solvable')
                self.logger.info(f'No plan found when solving partial ep_goals {problem.goal_states}')
                self.result.update({'plan':[]})
                self.result.update({'solvable': False})
                self._finalise_result(problem)
                return self.result
        actions = [ a  for s,a in path]
        actions = actions[1:]
        self.logger.info(f'plan is: {actions}')
        self.logger.info(f'Goal found')
        self.result.update({'solvable': True})
        self.result.update({'plan':actions})
        self._finalise_result(problem)
        return self.result

    def group_epistemic_goals(self,problem):
        # print(problem.goal_states["epistemic_g"])
        group_eg_dict = {}
        for eq_str,value in problem.goal_states["epistemic_g"]:
            var_str = eq_str.split(" ")[-1].split(",")[0][2:-1]
            if var_str in group_eg_dict:
                group_eg_dict[var_str].append((eq_str,value))
            else:
                group_eg_dict.update({var_str:[(eq_str,value)]})
            # print(var_str)
        # print(group_eg_dict)
        return group_eg_dict
        

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
