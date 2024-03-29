import logging

from util import setup_logger, PriorityQueue, PDDL_TERNARY
# import util


# LOGGER_NAME = "forward_search:bfsdc"
LOGGER_LEVEL = logging.INFO
# LOGGER_LEVEL = logging.DEBUG

SPLIT_KEY_WORD = "@"

class Search:
    def __init__(self,handlers,search_name):
        self.search_name = search_name      
        self.logger = setup_logger(search_name,handlers,logger_level=LOGGER_LEVEL) 
        self.expanded = 0
        self.goal_checked = 0
        self.generated = 0
        self.pruned = 0
        self.pruned_by_unknown = 0
        self.pruned_by_visited = 0
        self.visited = set()
        self.short_visited = []
        self.result = dict()
        self.branch_factors = []
        self.filtered_branching_factors = []
        self.p_path = {}
        self.heuristic = self.goal_counting
        self.h_weight = 1
        self.g_weight = 1
        self.max_goal_num = 0

    class SearchNode:
        state = None
        epistemic_item_set = set([])
        remaining_goal = 9999
        path = []

        def __init__(self,state,epistemic_item_set,path):
            self.state = state
            self.epistemic_item_set = epistemic_item_set
            self.path = path

    def _h(self,node,problem,p_path):
        h,es = self.heuristic(node,problem,p_path)
        return h,es
    
    def _f(self,h,g):
        f = g*self.g_weight+h*self.h_weight
        return f

    def _remaining_goal(self,h):
        self.goal_checked += 1
        return h
    # def _isGoal(self,current_p, current_node):
    #     return (current_p - self._gn(current_node)*1) == 0

    def _gn(self,node):
        path = node.path
        return len(path)-1
    
    def _duplication_check(self,ep_state_str):
        if not ep_state_str in self.visited:
            self.visited.add(ep_state_str)
            return True
        else:
            return False
        # return True

    def _unknown_check(self,succ_node):
        if succ_node.remaining_goal <= self.max_goal_num:
            return True
        else:
            return False

    #BFS with duplicate check on the state + epistemic formula
    # for novelty checking purpose, we need to move the goal check process at where the node is generated
    def searching(self,problem):
        self.logger.info("starting searching using [%s]",self.search_name)
        self.max_goal_num = len(problem.goals.ontic_dict)+len(problem.goals.epistemic_dict)
        
        # check whether the initial state is the goal state
        init_state = problem.initial_state
        init_path = [(problem.initial_state,'')]
        init_epistemic_item_set = dict()
        
        init_node = Search.SearchNode(init_state,init_epistemic_item_set,init_path)
        # self.group_eg_dict = self.group_epistemic_goals(problem)
        # self.landmarks_dict = problem.external.generate_constrain_dict(problem,self.group_eg_dict)

        open_list = PriorityQueue()
        h,es = self._h(init_node,problem,self.p_path)
        g = self._gn(init_node)
        fn = self._f(h,g)
        init_node.remaining_goal =  self._remaining_goal(h)
        init_node.epistemic_item_set.update(es)
        open_list.push(item=init_node, priority=fn)
        
        while not open_list.isEmpty():

            current_fn , _, current_node = open_list.pop_full()
            state = current_node.state
            ep_goal_dict = current_node.epistemic_item_set
            path = current_node.path
            actions = [ a  for s,a in path]
            actions = actions[1:]

            # if len(path) > 3:
            #     exit()
            self.logger.debug("path: %s",actions)

            is_goal = (0 == current_node.remaining_goal)
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
            
            
            all_actions = problem.getAllActions(state,path)
            self.logger.debug("finding all actions: [%s]" % (all_actions))
            
            # self.logger.debug(actions)
            filterAction = getattr(problem.external,'filterActionNames')

            if filterAction == None:
                filtered_action_names = list(all_actions.keys())
            else:
                filtered_action_names = filterAction(problem,all_actions)
                
            self.logger.debug("finding all actions: [%s]" % (list(filtered_action_names)))
            
            ontic_pre_dict = {}
            epistemic_pre_dict = {}
            for action_name in filtered_action_names:
                action = all_actions[action_name]
                ontic_pre_dict.update({action_name:action.a_preconditions.ontic_dict})
                epistemic_pre_dict.update({action_name:action.a_preconditions.epistemic_dict})
 
            flag_dict,e_pre_dict,pre_dict = problem.checkAllPreconditions(state,path, ontic_pre_dict,epistemic_pre_dict,self.p_path)



            # e_pre_dict.update(state)
            # e_pre_dict.update(ep_goal_dict)
            e_pre_dict.update(state)
            e_pre_dict.update(ep_goal_dict)
            e_pre_dict.update(pre_dict)
            
            self.logger.debug("flag_dict is [%s]",flag_dict)
            ep_state_str = state_to_string(e_pre_dict)
            if self._duplication_check(ep_state_str):
                self.logger.debug("path [%s] get in visited",actions)
                self.logger.info("ep_state_str is [%s]",ep_state_str)
                self.expanded +=1
                self.branch_factors.append(len(list(all_actions.keys())))
                self.filtered_branching_factors.append(list(flag_dict.values()).count(True))
                temp_successor = 0
                temp_actions = []
                
                for action_name in filtered_action_names:

                    if flag_dict[action_name]: 
                        action = all_actions[action_name]
                        self.logger.debug("action [%s] passed the precondition check", action_name)
                        # passed the precondition
                        succ_state = problem.generateSuccessor(state, action,path)
                        if not succ_state == None:
                            
                            succ_node = self.SearchNode(succ_state,{},path + [(succ_state,action_name)])

                            h,ep_dict = self._h(succ_node,problem,self.p_path)
                            self.logger.debug("heuristic is: %d" % (h))
                            g = self._gn(succ_node)
                            self.logger.debug("gn is: %d" % (g))
                            succ_node.remaining_goal =  self._remaining_goal(h)
                            self.logger.debug("remaining is: %d" % (succ_node.remaining_goal))
                            
                            if self._unknown_check(succ_node):
                                succ_node.epistemic_item_set = ep_dict
                                self.generated += 1
                                fn = self._f(h,g)
                                open_list.push(item=succ_node, priority=fn)
                                temp_successor +=1
                                temp_actions.append(action_name)
                            else:
                                self.pruned_by_unknown +=1


                    else:
                        self.logger.debug('action [%s] not generated in state [%s] due to not pass precondition',action_name,state)
                self.logger.debug('successor: [%s] with actions [%s]',temp_successor,temp_actions)
            else:
                self.pruned_by_visited += 1
                self.logger.debug("path [%s] already visited",actions)
                self.logger.debug("ep_state_str: [%s]",ep_state_str)
                self.logger.debug("visited: [%s]",self.visited)
            # self.logger.debug(open_list.count)
            
            
        self.logger.info(f'Problem is not solvable')
        self.result.update({'plan':[]})
        self.result.update({'solvable': False})
        
        self._finalise_result(problem)
        self.logger.debug(self.result)
        return self.result

    
    




    def _finalise_result(self,problem):
        # logger output


        self.logger.info(f'[number of node pruned_by_unknown]: {self.pruned_by_unknown}')
        self.logger.info(f'[number of node pruned_by_visited]: {self.pruned_by_visited}')
        self.pruned = self.pruned_by_unknown + self.pruned_by_visited
        self.logger.info(f'[number of node pruned]: {self.pruned}')

        self.logger.info(f'[number of node goal_checked]: {self.goal_checked}')
        self.logger.info(f'[number of node expansion]: {self.expanded}')
        self.logger.info(f'[number of node generated]: {self.generated}')
        self.logger.info(f'[number of epistemic formulas evaluation: {problem.epistemic_calls}]')
        self.logger.info(f'[time in epistemic formulas evaluation: {problem.epistemic_call_time}]')
        self.logger.info(f'[avg time in epistemic formulas evaluation: {problem.epistemic_call_time.total_seconds()/problem.epistemic_calls}]')
        self.logger.info(f'[goal_size: {len(list(problem.goals.epistemic_dict.keys()))}]')
        self.logger.info(f'[pddl_goals: {list(problem.goals.epistemic_dict.keys())}]')
        
        # file output
        self.result.update({'pruned':self.pruned})
        self.result.update({'pruned_by_unknown':self.pruned_by_unknown})
        self.result.update({'pruned_by_visited':self.pruned_by_visited})
        self.result.update({'goal_checked':self.goal_checked})
        self.result.update({'expanded':self.expanded})
        self.result.update({'generated':self.generated})
        self.result.update({'epistemic_calls':problem.epistemic_calls})
        self.result.update({'epistemic_call_time':problem.epistemic_call_time.total_seconds()})
        self.result.update({'epistemic_call_time_avg':problem.epistemic_call_time.total_seconds()/problem.epistemic_calls})
        
        self.result.update({'goal_size':len(list(problem.goals.epistemic_dict.keys()))})
        self.result.update({'pddl_goals':list(problem.goals.epistemic_dict.keys())})
        
        ## added for common perspective iterations
        common_iteration_list = problem.epistemic_model.common_iteration_list
        num_common_call = 0
        all_common_iteration = 0
        max_common_iteration = 0
        average_common_iteration = 0
        if not common_iteration_list == list():
            num_common_call = len(common_iteration_list)
            all_common_iteration = sum(common_iteration_list)
            max_common_iteration = max(common_iteration_list)
            average_common_iteration = all_common_iteration/(num_common_call*1.0)
        self.logger.info(f'[number of common perspective generated]: {num_common_call}')
        self.logger.info(f'[number of all iterations used when generating common perspectives]: {all_common_iteration}')
        self.logger.info(f'[number of max iterations used when generating common perspectives]: {max_common_iteration}')
        self.logger.info(f'[number of average iterations used when generating common perspectives]: {average_common_iteration}')
        self.result.update( {'common_calls':num_common_call})
        self.result.update( {'common_total':all_common_iteration})
        self.result.update( {'common_max':max_common_iteration})
        self.result.update( {'common_average':average_common_iteration})

        avg_branching_factors = 0
        max_branching_factors = 0
        avg_filtered_branching_factors = 0
        max_filtered_branching_factors = 0
        if not self.branch_factors == list():
            avg_branching_factors = sum(self.branch_factors)/len(self.branch_factors)
            max_branching_factors = max(self.branch_factors)
        if not self.filtered_branching_factors == list():
            avg_filtered_branching_factors = sum(self.filtered_branching_factors)/len(self.filtered_branching_factors)
            max_filtered_branching_factors = max(self.filtered_branching_factors)
        self.logger.info(f'[number of averaged unfiltered branching factors]: {avg_branching_factors}')
        self.logger.info(f'[number of max unfiltered branching factors]: {max_branching_factors}')
        self.logger.info(f'[number of average filtered branching factors]: {avg_filtered_branching_factors}')
        self.logger.info(f'[number of max filtered branching factors]: {max_filtered_branching_factors}')
        self.result.update({'avg_branching_factors': avg_branching_factors})
        self.result.update({'max_branching_factors': max_branching_factors})
        self.result.update({'avg_filtered_branching_factors': avg_filtered_branching_factors})
        self.result.update({'max_filtered_branching_factors': max_filtered_branching_factors})        



    def group_epistemic_goals(self,problem):
        group_eg_dict = {}
        for eq_str,value in problem.goals.epistemic_dict.items():
            var_str = eq_str.split(" ")[-1].split(",")[0][2:-1]
            if var_str in group_eg_dict:
                group_eg_dict[var_str].append((eq_str,value))
            else:
                group_eg_dict.update({var_str:[(eq_str,value)]})
        return group_eg_dict





    # it is not admissible
    def goal_counting(self,node,problem,p_path):
        remain_goal_number = 0
        state = node.state
        path = node.path
        
        is_goal,epistemic_dict,goal_dict = problem.isGoal(state,path,p_path)
        
        remain_goal_number = list(goal_dict.values()).count(False)

        # for key,value in goal_dict.items():
        #     if str(PDDL_TERNARY.UNKNOWN.value) in key and not value:
        #         self.logger.debug('Unknown been updated, goal is impossible')
        #         return 9999,epistemic_dict      
        # return remain_goal_number,epistemic_dict


        for key,value in goal_dict.items():
            
            # if str(PDDL_TERNARY.UNKNOWN.value) in key and not value:
            if key in problem.goals.epistemic_dict.keys() \
                and problem.goals.epistemic_dict[key].value == PDDL_TERNARY.UNKNOWN \
                    and not value:
                self.logger.debug('Unknown been updated, goal is impossible')
                self.logger.debug('goal is impossible')
                return 9999,epistemic_dict      
        return remain_goal_number,epistemic_dict
        heuristic_value = remain_goal_number
        
        # landmark_constrain = []
        temp_v_name_list = []
        for v_name, ep_goals in self.group_eg_dict.items():
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
        temp_landmark = set()
                
        for temp_v_name in temp_v_name_list:
            # flag = True
            for temp_state in self.landmarks_dict[temp_v_name]:
                if not str(sorted(temp_state)) in temp_landmark:
                    temp_flag = True
                    for key,value in temp_state.items():
                        if key in state.keys():
                            if not state[key]==value:
                                temp_flag = False
                                break
                    if temp_flag:
                        heuristic_value +=1
                        temp_landmark.add(str(sorted(temp_state)))
                        break
                
            # if flag:
            #     heuristic_value +=1
                
                
        
        
        # if 'secret-a' in temp_v_name_list:
        #     landmark_constrain.append(('agent_at-b','agent_at-d'))
        # elif 'secret-c' in temp_v_name_list:
        #     landmark_constrain.append(('agent_at-b','agent_at-d'))
        # if 'secret-b' in temp_v_name_list:
        #     landmark_constrain.append(('agent_at-c','agent_at-a'))
        # elif 'secret-d' in temp_v_name_list:
        #     landmark_constrain.append(('agent_at-c','agent_at-a'))
            
        # for v1,v2 in landmark_constrain:
        #     if state[v1] == state[v2]:
        #         heuristic_value +=1
        

        return heuristic_value,epistemic_dict



def state_to_string(dicts):
    output = []
    for key,value in dicts.items():
        output.append(f'{key}:{value}')
    output.sort() 
    return str(output)
