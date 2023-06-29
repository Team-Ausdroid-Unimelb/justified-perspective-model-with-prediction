import logging
import util


LOGGER_NAME = "search:heuristic_search"
LOGGER_LEVEL = logging.INFO
LOGGER_LEVEL = logging.DEBUG
# logger = logging.getLogger("bfsdc")
# logger.setLevel(logging.DEBUG)

SPLIT_KEY_WORD = "@"

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
        group_eg_dict = group_epistemic_goals(problem)
        
        constrain_dict = problem.external.generate_constrain_dict(problem,group_eg_dict)
        print(constrain_dict)
        # print(group_eg_dict)
        # return
        
        
        
        open_list = util.PriorityQueue()
        p,es = _f(init_node,problem,group_eg_dict)
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
            # remaining_g = current_p - _gn(current_node)
            # print(f"p:{current_p}, g:{ _gn(current_node)}, r:{remaining_g}")
            is_goal = _isGoal(current_p,current_node)
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
                for action_name in filtered_action_names:
                    action = actions[action_name]
                    # pre_flag,temp_epistemic_item_set = problem.checkPreconditionsN(state,actions[action],path)
                    pre_flag,p_dict,e_dict,pre_dict = problem.checkPreconditions(state,action,path)
                    if pre_flag: 
                        succ_state = problem.generateSuccessor(state, action,path)
                        succ_node = self.SearchNode(succ_state,pre_dict,path + [(succ_state,action_name)])
                        self.generated += 1
                        self.goal_checked += 1
                        p,goal_dict = _f(succ_node,problem,group_eg_dict)
                        # es.update(succ_node.epistemic_item_set)
                        succ_node.epistemic_item_set.update(goal_dict)
                        self.logger.debug(f"action = {action_name}")
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

def group_epistemic_goals(problem):
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



def _f(node,problem,group_eg_dict):
    heuristic = goal_counting
    g = _gn(node)
    h,es = heuristic(node,problem,group_eg_dict)
    f = g*10+h*11
    # print(f)
    return f,es

def _isGoal(current_p, current_node):
    return (current_p - _gn(current_node)*10) == 0

def _gn(node):
    path = node.path
    return len(path)-1

# it is not admissible
def goal_counting(node,problem,group_eg_dict):
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
    # return remain_goal_number,goal_dict
    
    # for goal,value in epistemic_goal_states:
    #     if goal in epistemic_item_set:
    #         if not epistemic_item_set[goal] == value:
    #             remain_goal_number += 1
    #     else:
    #         remain_goal_number += 1
    for key,value in goal_dict.items():
        if "-1" in key and not value:
            return 9999,goal_dict       
    # print(state)
    # print(epistemic_item_set)
    # print(remain_goal_number)
    # {'secret-b': [("b [a] ('secret-b','t')", 1), ("b [d] b [a] ('secret-b','f')", 1)], 
    #  'secret-c': [("b [b] ('secret-c','t')", 1), ("b [c] b [b] ('secret-c','f')", 1)], 
    #  'secret-d': [("b [c] ('secret-d','t')", 1), ("b [b] b [c] ('secret-d','f')", 1)], 
    #  'secret-a': [("b [d] ('secret-a','t')", 1), ("b [a] b [d] ('secret-a','f')", 1)]}
    # print(goal_dict)
    # {"b [a] ('secret-b','t') 1": False, 
    #  "b [b] ('secret-c','t') 1": False, 
    #  "b [c] ('secret-d','t') 1": False, 
    #  "b [d] ('secret-a','t') 1": False, 
    #  "b [d] b [a] ('secret-b','f') 1": False, 
    #  "b [c] b [b] ('secret-c','f') 1": False, 
    #  "b [b] b [c] ('secret-d','f') 1": False, 
    #  "b [a] b [d] ('secret-a','f') 1": False}
    # exit()
    heuristic_value = remain_goal_number
    
    landmark_constrain = []
    temp_v_name_list = []
    for v_name, ep_goals in group_eg_dict.items():
        for ep_str,value in ep_goals:
            if not goal_dict[f"{ep_str} {value}"]:
                temp_v_name_list.append(v_name)
                # heuristic_value +=1
                break
    
    # for v_name in temp_v_name_list:
    #     temp_pair_dict = {}
    #     for ep_str,value in group_eg_dict[v_name]:
    #         ep_value = ep_str.split(v_name)[1][3:-2]
    #         ep_front = ep_str.split(v_name)[0]
    #         ep_header = format_ep(ep_value,value)
            
            
            
            
    
    
    # if 'secret-a' in temp_v_name_list:
    #     landmark_constrain.append(('agent_at-b','agent_at-d'))
    # elif 'secret-c' in temp_v_name_list:
    #     landmark_constrain.append(('agent_at-b','agent_at-d'))
    # if 'secret-b' in temp_v_name_list:
    #     landmark_constrain.append(('agent_at-c','agent_at-a'))
    # elif 'secret-d' in temp_v_name_list:
    #     landmark_constrain.append(('agent_at-c','agent_at-a'))
        
    for v1,v2 in landmark_constrain:
        if state[v1] == state[v2]:
            heuristic_value +=1
    
    # print(f' h is: {heuristic_value}, gc is: {remain_goal_number}')
    if remain_goal_number == 0:
        print(f' h is: {heuristic_value}, gc is: {remain_goal_number}')
        
    
    return heuristic_value,goal_dict



