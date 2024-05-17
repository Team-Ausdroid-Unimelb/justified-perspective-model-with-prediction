import logging
import datetime
# import resource
import psutil
import os
from pddl_model import Problem

from util import setup_logger, PriorityQueue, GLOBAL_PERSPECTIVE_INDEX,make_hashable
from util import Entity,EntityType,Condition,ConditionType,EP_formula,Ternary,EPFType,Action
# import util


# LOGGER_NAME = "forward_search:bfsdc"
LOGGER_LEVEL = logging.INFO
# LOGGER_LEVEL = logging.DEBUG

SPLIT_KEY_WORD = "@"

class Search:
    def __init__(self,handlers,search_name,timeout):
        self.search_name = search_name      
        self.logger = setup_logger(search_name,handlers,logger_level=LOGGER_LEVEL) 
        self.expanded = 0
        self.goal_checked = 0
        self.generated = 1
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
        self.timeout = datetime.timedelta(seconds=timeout)
        self.memoryout = 10*1024
        self.unknown_goal_name = []
    # Do i need to reset here?

    class SearchNode:
        def __init__(self,state,remaining_goal_num,perspective_dict,path):
            self.state = state
            self.perspective_dict = perspective_dict
            self.remaining_goal = remaining_goal_num
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
    
    
    
    def _duplication_check(self,state,sgp_p_dict):
        
        # self.logger.debug(sgp_p_dict.keys())
        for k, item in sgp_p_dict.items():
            sgp_p_dict[k] = item[-1]
        
        sgp_p_dict.update({GLOBAL_PERSPECTIVE_INDEX:state})
        
        hsgp_p_dict = make_hashable(sgp_p_dict)
        if not hsgp_p_dict in self.visited:
            self.visited.add(hsgp_p_dict)
            return True
        # if not ep_state_str in self.visited:
        #     self.visited.add(ep_state_str)
        #     return True
        # else:
        #     return False
        # return True

    def _unknown_check(self,succ_node,goal_dict):
        
        for goal_name,goal_value in goal_dict.items():
            if goal_name in self.unknown_goal_name:
                if not goal_value:
                    return False
        return True
            

    def action_filter(self,problem,all_legal_action_name):
        return all_legal_action_name

    #BFS with duplicate check on the state + epistemic formula
    # for novelty checking purpose, we need to move the goal check process at where the node is generated
    def searching(self,problem:Problem):
        self.logger.info("starting searching using [%s]",self.search_name)
        start_time = datetime.datetime.now()

        self.max_goal_num = len(list(problem.goals.keys()))
        # intitalise unknown goal name
        for key,item in problem.goals.items():
            goal_condition: Condition = item
            if goal_condition.condition_type == ConditionType.EP:
                ep_formula: EP_formula = goal_condition.condition_formula
                if ep_formula.epf_type == EPFType.EP:
                    if goal_condition.target_value == Ternary.UNKNOWN:
                        self.unknown_goal_name.append(key)
                    elif "$" in ep_formula.ep_query:
                        self.unknown_goal_name.append(key)
        self.logger.debug(f'unknown goal name: {self.unknown_goal_name}')
                
        
        # check whether the initial state is the goal state
        init_state = problem.initial_state
        init_path = [(init_state,'')]
        remaining_goal_num,init_goal_dict,init_p_dict = problem.is_goal(init_path)
        self.goal_checked +=1
       
        # init_epistemic_item_set = dict()
        
        init_node = Search.SearchNode(init_state,remaining_goal_num,init_p_dict,init_path)
        # self.group_eg_dict = self.group_epistemic_goals(problem)
        # self.landmarks_dict = problem.external.generate_constrain_dict(problem,self.group_eg_dict)

        open_list = PriorityQueue()
        h = self._h(init_node,init_goal_dict,problem)
        g = self._gn(init_node)
        fn = self._f(h,g)
        open_list.push(item=init_node, priority=fn)
        
        
        while not open_list.isEmpty():

            _ , _, current_node = open_list.pop_full()
            state = current_node.state
            sg_p_dict = current_node.perspective_dict
            path = current_node.path
            actions = [ a  for s,a in path]
            actions = actions[1:]

            # if len(path) > 3:
            #     exit()
            self.logger.debug("path: %s",actions)

            goal_checking = (0 == current_node.remaining_goal)
            if goal_checking:
                # self.logger.info(path)
                actions = [ a  for s,a in path]
                actions = actions[1:]
                self.logger.info(f'plan is: {actions}')
                self.logger.info(f'Goal found')
                self.result.update({'solvable': True})
                self.result.update({'plan':actions})
                self.result.update({'path_length':len(actions)})
                self.result.update({'timeout':self.timeout.seconds})
                self.result.update({'memoryout':self.memoryout})
                self._finalise_result(problem)
                return self.result

            current_time = datetime.datetime.now()
            delta_time = current_time - start_time
            process = psutil.Process(os.getpid())

            # Get the memory usage (in bytes)
            memory_info = process.memory_info()
            current_memory_usage = memory_info.rss  # resident set size in bytes

            # Convert bytes to MB for easier interpretation
            usage = current_memory_usage / (1024 * 1024)

            if delta_time > self.timeout:
                actions = [ a  for s,a in path]
                actions = actions[1:]
                self.logger.info(f'Problem cannot be solved in the given time ({self.timeout.seconds}).')
                self.result.update({'plan':[]})
                self.result.update({'path_length':len(actions)})
                self.result.update({'solvable': False})
                self.result.update({'running': "TIMEOUT"})
                self.result.update({'timeout':self.timeout.seconds})
                self.result.update({'memoryout':self.memoryout})
                self._finalise_result(problem)
                return self.result
            elif usage > self.memoryout:
                actions = [ a  for s,a in path]
                actions = actions[1:]
                self.logger.info(f'Problem cannot be solved in the given memory ({self.memoryout}MB).')
                self.result.update({'plan':[]})
                self.result.update({'path_length':len(actions)})
                self.result.update({'solvable': False})
                self.result.update({'running': "MEMORYOUT"})
                self.result.update({'timeout':self.timeout.seconds})
                self.result.update({'memoryout':self.memoryout})
                self._finalise_result(problem)
                return self.result

            all_legal_actions,sgp_p_dict = problem.get_all_legal_actions(state,path,sg_p_dict)
            all_legal_action_name = list(all_legal_actions.keys())
            filtered_action_name = self.action_filter(problem,all_legal_action_name)
            
            self.logger.debug(sgp_p_dict.keys())
            self.logger.debug(sgp_p_dict)
            self.logger.debug("action generated: %s",all_legal_actions.keys())
            
            if self._duplication_check(state,sgp_p_dict):
                # self.logger.debug("path [%s] get in visited",actions)
                # self.logger.debug("ep_state_str is [%s]",ep_state_str)
                self.expanded +=1
                self.branch_factors.append(len(list(all_legal_actions.keys())))
                temp_successor = 0
                temp_actions = []
                for action_name in filtered_action_name:
                    action :Action = all_legal_actions[action_name]
                # for action_name,action in all_legal_actions.items():
                    self.logger.debug("action [%s] passed the precondition check", action_name)
                    # passed the precondition
                    succ_state = problem.generate_successor(state, action,path)
                    if not succ_state == None:
                        
                        new_path = path + [(succ_state,action_name)]
                        remaining_goal_num,goal_dict,g_p_dict = problem.is_goal(new_path)
                        self.goal_checked+=1
                        succ_node = self.SearchNode(succ_state,remaining_goal_num,g_p_dict,new_path)

                        if self._unknown_check(succ_node,goal_dict):
                            self.generated += 1
                            h = self._h(succ_node,goal_dict,problem)
                            g = self._gn(succ_node)
                            fn = self._f(h,g)
                            

                            self.logger.debug("heuristic is: %d" % (h))
                            g = self._gn(succ_node)
                            self.logger.debug("gn is: %d" % (g))
                            self.logger.debug("remaining is: %d" % (succ_node.remaining_goal))
                            
                            open_list.push(item=succ_node, priority=fn)
                            temp_successor +=1
                            temp_actions.append(action_name)
                        else:
                            self.pruned_by_unknown +=1
                            
                    else:
                        self.logger.debug("successor node been pruned due to exceeds the function range",action_name)
                self.logger.debug('successor: [%s] with actions [%s]',temp_successor,temp_actions)
            else:
                self.pruned_by_visited += 1
                # print(self.pruned_by_visited)
                self.logger.debug("path [%s] already visited",actions)
            # self.logger.debug(open_list.count)
            
        self.logger.info(f'Problem is not solvable')
        self.result.update({'plan':[]})
        self.result.update({'path_length':0})
        self.result.update({'solvable': False})
        self.result.update({'timeout':self.timeout.seconds})
        self.result.update({'memoryout':self.memoryout})
        self._finalise_result(problem)
        self.logger.debug(self.result)
        return self.result

    
    




    def _finalise_result(self,problem:Problem):
        # logger output
        ontic_goal_list = list()
        epistemic_goal_list = list()
        for key,item in problem.goals.items():
            condition : Condition = item
            if condition.condition_type == ConditionType.ONTIC:
                ontic_goal_list.append(key)
            elif condition.condition_type == ConditionType.EP:
                epistemic_goal_list.append(key)
            else:
                raise ValueError("Unknown condition type")
        self.pruned = self.pruned_by_unknown + self.pruned_by_visited
        
        
        self.logger.info(f'[number of node pruned_by_unknown]: {self.pruned_by_unknown}')
        self.logger.info(f'[number of node pruned_by_visited]: {self.pruned_by_visited}')
        self.logger.info(f'[number of node pruned]: {self.pruned}')
        self.logger.info(f'[number of node goal_checked]: {self.goal_checked}')
        self.logger.info(f'[number of node expansion]: {self.expanded}')
        self.logger.info(f'[number of node generated]: {self.generated}')
        self.logger.info(f'[number of epistemic formulas evaluation: {problem.epistemic_calls}]')
        self.logger.info(f'[time in epistemic formulas evaluation: {problem.epistemic_call_time}]')
        self.logger.info(f'[avg time in epistemic formulas evaluation: {0 if problem.epistemic_calls == 0 else problem.epistemic_call_time.total_seconds()*1000/problem.epistemic_calls}]')
        self.logger.info(f'[total_goal_size: {len(ontic_goal_list)+len(epistemic_goal_list)}]')
        self.logger.info(f'[ontic_goal_size: {len(ontic_goal_list)}]')
        self.logger.info(f'[epistemic_goal_size: {len(epistemic_goal_list)}]')
        self.logger.info(f'[ontic_goals: {ontic_goal_list}]')
        self.logger.info(f'[epistemic_goals: {epistemic_goal_list}]')
        self.logger.info(f'[goals: {ontic_goal_list+epistemic_goal_list}]')
        self.logger.info(f'[epistemic_call_time_max: {problem.epistemic_call_time_max.total_seconds()*1000}]')
        self.logger.info(f'[functions: {len(list(problem.functions.keys()))}]')
        # file output
        self.result.update({'pruned':self.pruned})
        self.result.update({'pruned_by_unknown':self.pruned_by_unknown})
        self.result.update({'pruned_by_visited':self.pruned_by_visited})
        self.result.update({'goal_checked':self.goal_checked})
        self.result.update({'expanded':self.expanded})
        self.result.update({'generated':self.generated})
        self.result.update({'epistemic_calls':problem.epistemic_calls})
        self.result.update({'epistemic_call_time':problem.epistemic_call_time.total_seconds()})
        self.result.update({'epistemic_call_time_avg':0 if problem.epistemic_calls == 0 else problem.epistemic_call_time.total_seconds()*1000/problem.epistemic_calls})
        self.result.update({'epistemic_call_time_max':problem.epistemic_call_time_max.total_seconds()*1000})
        self.result.update({'epistemic_call_length':problem.epistemic_call_length})
        self.result.update({'epistemic_call_length_avg':0 if problem.epistemic_calls == 0 else problem.epistemic_call_length/problem.epistemic_calls})
        self.result.update({'epistemic_call_length_max':problem.epistemic_call_length_max})
        self.result.update({'total_goal_size':len(ontic_goal_list)+len(epistemic_goal_list)})
        self.result.update({'ontic_goal_size':len(ontic_goal_list)})
        self.result.update({'epistemic_goal_size':len(epistemic_goal_list)})
        self.result.update({'ontic_goals:':ontic_goal_list})
        self.result.update({'epistemic_goals':epistemic_goal_list})
        self.result.update({'goals':ontic_goal_list+epistemic_goal_list})
        self.result.update({'functions':len(list(problem.functions.keys()))})
        self.result.update({'domain_path':problem.domain_path})
        self.result.update({'problem_path':problem.problem_path})

        max_depth = 0

        goal_agents = set()
        
        for epistemic_condition_name in epistemic_goal_list:
            epistemic_condition: Condition = problem.goals[epistemic_condition_name]
            ep_formula: EP_formula = epistemic_condition.condition_formula
            temp_depth = ep_formula.ep_query.count('[')
            if temp_depth > max_depth:
                max_depth = temp_depth
            query_prefix_list = ep_formula.ep_query.split(' ')
            for temp_str in query_prefix_list:
                if '[' in temp_str:
                    temp_agent_str = temp_str[1:-1]
                    temp_agent_list = temp_agent_str.split(',')
                    for agent_id in temp_agent_list:
                        goal_agents.add(agent_id)
        # for key,item in problem.goals.epistemic_dict.items():
        #     temp_depth = key.count('[')
        #     if temp_depth > max_depth:
        #         max_depth = temp_depth
        #     if item.query_prefix[0] == "$":
        #         num_of_unknown_goals +=1
        #     query_prefix_list = item.query_prefix.split(' ')
        #     for temp_str in query_prefix_list:
        #         if '[' in temp_str:
        #             temp_agent_str = temp_str[1:-1]
        #             temp_agent_list = temp_agent_str.split(',')
        #             for agent_id in temp_agent_list:
        #                 goal_agents.add(agent_id)
        num_of_unknown_goals = len(self.unknown_goal_name)
        self.result.update({'max_goal_depth':max_depth})
        self.result.update({'num_of_unknown_goals':num_of_unknown_goals})
        self.result.update({'num_of_goal_agents':len(goal_agents)})
        self.result.update({'goal_agents':list(goal_agents)})

        agents= set()
        for k,item in problem.entities.items():
            entity : Entity = item
            if entity.enetity_type == EntityType.AGENT:
                agents.add(k)
        self.result.update({'agents':list(agents)})
        self.result.update({'num_of_agents':len(agents)})
        
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
        # self.logger.info(f'[number of average filtered branching factors]: {avg_filtered_branching_factors}')
        # self.logger.info(f'[number of max filtered branching factors]: {max_filtered_branching_factors}')
        self.result.update({'avg_branching_factors': avg_branching_factors})
        self.result.update({'max_branching_factors': max_branching_factors})
        # self.result.update({'avg_filtered_branching_factors': avg_filtered_branching_factors})
        # self.result.update({'max_filtered_branching_factors': max_filtered_branching_factors})        



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
    def goal_counting(self,node,goal_dict,problem):

        remain_goal_number = list(goal_dict.values()).count(False)




        # for key,value in goal_dict.items():

                
        #     if key in problem.goals.epistemic_dict.keys() \
        #         and problem.goals.epistemic_dict[key].query_prefix[0] == "$" \
        #             and not value:
        #         self.logger.debug('Unknown been updated, goal is impossible')
        #         self.logger.debug('goal is impossible')
        #         return 9999
        return remain_goal_number
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
