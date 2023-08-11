import logging
import util


LOGGER_NAME = "search:wastar"
LOGGER_LEVEL = logging.INFO

W = 1.5
# LOGGER_LEVEL = logging.DEBUG
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
        
        
        self.logger.info(f'starting searching using heuristic_search')
        self.logger.info(f'the initial is {problem.initial_state}')
        self.logger.info(f'the variables are {problem.variables}')
        self.logger.info(f'the domains are {problem.domains}')
        
        # check whether the initial state is the goal state
        init_state = problem.initial_state
        init_path = [(problem.initial_state,'None')]
        init_epistemic_item_set = set([])
        
        init_node = Search.SearchNode(init_state,init_epistemic_item_set,init_path)

        
        open_list = util.PriorityQueue()
        p,es = _f(init_node,problem)
        init_node.epistemic_item_set.update(es)
        # remaining_g = p-_gn(init_node)
        open_list.push(item=init_node, priority=p)
        
        while not open_list.isEmpty():
            # logger.debug(f"queue length {len(queue)}")
            current_p , _, current_node = open_list.pop_full()
            self.logger.debug(f"current_p: {current_p}-{_gn(current_node)}, current_node {current_node}")

            state = current_node.state
            epistemic_item_set = current_node.epistemic_item_set
            path = current_node.path
            actions = [ a  for s,a in path]
            actions = actions[1:]
            self.logger.debug(f"action_lists: {actions}")
            # self.goal_checked += 1
            # if len(path) >3:
            #     return
            # Goal Check
            # is_goal, temp_epistemic_item_set = problem.isGoalN(state,path)
            # print(temp_epistemic_item_set)
            # print(problem.goal_states)
            remaining_g = current_p - _gn(current_node)
            
            # print(f"p:{current_p}, g:{ _gn(current_node)}, r:{remaining_g}")
            is_goal = remaining_g==0
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
            
            # check whether the node has been visited before
            # epistemic_item_set.update(epistemic_item_set)
            epistemic_item_set.update(state)
            # temp_str = state_to_string(temp_epistemic_item_set)
            if not epistemic_item_set in self.visited:
                self.logger.debug(epistemic_item_set)
            # if True:
                
                self.expanded +=1
                # print(expanded)
                # update the visited list
                # short_visited.append(temp_str)
                self.visited.append(epistemic_item_set)
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
                    # pre_flag,temp_epistemic_item_set = problem.checkPreconditionsN(state,actions[action],path)
                    pre_flag,p_dict,e_dict,pre_dict = problem.checkPreconditions(state,actions[action],path)
                    self.generated += 1
                    if pre_flag: 
                        succ_state = problem.generateSuccessor(state, actions[action],path)
                        succ_node = self.SearchNode(succ_state,pre_dict,path + [(succ_state,action)])
                        
                        self.goal_checked += 1
                        p,goal_dict = _f(succ_node,problem)
                        # es.update(succ_node.epistemic_item_set)
                        succ_node.epistemic_item_set.update(goal_dict)
                        self.logger.debug(f"succ_state = {succ_state}")
                        self.logger.debug(f"goal_dict = {goal_dict}")
                        
                        open_list.push(item=succ_node, priority=p)
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

def _f(node,problem):
    heuristic = goal_counting
    g = _gn(node)
    h,es = heuristic(node,problem)
    f = h*W + g
    # print(f"g: {g},h: {h},f: {f}")
    return f,es

def _gn(node):
    path = node.path
    return len(path)-1

# it is not admissible
def goal_counting(node,problem):
    remain_goal_number = 0
    goal_states = problem.goal_states
    ontic_goal_states = goal_states['ontic_g']
    epistemic_goal_states = goal_states['epistemic_g']
    state = node.state
    path = node.path
    
    is_goal,perspectives_dict,epistemic_dict,goal_dict = problem.isGoal(state,path)
    
    
    remain_goal_number = list(goal_dict.values()).count(False)
    # for goal,value in ontic_goal_states:
    #     if goal in state:
    #         if not state[goal] == value:
    #             remain_goal_number += 1
    #     else:
    #         remain_goal_number += 1    
    
    
    # for goal,value in epistemic_goal_states:
    #     if goal in epistemic_item_set:
    #         if not epistemic_item_set[goal] == value:
    #             remain_goal_number += 1
    #     else:
    #         remain_goal_number += 1
            
    # print(state)
    # print(goal_dict)
    # print(remain_goal_number)
    
    return remain_goal_number,goal_dict