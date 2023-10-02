import enum
# import pddl_model
import typing
import re
import logging
import copy
from util import PDDL_TERNARY,EP_VALUE
from util import EpistemicQuery,EQ_TYPE,Q_TYPE


LOGGER_NAME = "forward_epistemic_model"
LOGGER_LEVEL = logging.INFO
# LOGGER_LEVEL = logging.DEBUG
from util import setup_logger
from util import ActionList2DictKey,GLOBAL_PERSPECTIVE_INDEX, ROOT_NODE_ACTION
from util import raiseNotDefined,eval_var_from_str
PRE_INIT_PDICT_KEY = ActionList2DictKey([])


class EpistemicModel:
    logger = None
    external = None
    entities = {}
    variables = {}
    
    
    def __init__(self, handlers, entities, variables, external):
        self.logger = setup_logger(LOGGER_NAME,handlers,logger_level=LOGGER_LEVEL) 
        self.entities = entities
        self.variables = variables
        self.external = external
        self.goal_p_keys = None
        self.pre_p_keys = None
        self.all_p_keys = list()






    # def allPerspectiveKeys(self, epistemic_goals_dict,prefix):
    #     self.logger.debug('')
    #     self.logger.debug('allPerspectiveKeys')
    #     self.logger.debug('prefix: [%s]',prefix)
    #     eq_dict = {}
    #     perspective_name_list = set([''])
    #     for epistemic_goal_str,value in epistemic_goals_dict.items():
    #         temp_eq = self.partially_converting_to_eq(epistemic_goal_str)
    #         if type(temp_eq) == str:
    #             # this is the end of eq
    #             # no need to generate perspectives
    #             # just need to evaluate the result and return value
    #             # key = f"{prefix} {temp_eq}"
    #             # perspective_name_list.add("")
    #             pass
                
    #         else:
    #             # it means the query is not to the last level yet
    #             agents_str = temp_eq.agents_str
    #             self.logger.debug("agent_str: [%s]",agents_str)
    #             content = temp_eq.q_content
    #             # key = f"{prefix} {temp_eq.header_str} {agents_str}"
    #             key = f"{temp_eq.header_str} {agents_str} "
    #             if key in eq_dict.keys():
    #                 eq_dict[key]['content'].update({content:value})
    #             else:
    #                 eq_dict[key] = {'q_type':temp_eq.q_type,'eq_type':temp_eq.eq_type,'q_group':temp_eq.q_group,'content':{content:value}}
    #             if "," in agents_str:
    #                 # it means this is a group query
    #                 agt_id_list = EpistemicQuery.agtStr2List(agents_str)
    #                 for i in agt_id_list:
    #                     agt_str = EpistemicQuery.agtList2Str([i])
    #                     agt_key = f"{temp_eq.header_str[1]} {agt_str} "
    #                     self.logger. debug("agent key is [%s]",agt_key)
    #                     if i in eq_dict.keys():
    #                         eq_dict[agt_key]['content'].update({content:None})
    #                     else:
    #                         eq_dict[agt_key] = {'q_type':temp_eq.q_type,'eq_type':temp_eq.eq_type,'q_group':temp_eq.q_group,'content':{content:None}}
                    
    #     self.logger. debug('eq_dict in allPerspectiveKeys [%s]',eq_dict)       
        
    #     for key,item in eq_dict.items():
    #         # generate perspectives
    #         new_path = []
    #         eq_type = item['eq_type']
            
    #         self.logger.debug("calling local perspective for [%s] and content [%s]",key,item['content'])
    #         local_p_keys_list = self.allPerspectiveKeys(item['content'],key)
            
    #         self.logger. debug("local_p_keys_list is [%s]",local_p_keys_list)
    #         # perspectives_dict.update(local_perspectives)
    #         self.logger.debug('perspectives_dict before adding local [%s]',perspective_name_list)
    #         for lp_key in local_p_keys_list:
    #             p_key = key+lp_key
    #             perspective_name_list.add(p_key)
            
    #         self.logger.debug('perspectives_dict after adding local [%s]',perspective_name_list)
        
    #     perspective_name_list = sorted(perspective_name_list, key=len)
        
    #     self.logger.debug('returned [%s]',perspective_name_list)
    #     return perspective_name_list
        


    def epistemicGoalsHandler(self,epistemic_goals_dict, prefix, path, p_path):

        self.logger.debug('')
        self.logger.debug('epistemicGoalHandler')
        self.logger.debug('prefix: [%s]',prefix)
        
        action_list = [a for s,a in path]
        state_list = [s for s,a in path]
        self.logger.debug(action_list)
        old_actions_str = ActionList2DictKey(action_list=action_list[:-1])
        actions_str = ActionList2DictKey(action_list=action_list)
        # if "-,,move_right-a,sharing-b,move_right-b" in actions_str:
        #     self.logger.setLevel(logging.DEBUG)
            
        self.logger.debug("actions_str [%s], old_actions_str [%s]",actions_str,old_actions_str)
        
        
       
        result_dict = dict()
        
        for key, item in epistemic_goals_dict.items():
            eq_str = item.query
            self.logger.debug(eq_str)
            # eq = self.partially_converting_to_eq(eq_str)

            output = self.eval_eq_in_ps(eq_str,prefix, GLOBAL_PERSPECTIVE_INDEX, old_actions_str, actions_str, state_list, p_path,seeing_flag=False)
            result_dict[key] = output

        # self.logger.setLevel(logging.INFO)
                
        return result_dict
    
    def eval_eq_in_pss(self,eq_str,prefix, parent_prefix, actions_str_old, actions_str_new, p_list, p_path,seeing_flag=False):
        eq = self.partially_converting_to_eq(eq_str)
        value_list = []
        for p in p_list:
            
            value = self.eval_eq_in_ps(eq_str,prefix, parent_prefix, actions_str_old, actions_str_new, p, p_path,seeing_flag)
            self.logger.debug("PSS: eq str: [%s] is [%s]",eq,value)
            value_list.append(value)
            
        if eq.q_type == Q_TYPE.MUTUAL or eq.q_type == Q_TYPE.COMMON:
            return min(value_list)
        elif eq.q_type == Q_TYPE.DISTRIBUTION:
            return max(value_list)
        else:
            raiseNotDefined()
    
    def eval_eq_in_ps(self,eq_str,prefix, parent_prefix, actions_str_old, actions_str_new, p, p_path,seeing_flag=False):
        eq = self.partially_converting_to_eq(eq_str)
        
        # self.logger.debug(p)
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
                    
                    temp_ps = None
                    while not new_ps == temp_ps:
                        for_p = new_ps.copy()
                        temp_ps = new_ps.copy()
                        new_ps = list()
                        # added = set()
                        for temp_p in for_p:
                            for agt_id in eq.q_group:
                                new_prefix = prefix + eq.header_str + " " + EpistemicQuery.agtList2Str([agt_id])
                                self.logger.debug("input perspective: [%s]",temp_p)
                                new_temp_p = self.get1ps(agt_id,temp_p, new_prefix, actions_str_old, actions_str_new, p_path)
                                self.logger.debug("[%s]'s perspective: [%s]",agt_id,new_temp_p)
                                new_t_p_str = str(new_temp_p)
                                if not new_temp_p in new_ps:
                                # if new_t_p_str not in added:
                                    # added.add(new_t_p_str)
                                    new_ps.append(new_temp_p)
                        self.logger.debug("all perspective: [%s]",new_ps)
                        
                else:
                    for agt_id in eq.q_group:
                        new_prefix = prefix + eq.header_str + " " + EpistemicQuery.agtList2Str([agt_id])
                        new_temp_p = self.get1ps(agt_id,p, new_prefix, actions_str_old, actions_str_new, p_path)
                        new_ps.append(new_temp_p)

                result_list = []
                
                
                self.logger.debug("[%s] pss: [%s]",eq_str,new_ps)
                for p in new_ps:
                    
                    value = self.eval_eq_in_ps(eq.q_content,prefix, parent_prefix, actions_str_old, actions_str_new, p, p_path,seeing_flag)
                    self.logger.debug("PSS: eq str: [%s] is [%s]",eq,value)
                    result_list.append(value)
                    
                if eq.q_type == Q_TYPE.MUTUAL or eq.q_type == Q_TYPE.COMMON:
                    return min(result_list)
                elif eq.q_type == Q_TYPE.DISTRIBUTION:
                    return max(result_list)
                else:
                    raiseNotDefined()
                # new_eq_str = EpistemicQuery.partial_eq2str(eq.q_type,eq.eq_type,eq.q_group) + eq.q_content
                
                # return self.eval_eq_in_pss(new_eq_str,new_prefix, prefix, actions_str_old, actions_str_new, new_ps, p_path,seeing_flag)
            
            
            elif len(eq.q_group) == 1:
                new_prefix = prefix + eq.header_str + " " + EpistemicQuery.agtList2Str(eq.q_group)
                self.logger.debug("input perspective: [%s]",p)
                new_p = self.get1ps(eq.q_group[0],p,new_prefix, actions_str_old, actions_str_new,p_path)
                self.logger.debug("[%s]'s perspective: [%s]",eq.q_group[0],new_p)
                return self.eval_eq_in_ps(eq.q_content,new_prefix,prefix, actions_str_old, actions_str_new, new_p, p_path,seeing_flag)
            else:
                self.logger.error("group size is wrong")
                raiseNotDefined()


    def get1ps(self,agt_id,p,prefix, actions_str_old, actions_str_new,p_path):
        parent_state = p[-1]
        p_str = str(p)
        # self.logger.debug(actions_str_new)
        # self.logger.debug(ActionList2DictKey([ROOT_NODE_ACTION]))
        # self.logger.debug("test")
        # self.logger.debug("[%s]",)
        self.logger.debug("agt_id [%s]",agt_id)
        self.logger.debug("prefix [%s]",prefix)
  
        if actions_str_new == ActionList2DictKey([ROOT_NODE_ACTION]):

            if actions_str_old not in p_path:
                p_path[actions_str_old] = dict()
                p_path[actions_str_old]["p_parent"] = list({})
                p_path[actions_str_old]["observation"] = list({})
                p_path[actions_str_old]["perspectives"] = list({})
            current_level_dict = dict()
            current_level_dict["p_parent"] = list()
            current_level_dict["observation"] = list()
            current_level_dict["perspectives"] = list()
        else:
            existing_p_dict = p_path[actions_str_old]
            current_level_dict = existing_p_dict[prefix]
            
            
        self.logger.debug("actions_str_old [%s]",actions_str_old)
        self.logger.debug("current_level_dict [%s]",current_level_dict)

            
        # self.logger.debug(p_path)
        
        if not actions_str_new in p_path.keys():
            p_path[actions_str_new] = dict()
        if not prefix in p_path[actions_str_new].keys():
            p_path[actions_str_new][prefix] = dict()
            p_path[actions_str_new][prefix]['p_parent'] = p
        
        self.logger.debug("actions_str_new [%s]",actions_str_new)
        
        self.logger.debug("p_path[actions_str_new][prefix] [%s]",p_path[actions_str_new][prefix])
        
        
        if p_path[actions_str_new][prefix]['p_parent'] == p:
            self.logger.debug("p_parent is the same")
            if "observation" in p_path[actions_str_new][prefix].keys() and not p_path[actions_str_new][prefix]["observation"]==list():
                self.logger.debug("observation is not empty [%s]",p_path[actions_str_new][prefix]['observation'])
                new_os = p_path[actions_str_new][prefix]['observation']
            else:
                
                p_path[actions_str_new][prefix]['p_parent'] = p
                old_os = current_level_dict["observation"]
                new_o = self.get1o(parent_state,agt_id)
                new_os =  old_os + [new_o]
                self.logger.debug("observation is not found [%s]",new_os)
                p_path[actions_str_new][prefix]['observation'] = new_os 
            
            if "perspectives" in p_path[actions_str_new][prefix].keys() and not p_path[actions_str_new][prefix]["perspectives"]==list():
                return p_path[actions_str_new][prefix]['perspectives']
            else:
                
                old_ps = current_level_dict["perspectives"]
                parent_state = p[-1]
                new_p = self.get1p(parent_state,new_os)
                new_ps =  old_ps + [new_p]
                p_path[actions_str_new][prefix]['perspectives'] = new_ps
                
                return new_ps
        else:
            self.logger.debug("p_parent is the different, must be cb")
            self.logger.debug("input p is: [%s]",p)
            new_os = []
            for temp_p in p:
                temp_o = self.get1o(temp_p,agt_id)
                new_os.append(temp_o)
            
            new_ps = []
            for i in range(len(p)):
                temp_p = self.get1p(p[i],new_os[:i+1:])
                new_ps.append(temp_p)
            
            return new_ps

    
    def get1o(self,parent_state,agt_id):
        new_state = {}
        for var_index,value in parent_state.items():
            if self.external.checkVisibility(parent_state,agt_id,var_index,self.entities,self.variables)==PDDL_TERNARY.TRUE:
                new_state.update({var_index: value})
        return new_state
    # def get1o(self,agt_id,p,prefix, actions_str_old, actions_str_new,p_path):

    def get1p(self,parent_state,os):
        new_state = {}
        for v_index,e in parent_state.items():
            self.logger.debug('\t find history value for [%s],[%s]',v_index,e)
            ts_index = self._identifyLastSeenTimestamp(os,v_index)
            self.logger.debug('\t last seen timestamp index: [%s]',ts_index)
            value = self._identifyMemorizedValue( os, ts_index,v_index)
            self.logger.debug('\t [%s]"s value is: [%s]',v_index,value)
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

    def _identifyMemorizedValue(self,observation_list, ts_index,v_index):
        ts_index_temp = ts_index
        if ts_index_temp <0: return None
        
        while ts_index_temp >=0:

            # temp_observation = self.getObservations(external,state,agt_id,entities,variables)
            # logger.debug(f'temp observation in identifyMemorization: {temp_observation}')
            temp_observation = observation_list[ts_index_temp]
            if not v_index in temp_observation or temp_observation[v_index] == None:
                ts_index_temp += -1
            else:
                return temp_observation[v_index]
        
        ts_index_temp = ts_index + 1
        
        while ts_index_temp < len(observation_list):

            # temp_observation = self.getObservations(external,state,agt_id,entities,variables)
            temp_observation = observation_list[ts_index_temp]
            if not v_index in temp_observation or temp_observation[v_index] == None:
                ts_index_temp += 1
            else:
                return temp_observation[v_index]        
        return None


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
        
        
    # def _initialize_P(self,p_key,any_full_state,p_path):
    #     # if action_key not in p_path.keys():
    #     #     p_path[action_key] = dict()
        

    #     # if action_key == PRE_INIT_PDICT_KEY:
    #     empty_state = dict()
    #     empty_updates = dict()
    #     for v_name in any_full_state.keys():
    #         empty_state[v_name]= EP_VALUE.HAVENT_SEEN
    #         empty_updates[v_name]= False
    #     p_path[PRE_INIT_PDICT_KEY][p_key] = dict()
    #     p_path[PRE_INIT_PDICT_KEY][p_key]['states'] = [empty_state]
    #     p_path[PRE_INIT_PDICT_KEY][p_key]['updates'] = [empty_updates]

    # def _evaluateContent(self,path,temp_eq):

    #     state = path[-1][0]
    #     # optional to add keywords to represent the value of formula
    #     # and it can be put into the external function
        
    #     # assuming the query only about value of variables here
    #     content_list = temp_eq[1:-1].split(",")
    #     v_index = content_list[0].replace("'","")
    #     value = content_list[1].replace("'","")
        
        
    #     if v_index not in state.keys():
    #         return PDDL_TERNARY.UNKNOWN
    #     elif state[v_index] == value:
    #         return PDDL_TERNARY.TRUE
    #     else:
    #         return PDDL_TERNARY.FALSE
    
    # def _generateGroupPerspectives(self,q_type,group_p_key,acts_name_str,previous_acts_name_str,parent_key,p_path):
    #     # if len(q_group) == 1:
    #     #     new_state,new_update = self._generateOnePerspectives(q_group[0],parent_state,p_path)
    #     #     return new_state,new_update
    #     # else:
    #     agent_str = group_p_key.split(' ')[1]
    #     q_group = EpistemicQuery.agtStr2List(agent_str=agent_str)
    #     full_group_p_key = parent_key + group_p_key


    #     if q_type == Q_TYPE.MUTUAL:
            
    #         new_state,new_update = self._mergePUs(q_group,group_p_key,parent_key,acts_name_str,previous_acts_name_str,p_path,intersection_flag=True)
    #         p_path[acts_name_str][full_group_p_key]["states"] = p_path[previous_acts_name_str][full_group_p_key]["states"] + [new_state]
    #         p_path[acts_name_str][full_group_p_key]["updates"] = p_path[previous_acts_name_str][full_group_p_key]["updates"] + [new_update]
    #     elif q_type == Q_TYPE.DISTRIBUTION:
    #         new_state,new_update = self._mergePUs(q_group,group_p_key,parent_key,acts_name_str,previous_acts_name_str,p_path,intersection_flag=False)
    #         p_path[acts_name_str][full_group_p_key]["states"] = p_path[previous_acts_name_str][full_group_p_key]["states"] + [new_state]
    #         p_path[acts_name_str][full_group_p_key]["updates"] = p_path[previous_acts_name_str][full_group_p_key]["updates"] + [new_update]
    #     elif q_type == Q_TYPE.COMMON:
    #         new_state,new_update = self._fixpointPUs(q_group,group_p_key,parent_key,acts_name_str,previous_acts_name_str,p_path,intersection_flag=True)
    #         self.logger.debug("cb is [%s]",new_state)
    #         p_path[acts_name_str][full_group_p_key]["states"] = p_path[previous_acts_name_str][full_group_p_key]["states"] + [new_state]
    #         p_path[acts_name_str][full_group_p_key]["updates"] = p_path[previous_acts_name_str][full_group_p_key]["updates"] + [new_update]
    #     else:
    #         assert False,"wrong Q type"

    # def _fixpointPUs(self,q_group,group_p_key,parent_key,acts_name_str,previous_acts_name_str,p_path,intersection_flag = True):
    #     # generating first level
    #     full_group_p_key = parent_key+group_p_key.replace("c","e")
    #     new_state,new_update = self._mergePUs(q_group,full_group_p_key,parent_key,acts_name_str,previous_acts_name_str,p_path,intersection_flag=True)
    #     if full_group_p_key not in p_path[previous_acts_name_str].keys():
    #         self._initialize_P(full_group_p_key,new_state,p_path)
    #     p_path[acts_name_str][full_group_p_key] = dict()
    #     p_path[acts_name_str][full_group_p_key]["states"] = p_path[previous_acts_name_str][full_group_p_key]["states"] + [new_state]
    #     p_path[acts_name_str][full_group_p_key]["updates"] = p_path[previous_acts_name_str][full_group_p_key]["updates"] + [new_update]
    #     temp_state = dict()
    #     temp_update = dict()
    #     temp_full_group_p_key = full_group_p_key
    #     while (not temp_state == new_state) or (not temp_update == new_update):
            
    #         temp_state = new_state
    #         temp_update = new_update
    #         self.logger.debug("temp_state is: [%s]",temp_state)
    #         full_group_p_key = temp_full_group_p_key.replace("c","e")
    #         new_state,new_update = self._mergePUs(q_group,group_p_key,full_group_p_key,acts_name_str,previous_acts_name_str,p_path,intersection_flag=True)
    #         if full_group_p_key not in p_path[previous_acts_name_str].keys():
    #             self._initialize_P(full_group_p_key,new_state,p_path)
    #         p_path[acts_name_str][full_group_p_key] = dict()
    #         p_path[acts_name_str][full_group_p_key]["states"] = p_path[previous_acts_name_str][full_group_p_key]["states"] + [new_state]
    #         p_path[acts_name_str][full_group_p_key]["updates"] = p_path[previous_acts_name_str][full_group_p_key]["updates"] + [new_update]
    #         temp_full_group_p_key = full_group_p_key
    #     return new_state,new_update



    # def _mergePUs(self,q_group,group_p_key,parent_key,acts_name_str,previous_acts_name_str,p_path,intersection_flag = True):

    #     self.logger.debug("merging perspectives")
    #     self.logger.debug("q_group is [%s]",q_group)
    #     self.logger.debug("parent key is [%s]",parent_key)
    #     self.logger.debug("group_p_key is [%s]",group_p_key)

        
    #     eq_type_str = group_p_key.split(" ")[0]
    #     if len(eq_type_str) > 1:
    #         eq_type_str = eq_type_str[1]
    #     agt_str = EpistemicQuery.agtList2Str([q_group[0]])
    #     agt_str = eq_type_str + " " + agt_str
    #     p_key = parent_key + agt_str + " " #if not parent_key == GLOBAL_PERSPECTIVE_INDEX else agt_str + " "
    #     # p_key = eq_type_str + " " + p_key
    #     self.logger. debug("p_key is [%s]",p_key)

    #     self.logger.debug("p_path [%s]'s keys are [%s]: ",acts_name_str, p_path[acts_name_str].keys())


    #     parent_state = p_path[acts_name_str][parent_key]["states"][-1]
    #     self.logger.debug("parent state [%s]: [%s]",parent_key,parent_state)
        
    #     if p_key not in p_path[previous_acts_name_str]:
    #         self._initialize_P(p_key,parent_state,p_path)
    #     previous_pu = p_path[previous_acts_name_str][p_key]
        

    #     new_state,new_update = self._generateOnePerspectives(q_group[0],parent_state,previous_pu)
    #     self.logger.debug("[%s] state: [%s]",p_key,new_state)
    #     self.logger.debug("[%s] new_update: [%s]",p_key,new_update)
    #     # update p_path for future reference

    #     p_path[acts_name_str][p_key] = dict()
    #     p_path[acts_name_str][p_key]['states'] = previous_pu['states'] + [new_state]
    #     p_path[acts_name_str][p_key]['updates'] = previous_pu['updates'] + [new_update]
    #     new_state_list = p_path[acts_name_str][p_key]['states'] 
    #     new_update_list = p_path[acts_name_str][p_key]['updates'] 


    #     self.logger.debug("[%s]'s p: [%s]",q_group[0],new_state)
    #     self.logger.debug("[%s]'s updates: [%s]",q_group[0],new_update)
    #     if len(q_group) > 1:
    #         for i in range(len(q_group)-1):
    #             temp_state = new_state
    #             temp_update = new_update
    #             temp_state_list = new_state_list
    #             temp_update_list = new_update_list


    #             agt_str = EpistemicQuery.agtList2Str([q_group[i+1]])
    #             agt_str = eq_type_str + " " + agt_str
    #             p_key = parent_key + agt_str + " " 


    #             if p_key not in p_path[previous_acts_name_str]:
    #                 self._initialize_P(p_key,parent_state,p_path)

    #             previous_pu = p_path[previous_acts_name_str][p_key]
    #             new_state,new_update = self._generateOnePerspectives(q_group[i+1],parent_state,previous_pu)
    #             # update p_path for future reference
    #             self.logger.debug("[%s] state: [%s]",p_key,new_state)
    #             self.logger.debug("[%s] new_update: [%s]",p_key,new_update)
    #             p_path[acts_name_str][p_key] = dict()
    #             p_path[acts_name_str][p_key]['states'] = previous_pu['states'] + [new_state]
    #             p_path[acts_name_str][p_key]['updates'] = previous_pu['updates'] + [new_update]
    #             # new_state_list = p_path[acts_name_str][p_key]['states'] 
    #             # new_update_list = p_path[acts_name_str][p_key]['updates'] 

    #             self.logger.debug("[%s]'s p: [%s]",q_group[i+1],new_state)
    #             self.logger.debug("[%s]'s updates: [%s]",q_group[i+1],new_update)
    #             new_state = self._mergeS(new_state,temp_state,intersection_flag=intersection_flag)
    #             new_update = self._mergeU(new_update,temp_update,intersection_flag=intersection_flag)
    #             # new_state_list,new_update_list = self._mergePU(new_state_list,new_update_list,temp_state_list,temp_update_list ,intersection_flag=True)
    #             # new_state = self._mergeS(new_state,temp_state,intersection_flag=intersection_flag)
    #             # new_updates = self._mergeU(new_updates,temp_update,intersection_flag=intersection_flag)
    #             self.logger.debug("p after merge: [%s]",new_state)
                
            
    #         # group_key = ",".join(q_group)
    #         # group_key = EpistemicQuery.agtList2Str(q_group) + " "
                
    #     return new_state,new_update





    # def _mergePU(self,s_list1,u_list1,s_list2,u_list2,intersection_flag = True):
    #     self.logger. debug("p1 is [%s] and its len is [%s]",s_list1,len(s_list1))
    #     self.logger. debug("p2 is [%s] and its len is [%s]",s_list2,len(s_list2))
    #     assert (len(s_list1)==len(s_list2)),"merging two lists with different length"
    #     new_s_list = list()
    #     new_u_list = list()
    #     for i in range(len(s_list1)):
    #         temp_s = self._mergeS(s_list1[i],s_list2[i])
    #         new_s_list.append(temp_s)
    #         temp_u = self._mergeS(u_list1[i],u_list2[i])
    #         new_u_list.append(temp_u)            
    #     return new_s_list,new_u_list
        

    # # def _mergeP(self,p1,p2, intersection_flag = True):
    # #     self.logger.debug("p1 is [%s] and its len is [%s]",p1,len(p1))
    # #     self.logger.debug("p2 is [%s] and its len is [%s]",p2,len(p2))
    # #     assert (len(p1)==len(p2)),"merging two lists with different length"
    # #     new_p = list()
    # #     new_updates = list()
    # #     for i in p1.items():
    # #         temp_state = self._mergeS(p1[i],p2[i])
    # #         temp_update = self._mergeU(us1[i],us2[i])
    # #         new_p.append(temp_state)
    # #         new_updates.append(temp_update)
    # #     return new_p,new_updates

    # def _mergeU(self,u1,u2, intersection_flag = True):
    #     assert (len(u1)==len(u2)),"merging two updates with different length"
    #     new_update = dict()
    #     for k,v1 in u1.items():
    #         v2=u2[k]
    #         if intersection_flag:
    #             new_update[k] = intersectUpdates(v1,v2)
    #         else:
    #             new_update[k] = unionUpdate(v1,v2)
    #     return new_update


    # def _mergeS(self, s1,s2, intersection_flag = True):
    #     assert (len(s1)==len(s2)),"merging two states with different length"
    #     new_state = dict()
    #     for k,v1 in s1.items():
    #         v2=s2[k]
    #         if intersection_flag:
    #             new_state[k] = intersectBeliefValue(v1,v2)
    #         else:
    #             new_state[k] = unionBeliefValue(v1,v2)
    #     return new_state

    # def _generateGroupObservations(self,q_type,q_group,parent_state,p_path):
    #     # initial perspectives 

    #     new_state,new_update = self._getOneObservation(parent_state,q_group[0])
        
    #     if len(q_group) == 1:
    #         return new_state,new_update
    #     else:
    #         if q_type == Q_TYPE.MUTUAL:
    #             pass
    #         elif q_type == Q_TYPE.DISTRIBUTION:
    #             pass
    #         elif q_type == Q_TYPE.COMMON:
    #             pass
    #         else:
    #             assert False,"wrong Q type"

    
    # def _generateOnePerspectives(self,agt_id,parent_state,previous_p):
    #     self.logger.debug("parent state: [%s]",parent_state)
    #     self.logger.debug("previous_p: [%s]",previous_p)

    #     previous_update = previous_p['updates'][-1]
    #     previous_state = previous_p['states'][-1]

    #     self.logger.debug("previous_state: [%s]",previous_state)
    #     self.logger.debug("previous_update: [%s]",previous_update)

    #     observation,_ = self._getOneObservation(parent_state,agt_id)

    #     self.logger.debug("observation: [%s]",observation)

        
    #     new_update = previous_update.copy()
    #     new_state = previous_state.copy()

        
    #     for v_name, updating in previous_update.items():
    #         if updating:
    #             # it means the value has been seen before but have not been updated
    #             if parent_state[v_name]== EP_VALUE.NOT_SEEING:
    #                 # it means the value is not visible in its parent perspective
    #                 # we have nothing to update the value, 
    #                 # so update status stays the same, the value stays the same
    #                 #   which means it will get updated in the future

    #                 pass
    #             # the below should not happen
    #             elif parent_state[v_name] == EP_VALUE.HAVENT_SEEN:
    #                 # it means the value is not visible (has not been seen) in its parent perspective
    #                 pass

    #             elif parent_state[v_name] == EP_VALUE.CONFLICT:
    #                 # it means the value has conflict in its parent perspective
    #                 pass

    #             else:
    #                 # it means the value is visible in its parent perspective
    #                 new_state[v_name] = parent_state[v_name]
    #                 new_update[v_name] = False
    #         # elif updating and parent_state[v_name] == EP_VALUE.HAVENT_SEEN:
    #         #     # still no valid updates, will update in the next state
    #         #     pass
    #         # else:
    #         #     # the value does not need to be updated
    #         #     pass

        
    #     for v_name,value in observation.items():
    #         if value == EP_VALUE.NOT_SEEING or value == EP_VALUE.HAVENT_SEEN:
    #             # the agent observes this value
    #             # but the value is None due to its parent
    #             # so this value needed update once its parent seen this value
    #             new_update[v_name] = True
    #         else:
    #             new_state[v_name] = value
    #             new_update[v_name] = False

    #     self.logger.debug("new_state: [%s]",new_state)
    #     self.logger.debug("new_update: [%s]",new_update)
    #     return new_state,new_update
    
    # def _getOneObservation(self,state,agt_id):
    #     new_state = {}
    #     new_update = {}

    #     for v_name,value in state.items():
    #         if self.external.checkVisibility(state,agt_id,v_name,self.entities,self.variables)==PDDL_TERNARY.TRUE:
    #             new_state.update({v_name: value})
    #         else:
    #             new_update.update({v_name:EP_VALUE.NOT_SEEING})

    #     return new_state,new_update
    
    

        
    # def intersectObservation(self,state1,state2):
    #         new_state = {}
    #         for k,v in state1.items():
    #             if k in state2.keys():
    #                 if v == state2[k]:
    #                     new_state[k] = v
    #         return new_state

        
        