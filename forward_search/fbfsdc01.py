import logging

from util import setup_logger, PriorityQueue, PDDL_TERNARY
# import util
import re

LOGGER_NAME = "forward_search:bfsdc"
LOGGER_LEVEL = logging.INFO
LOGGER_LEVEL = logging.DEBUG

SPLIT_KEY_WORD = "@"

class Search:
    def __init__(self,handlers,external):        
        self.logger = setup_logger(LOGGER_NAME,handlers,logger_level=LOGGER_LEVEL) 
        self.expanded = 0
        self.goal_checked = 0
        self.generated = 0
        self.pruned = 0
        self.pruned_by_unknown = 0
        self.pruned_by_visited = 0
        self.visited = []
        self.short_visited = []
        self.result = dict()
        self.branch_factors = []
        self.p_path = {}
        self.external = external


    class SearchNode:
        state = {}
        epistemic_item_set = set([])
        remaining_goal = 9999
        path = []

        def __init__(self,state,epistemic_item_set,path):
            self.state = state
            self.epistemic_item_set = epistemic_item_set
            self.path = path



    
        


    #BFS with duplicate check on the state + epistemic formula
    # for novelty checking purpose, we need to move the goal check process at where the node is generated
    def searching(self,problem, filterActionNames = None):

        self.logger.info("starting searching using %s",LOGGER_NAME)
        max_goal_num = len(problem.goals.ontic_dict)+len(problem.goals.epistemic_dict)

        # check whether the initial state is the goal state
        init_state = problem.initial_state
        init_rule = problem.globle_rule
        init_path = [(problem.initial_state,'',init_rule)]#####################################################################
        init_epistemic_item_set = dict()
        
        init_node = Search.SearchNode(init_state,init_epistemic_item_set,init_path)

        
        
        
        open_list = PriorityQueue()
        p,es = self._f(init_node,problem,self.p_path)
        init_node.remaining_goal =  p-self._gn(init_node)
        init_node.epistemic_item_set.update(es)
        # remaining_g = p-_gn(init_node)
        open_list.push(item=init_node, priority=self._gn(init_node))
        
        
        while not open_list.isEmpty():

            current_p , _, current_node = open_list.pop_full()
            
            state = current_node.state
            ep_goal_dict = current_node.epistemic_item_set
            path = current_node.path
            actions = [ a  for s,a,r in path]
            actions = actions[1:]

            

            # if len(path) > 5:
            #     exit()
            self.logger.debug("path: %s",actions)


            is_goal = (0 == current_node.remaining_goal)
            if is_goal:
                # self.logger.info(path)
                actions = [ a  for s,a,r in path]
                actions = actions[1:]
                self.logger.info(f'plan is: {actions}')
                self.logger.info(f'Goal found')
                self.result.update({'solvable': True})
                self.result.update({'plan':actions})
                self._finalise_result(problem)
                return self.result
            
            all_actions = problem.getAllActions(state,path)
            # self.logger.debug(actions)
            filtered_action_names = filterActionNames(problem,all_actions)
            
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
            # assert(len(path) <=2)
            ep_state_str = state_to_string(e_pre_dict)
            if not ep_state_str in self.visited:
                # self.logger.debug(epistemic_item_set)
            # if True:
                # self.branch_factors.append(flag_dict.values().count(True))
                self.logger.debug("path [%s] get in visited",actions)
                self.logger.debug("ep_state_str is [%s]",ep_state_str)
                self.expanded +=1
                temp_successor = 0
                temp_actions = []
                # update the visited list
                # self.short_visited.append(temp_str)
                self.visited.append(ep_state_str)

                
                # self.logger.debug("finding legal actions:")


                
                for action_name in filtered_action_names:

                    self.logger.debug(action_name)

                    if flag_dict[action_name]: 
                        action = all_actions[action_name]
                        self.logger.debug("action [%s] passed the precondition check", action_name)
                        # passed the precondition
                        succ_state = problem.generateSuccessor(state, action,path)


                        ##################################挪进problem.generateSuccessor
                        #succ_state = self.external.update_state(succ_state, path, problem)
                        #print(succ_state)
                        ##########################
                        
                        # self.visited.append(e_dict)
                        self.goal_checked += 1
                        if succ_state is not None:
                            succ_node = self.SearchNode(succ_state,{},path + [(succ_state,action_name,init_rule)])###############################
                        

                            p,ep_dict = self._f(succ_node,problem,self.p_path)
                            
                            succ_node.remaining_goal = p - self._gn(succ_node)
                            # print(max_goal_num)
                            # print(succ_node.remaining_goal)
                            if succ_node.remaining_goal <= max_goal_num:
                                succ_node.epistemic_item_set = ep_dict
                                self.generated += 1
                                open_list.push(item=succ_node, priority=self._gn(succ_node))
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
        
        # file output
        self.result.update({'pruned':self.pruned})
        self.result.update({'pruned_by_unknown':self.pruned_by_unknown})
        self.result.update({'pruned_by_visited':self.pruned_by_visited})
        self.result.update({'goal_checked':self.goal_checked})
        self.result.update({'expanded':self.expanded})
        self.result.update({'generated':self.generated})
        self.result.update({'epistemic_calls':problem.epistemic_calls})
        self.result.update({'epistemic_call_time':problem.epistemic_call_time.total_seconds()})
        
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

    def group_epistemic_goals(self,problem):
        group_eg_dict = {}
        for eq_str,value in problem.goals.epistemic_dict.items():
            var_str = eq_str.split(" ")[-1].split(",")[0][2:-1]
            if var_str in group_eg_dict:
                group_eg_dict[var_str].append((eq_str,value))
            else:
                group_eg_dict.update({var_str:[(eq_str,value)]})
        return group_eg_dict



    def _f(self,node,problem,p_path):
        heuristic = self.goal_counting
        g = self._gn(node)
        h,es = heuristic(node,problem,p_path)
        f = g*1+h*1
        return f,es

    def _isGoal(self,current_p, current_node):
        return (current_p - self._gn(current_node)*1) == 0

    def _gn(self,node):
        path = node.path
        return len(path)-1

    # it is not admissible
    def goal_counting(self,node,problem,p_path):
        remain_goal_number = 0
        state = node.state
        path = node.path
        
        is_goal,epistemic_dict,goal_dict = problem.isGoal(state,path,p_path)
        
        remain_goal_number = list(goal_dict.values()).count(False)
        # print(goal_dict)
        
        for key,value in goal_dict.items():
            #if str(PDDL_TERNARY.UNKNOWN.value) == problem.goals.epistemic_dict[key].value and not value:
            if key in problem.goals.epistemic_dict and str(PDDL_TERNARY.UNKNOWN.value) == problem.goals.epistemic_dict[key].value and not value:
                self.logger.debug('Unknown been updated, goal is impossible')
                return 9999,epistemic_dict      
        return remain_goal_number,epistemic_dict



def state_to_string(dicts):
    output = []
    for key,value in dicts.items():
        output.append(f'{key}:{value}')
    output.sort() 
    return str(output)
