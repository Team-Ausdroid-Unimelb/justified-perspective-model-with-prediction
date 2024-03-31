import enum
# import pddl_model
import typing
import re
import logging
import copy
from util import PDDL_TERNARY,EP_VALUE
from util import EpistemicQuery,EQ_TYPE,Q_TYPE
from predictor import Predictor

LOGGER_NAME = "forward_epistemic_model"
LOGGER_LEVEL = logging.INFO
# LOGGER_LEVEL = logging.DEBUG
from util import setup_logger
from util import ActionList2DictKey,GLOBAL_PERSPECTIVE_INDEX, ROOT_NODE_ACTION
from util import raiseNotDefined,eval_var_from_str,Queue
PRE_INIT_PDICT_KEY = ActionList2DictKey([])


class EpistemicModel:
    logger = None
    external = None
    common_iteration_list = list()
    entities = {}
    variables = {}
    domains = None

    
    
    def __init__(self, handlers, entities, variables, external,domains):
        self.logger = setup_logger(LOGGER_NAME,handlers,logger_level=LOGGER_LEVEL) 
        self.entities = entities
        self.variables = variables
        self.external = external
        self.goal_p_keys = None
        self.pre_p_keys = None
        self.all_p_keys = list()
        self.domains = domains
        self.predictor = Predictor()


    def epistemicGoalsHandler(self,epistemic_goals_dict, prefix, path, p_path):

        self.logger.debug('')
        self.logger.debug('epistemicGoalHandler')
        self.logger.debug('prefix: [%s]',prefix)
        
        action_list = [a for s,a,r in path]
        state_list = [s for s,a,r in path]
        rule_list = [r for s,a,r in path]
        dict1 = {}
        self.logger.debug(action_list)
        old_actions_str = ActionList2DictKey(action_list=action_list[:-1])
        actions_str = ActionList2DictKey(action_list=action_list)
        # if "-,,move_right-b,sharing-a,move_right-c" in actions_str:
        #     self.logger.setLevel(logging.DEBUG)
            
        self.logger.debug("actions_str [%s], old_actions_str [%s]",actions_str,old_actions_str)
        
        result_dict = dict()

        for key, item in epistemic_goals_dict.items():
            eq_str = item.query
            self.logger.debug(eq_str)
            # eq = self.partially_converting_to_eq(eq_str)
            
            

            output = self.eval_eq_in_ps(eq_str,prefix, GLOBAL_PERSPECTIVE_INDEX, old_actions_str, actions_str, state_list,rule_list, p_path,dict1,seeing_flag=False)
            result_dict[key] = output

        # self.logger.setLevel(logging.INFO)
                
        return result_dict
    
    def eval_eq_in_pss(self,eq_str,prefix, parent_prefix, actions_str_old, actions_str_new, p_list,rule_list, p_path,seeing_flag=False):
        eq = self.partially_converting_to_eq(eq_str)
        value_list = []
        dict1 = {}
        n = 1

        for p in p_list:
            #print(dict1)
            value = self.eval_eq_in_ps(eq_str,prefix, parent_prefix, actions_str_old, actions_str_new, p,rule_list, p_path,dict1,seeing_flag)
            self.logger.debug("PSS: eq str: [%s] is [%s]",eq,value)
            value_list.append(value)
            
        if eq.q_type == Q_TYPE.MUTUAL or eq.q_type == Q_TYPE.COMMON:
            int_list = [v.value for v in value_list]
            minimum = min(int_list)
            self.logger.debug(" the value list is: [%s] with values [%s] and min value is [%s]",value_list,int_list,minimum)
            return min(value_list)
        elif eq.q_type == Q_TYPE.DISTRIBUTION:
            return max(value_list)
        else:
            raiseNotDefined()
    
    def eval_eq_in_ps(self,eq_str,prefix, parent_prefix, actions_str_old, actions_str_new, p,rule_list, p_path,rule_dict,seeing_flag=False):
        eq = self.partially_converting_to_eq(eq_str)
        self.logger.debug("input perspectives: [%s]",p)
        self.logger.debug("last state: [%s]",p[-1])

        if type(eq) == str:
            # for knowledge and belief
            
            result = eval_var_from_str(self.logger,eq,p[-1])
            self.logger.debug("eq str: [%s] is [%s]",eq,result)
            return result
        else:
            seeing_flag = True if eq.eq_type == EQ_TYPE.SEEING else False
            if len(eq.q_group) >1:
                
                new_ps = list()
                if eq.q_type == Q_TYPE.COMMON:
                    new_ps = [p]
                    common_counter = 0
                    temp_ps = None
                    while not new_ps == temp_ps:
                        common_counter +=1
                        for_p = new_ps.copy()
                        temp_ps = new_ps.copy()
                        new_ps = list()
                        # added = set()
                        for temp_p in for_p:
                            for agt_id in eq.q_group:
                                new_prefix = prefix + eq.header_str + " " + EpistemicQuery.agtList2Str([agt_id]) + " "
                                self.logger.debug("input perspective: [%s]",temp_p)
                                new_temp_p = self.get1ps(agt_id,temp_p, new_prefix, actions_str_old, actions_str_new, rule_list, p_path)
                                self.logger.debug("[%s]'s perspective: [%s]",agt_id,new_temp_p)
                                new_t_p_str = str(new_temp_p)
                                if not new_temp_p in new_ps:
                                # if new_t_p_str not in added:
                                    # added.add(new_t_p_str)
                                    new_ps.append(new_temp_p)
                        self.logger.debug("all perspective: [%s]",new_ps)
                    self.common_iteration_list.append(common_counter)
                elif eq.q_type == Q_TYPE.DISTRIBUTION:
                    temp_ps = list()
                    for agt_id in eq.q_group:
                        new_prefix = prefix + eq.header_str + " " + EpistemicQuery.agtList2Str([agt_id]) + " "
                        new_temp_p = self.get1ps(agt_id,p, new_prefix, actions_str_old, actions_str_new,rule_list,  p_path)
                        temp_ps.append(new_temp_p)
                        
                    # generate all possible values

                    
                    temp_v_dict_list = [dict() for i in range(len(temp_ps[0]))]
                    for temp_p in temp_ps:
                        for i in range(len(temp_p)):
                            for k,v in temp_p[i].items():
                                if k not in temp_v_dict_list[i].keys():
                                    temp_v_dict_list[i][k] = set()
                                temp_v_dict_list[i][k].add(v)
                    self.logger.debug("all values [%s]",temp_v_dict_list)
                    
                    # remove None here
                    for i in range(len(temp_v_dict_list)):
                        for k,v in temp_v_dict_list[i].items():
                            if not v == {None}:
                                temp_set = set()
                                for item in v:
                                    if not item == None:
                                        temp_set.add(item)
                                temp_v_dict_list[i][k] = temp_set
                    self.logger.debug("updated all values [%s]",temp_v_dict_list)
                    
                    
                    
                    state_space_list = list()
                    for i in  range(len(temp_v_dict_list)):
                        v_dict=temp_v_dict_list[i]
                        state_space_list.append([])
                        empty_state = {}
                        myQ = Queue()
                        myQ.push(empty_state)
                        while not myQ.isEmpty():
                            temp_dict = myQ.pop()
                            flag = True
                            for k,v_set in v_dict.items():
                                if k not in temp_dict.keys():
                                    flag = False
                                    for v in v_set:
                                        new_temp_dict = temp_dict.copy()
                                        new_temp_dict[k] = v
                                        myQ.push(new_temp_dict)
                                    break
                            if flag:
                                state_space_list[i].append(temp_dict)
                            
                            
                        self.logger.debug("The number states is [%s] for timestamp [%s]",len(state_space_list[i]),i)
                        self.logger.debug("state space is [%s]",state_space_list[i])
                        
                    self.logger.debug("all state space is [%s]",state_space_list)
                    
                    for temp_p in temp_ps:
                        empty_sequence = []
                        myQ = Queue()
                        myQ.push(empty_sequence)
                        while not myQ.isEmpty():
                            temp_sequence = myQ.pop()
                            current_index = len(temp_sequence)
                            if not len(temp_sequence) == len(state_space_list):
                                exist_state = temp_p[current_index]
                                for matching_state in state_space_list[current_index]:
                                    self.logger.debug("matching_state [%s]",matching_state)
                                    self.logger.debug("exist_state [%s]",exist_state)
                                    flag = True
                                    for k,v in matching_state.items():
                                        if k in exist_state.keys():
                                            if not exist_state[k] == None and not exist_state[k] == matching_state[k] :
                                                flag = False
                                                continue
                                    if flag:
                                        new_sequence = temp_sequence + [matching_state]
                                        myQ.push(new_sequence)
                            else:
                                if not temp_sequence in new_ps:
                                    
                                    new_ps.append(temp_sequence)                                            
                else:
                    for agt_id in eq.q_group:
                        new_prefix = prefix + eq.header_str + " " + EpistemicQuery.agtList2Str([agt_id]) + " "
                        new_temp_p = self.get1ps(agt_id,p, new_prefix, actions_str_old, actions_str_new, p_path)
                        new_ps.append(new_temp_p)

                result_list = []
                
                
                self.logger.debug("[%s] generated ps: [%s]",eq_str,new_ps)
                for p in new_ps:
                    
                    value = self.eval_eq_in_ps(eq.q_content,prefix, parent_prefix, actions_str_old, actions_str_new, p, rule_list,p_path,rule_dict,seeing_flag)
                    self.logger.debug("PSS: eq str: [%s] is [%s]",eq,value)
                    result_list.append(value)
                    
                if eq.q_type == Q_TYPE.MUTUAL or eq.q_type == Q_TYPE.COMMON:
                    int_list = [v.value for v in result_list]
                    minimum = min(result_list)
                    self.logger.debug(" the value list is: [%s] with values [%s] and min value is [%s]",result_list,int_list,minimum)
                    return min(result_list)
                elif eq.q_type == Q_TYPE.DISTRIBUTION:
                    return max(result_list)
                else:
                    raiseNotDefined()
                # new_eq_str = EpistemicQuery.partial_eq2str(eq.q_type,eq.eq_type,eq.q_group) + eq.q_content
                
                # return self.eval_eq_in_pss(new_eq_str,new_prefix, prefix, actions_str_old, actions_str_new, new_ps, p_path,seeing_flag)
            
            
            elif len(eq.q_group) == 1:
                new_prefix = prefix + eq.header_str + " " + EpistemicQuery.agtList2Str(eq.q_group) + " "
                self.logger.debug("input perspective: [%s]",p)
                
                if not actions_str_new in p_path.keys():
                    p_path[actions_str_new] = dict()
                if not prefix in p_path[actions_str_new].keys():
                    p_path[actions_str_new][prefix] = dict()

                parent_ps = p
                agt_id = eq.q_group[0]

                new_os = [self.get1o(temp_p, agt_id) for temp_p in p]
                p_path[actions_str_new][prefix]['observation'] = new_os 

                domains = self.domains
                #print(domains)##############################################################
                print("##########")
                print("agt_id",agt_id)
                new_rs = self.predictor.getrs(new_os,p,domains)
                new_ps = self.predictor.getps(new_os,new_rs, p)

                p_path[actions_str_new][prefix]['rule'] = new_rs
                p_path[actions_str_new][prefix]['perspectives'] = new_ps
                rule_list = new_rs  ##?update value of rule_list


                #self.logger.debug("[%s]'s perspective: [%s]",eq.q_group[0],new_p)


                return self.eval_eq_in_ps(eq.q_content,new_prefix,prefix, actions_str_old, actions_str_new, new_ps,rule_list, p_path,rule_dict,seeing_flag)
            else:
                self.logger.error("group size is wrong")
                raiseNotDefined()
    

    def get1o(self,parent_state,agt_id):
        new_state = {}
        for var_index,value in parent_state.items():
            if self.external.checkVisibility(parent_state,agt_id,var_index,self.entities,self.variables)==PDDL_TERNARY.TRUE:
                new_state.update({var_index: value})
        
        return new_state
    # def get1o(self,agt_id,p,prefix, actions_str_old, actions_str_new,p_path):

   
    '''
    def get1p(self,agt_id,parent_state,os,parent_ps):
        new_state = {}
        for v_index,e in parent_state.items():
            # self.logger.debug('\t find history value for [%s],[%s]',v_index,e)
            ts_index = self._identifyLastSeenTimestamp(os,v_index)
            # self.logger.debug('\t last seen timestamp index: [%s]',ts_index)
            value = self._identifyMemorizedValue(parent_ps, ts_index,v_index)
            # self.logger.debug('\t [%s]"s value is: [%s]',v_index,value)
            new_state.update({v_index:value})
        return new_state 
    
    def _identifyLastSeenTimestamp(self,observation_list:typing.List,v_index):
        ts_index_temp = len(observation_list) -1
        
        # checking whether the variable has been seen by the agent list before
        while ts_index_temp >=0:
            
            # state,_ = path[ts_index_temp]

            # checking with observation
            if v_index in observation_list[ts_index_temp] :
                return ts_index_temp
            else:
                ts_index_temp -= 1
        return -1
    
    
    def _identifyMemorizedValue(self,ps, ts_index,v_index):
        ts_index_temp = ts_index

        if ts_index_temp <0: return None


        while ts_index_temp >=0:
            temp_observation = ps[ts_index_temp]

            if not v_index in temp_observation or temp_observation[v_index] == None:
                ts_index_temp += -1
            else:
                #
                return temp_observation[v_index]
        
        ts_index_temp = ts_index + 1
    
        while ts_index_temp < len(ps):
            temp_observation = ps[ts_index_temp]

            if not v_index in temp_observation or temp_observation[v_index] == None:
                ts_index_temp += 1
            else:
                #
                return temp_observation[v_index]        
        return None    
    '''
  

    # this is wrong
    # def _identifyMemorizedValue(self,observation_list, ts_index,v_index):
    #     ts_index_temp = ts_index
    #     if ts_index_temp <0:
    #         self.logger.debug("return None because agent has not seen this variable ever")
    #         return None
        
    #     self.logger.debug("observation list: [%s]",observation_list)
    #     for i in range(len(observation_list)):
    #         index = len(observation_list) - i -1
    #         if v_index in observation_list[index].keys() and not observation_list[index][v_index] == None:
    #             return observation_list[index][v_index]    
    #     return None


    # def _generateOnePerspectives(self,agt_id,p,p_path):
        # state_template = path[0][0]
        # new_path = []
        
        # observation_list = []
        
        # for i in range(len(path)):
        #     observation_list.append(self._getOneObservation(path[i][0],agt_id))
        # self.logger.debug('observation list is [%s]',observation_list)
        # for i in range(len(path)):
        #     new_state = self._generateOnePerspective(state_template,observation_list[:i+1])
        #     new_path.append((new_state,path[i][1]))
        # return new_path

    # def _generateOnePerspective(self,state_template,observation_list):
    #     new_state = {}
    #     for v_index,e in state_template.items():
    #         self.logger.debug('\t find history value for [%s],[%s]',v_index,e)
    #         ts_index = self._identifyLastSeenTimestamp(observation_list,v_index)
    #         self.logger.debug('\t last seen timestamp index: [%s]',ts_index)
    #         value = self._identifyMemorizedValue( observation_list, ts_index,v_index)
    #         self.logger.debug('\t [%s]"s value is: [%s]',v_index,value)
    #         new_state.update({v_index:value})
    #     return new_state 

    
    
    
    
    
    
    
    


    def partially_converting_to_eq(self,eq_str):
        match = re.search("[edc]?[ksb] \[[0-9a-z_,]*\] ",eq_str)
        if match == None:
            # it means this might be a variable = value string instead of a eq_string
            # for example(= (face c) 'head'))
            # self.logger.debug("return eq string [%s]",eq_str)
            return eq_str
        else:
            eq_list = eq_str.split(" ")
            header_str = eq_list[0]
            agents = eq_list[1]
            content = eq_str[len(header_str)+len(agents)+2:]
            return EpistemicQuery(header_str,agents,content)
        