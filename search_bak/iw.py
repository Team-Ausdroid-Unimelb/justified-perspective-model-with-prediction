import logging
import util

LOGGER_NAME = "search:iw"
LOGGER_LEVEL = logging.DEBUG

NOVELTY_KEY_WORD = "@"

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
        
        self.logger.info(f'starting searching using iw')
        self.logger.info(f'the initial is {problem.initial_state}')
        self.logger.info(f'the variables are {problem.variables}')
        self.logger.info(f'the domains are {problem.domains}')
        
        # Your code here:
        init_state = problem.initial_state
        init_path = [(problem.initial_state,'None')]
        init_epistemic_item_set = set([])
        init_node = self.SearchNode(init_state,init_epistemic_item_set,init_path)


        novelty = 1
        max_novelty = self._max_novelty(problem)
        self.logger.info(f'max novelty is {max_novelty}')
        
        while novelty <= max_novelty:
            queue = [init_node]
            self.logger.info(f'start to solve with novelty {novelty}')
            
            novelty_table = set([])
            self.logger.info(f'novelty table is {novelty_table}')
            
            while len(queue):
                current_node = queue.pop(0)
                state = current_node.state
                epistemic_item_set = current_node.epistemic_item_set
                path = current_node.path
                self.goal_checked += 1
                
                novelty_flag = False

                is_goal, epistemic_item_set = problem.isGoalN(state,path)
                if is_goal:
                    self.logger.info(f'Goal found')
                    self.logger.info(path)
                    actions = [ a  for s,a in path]
                    actions = actions[1:]
                    self.logger.info(f'plan is: {actions}')
                    self.result.update({'plan':actions})
                    self.result.update({'solvable': True})
                    self._finalise_result(problem)
                    
                    return self.result
                
                # check novelty
                epistemic_item_set.update(state)
                self.logger.debug(f'checking for goal')
                if self.novelty_check(novelty_table,epistemic_item_set,novelty):
                    novelty_flag = True
                
                # Add successor nodes into queue (no loop check; randomly tie-break)
                self.expanded += 1
                self.logger.debug("finding legal actions:")
                actions = problem.getAllActions(state,path)
                self.logger.debug(actions)
                filtered_action_names = filterActionNames(problem,actions)
                for action in filtered_action_names:
                    pre_flag,epistemic_item_set = problem.checkPreconditionsN(state,actions[action],path)
                    if pre_flag: 
                        self.generated += 1
                        succ_state = problem.generateSuccessor(state, actions[action],path)
                        epistemic_item_set.update(state)
                        self.logger.debug(f'checking for precondition of {action}')
                        if self.novelty_check(novelty_table,epistemic_item_set,novelty):
                            novelty_flag = True
                        # if str(succ_state) not in visited:
                        self.generated += 1
                        if novelty_flag:
                            succ_state = problem.generateSuccessor(state, actions[action],path)
                            succ_node = self.SearchNode(succ_state,set([]),path + [(succ_state,action)])
                            queue.append(succ_node)
                        else:
                            self.logger.debug("node pruned due to failed novelty check")
                            self.pruned +=1
            self.logger.info(f'Problem is not solvable with novelty {novelty}')
            
            novelty +=1
            
            
        self.logger.info(f'Problem is not solvable')        
        self.result.update({'plan':[]})
        self.result.update({'solvable': False})
        self._finalise_result(problem)
        return self.result

    def novelty_check(self,novelty_table = {}, state = {},novelty_bound=1):
        self.logger.debug(f'before novelty check: {novelty_table}')
        self.logger.debug(f'checking {state}')
        novelty_flag = False
        temp_novelty_list = []
        for temp_bound in range(novelty_bound+1):
            temp_novelty_list += self._create_checklist(state,temp_bound)
        
        # print(temp_novelty_list)
        temp_novel_set = set(temp_novelty_list)
        # print(temp_novel_set)
        for item in temp_novel_set:
            if item not in novelty_table:
                novelty_table.update(temp_novel_set)
                novelty_flag = True 
        # self.logger.debug(f'prune this node because: \n{temp_novelty_list}\n{novelty_table}\n')   
        self.logger.debug(f'after novelty check: {novelty_table}') 
        return novelty_flag



    def _create_checklist(self,state = {},novelty_bound=1):
        # logger.debug(f'state: {state}')
        # logger.debug(f'novelty_bound: {novelty_bound}')
        novel_item = []

        if novelty_bound == 0:
            return []
        else:
            
            for key,value in state.items():
                
                rest = self._create_checklist(state=state, novelty_bound=novelty_bound-1)
                if rest == []: 
                    novel_item = novel_item + [f"|{Search._toNoveltyItem(key,value)}"]
                else:
                    novel_item = novel_item + [ f"|{Search._toNoveltyItem(key,value)}{t}" for t in rest ]
        return novel_item

    def _max_novelty(self,problem):
        variable_list = problem.variables
        novelty = 1
        for value,item in variable_list.items():
            values = problem.domains[item.v_domain_name].d_values
            novelty *= len(values)
        return novelty

    def _toNoveltyItem(key,value):
        return f'{key}{NOVELTY_KEY_WORD}{value}'


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






if __name__ == '__main__':
    novelty_table_temp = set(['|a', '|b'])
    print(novelty_check(novelty_table = novelty_table_temp, state = {'a','b'},novelty_bound=2))
    print(novelty_table_temp)