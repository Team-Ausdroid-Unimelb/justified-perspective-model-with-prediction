# from model import Problem,E_TYPE,PDDL_TERNARY
import logging 
import math
from typing import Tuple
import numpy as np
import traceback

import re

from util import PDDL_TERNARY,EP_VALUE
from util import EpistemicQuery,E_TYPE
AGENT_ID_PREFIX = "agent_at-"
AGENT_LOC_PREFIX = 'agent_at-'
OBJ_LOC_PREFIX = 'shared-'


from datetime import datetime, timedelta
SPLIT_KEY_WORD = '@'
# all the immediate variable that not belong to landmark constrains
AGENT_VARIABLES = ['agent_at-']
OBJECT_VARIABLES = ['secret-','shared-']
FILTER_VARIABLES = ['shared-']


# logger = logging.getLogger("bbl")


LOGGER_NAME = "grapevine"
LOGGER_LEVEL = logging.INFO
# LOGGER_LEVEL = logging.DEBUG
from util import setup_logger
 
# declare common variables
common_constants = {

}



class ExternalFunction:
    logger = None
    
    def __init__(self, handlers):
        self.logger = setup_logger(LOGGER_NAME,handlers,logger_level=LOGGER_LEVEL) 

    # # customized evaluation function

    # extract variables from the query
    # def extractVariables(self,eq):
    #     # expected output would be a list of (var_name,value)
    #     if not type(eq) == epistemic_model.EpistemicQuery:
    #         # default is a single pair of var_name and value
    #         if not re.search("\([0-9a-z _\-\'\"]*,[0-9a-z _\'\"]*\)",eq) == None:
    #             var_name = eq.split(",")[0][1:]
    #             value = eq.split(",")[1][:-1]
    #             return [(var_name.replace('"','').replace("'",''),value.replace('"','').replace("'",''))]
    #         else:
    #             # customized function here
    #             pass
    #     else:
    #         return self.extractVariables(eq.q_content)
    
    # def extractVariable(self,q_content_str):
    #     print(q_content_str)
    #     if not re.search("\([0-9a-z _\-\'\"]*,[0-9a-z _\'\"]*\)",q_content_str) == None:
    #         var_name = q_content_str.split(",")[0][1:]
    #         value = q_content_str.split(",")[1][:-1]
    #         return (var_name.replace('"','').replace("'",''),value.replace('"','').replace("'",''))
    #     else:
    #         # customized function here
    #         pass

    # def extractAgents(self,eq):
    #     if not type(eq) == epistemic_model.EpistemicQuery:
    #         return []
    #     else:
            
    #         return eq.q_group + self.extractVariables(eq.q_content)    

    # customized evaluation function
    def evaluateS(self,world,statement):
        #default evaluation for variables
        if world == {}:
            return 2
        if not re.search("\([0-9a-z _\-\'\"]*,[0-9a-z _\'\"]*\)",statement) == None:
            var_name = statement.split(",")[0][1:].replace("'",'').replace('"','')
            value = statement.split(",")[1][:-1].replace("'",'').replace('"','')
            if var_name in world:
                return 1
            else:
                return 0
        else:
            self.logger.warning("the evaluation of the seeing equation has not defined")
            return 0

    def agentsExists(self,path,g_group_index):
        state = path[-1][0]
        for agt_id in g_group_index:
            if not AGENT_ID_PREFIX+agt_id in state.keys():
                return False
        return True
    
    def checkVisibility(self,state,agt_index,var_name,entities,variables):
        
        try:
            # self.logger.debug('checking seeing for agent [%s] on [%s]  in state [%s]',agt_index,var_name,state)
            tgt_index = variables[var_name].v_parent
            
            # check if the agt_index can be found
            assert(entities[agt_index].e_type==E_TYPE.AGENT)
            
            # if the variable contains shared or secret, then it means checking secret location
            # which mean checking location of shared (agent's own secret can be shared by others)
            # otherwise it checking agent's current location
            # if 'shared' in var_name or 'secret' in var_name:
            if 'secret' in var_name:
                tgt_loc = state[f'shared-{tgt_index}']
                if type(tgt_loc) == str:
                    tgt_loc = int(state[f'shared-{tgt_index}'])

                # agent should know their own secret before sharing
                if tgt_index == agt_index and tgt_loc == 0:
                    return PDDL_TERNARY.TRUE
                
                # if the secret has not been shared
                if tgt_loc == 0:
                    return PDDL_TERNARY.FALSE
                
                
            elif 'shared' in var_name:
                tgt_loc = state[f'shared-{tgt_index}']
                if type(tgt_loc) == str:
                    tgt_loc = int(state[f'shared-{tgt_index}'])
                
                # agent knows if a secret is not been shared
                # this is to break the continues effect of a sharing secret
                if tgt_loc == 0:
                    return PDDL_TERNARY.TRUE
                    
            
            else:
                # the target is an agent, it has its own location
                # tgt_loc = int(state[f'agent_at-{tgt_index}'])
                # Since in Grapevine domain, there is only two rooms
                # agent will know others location if they are in the same room
                # agent will also know others location if they are not in the same room
                return PDDL_TERNARY.TRUE


            agt_loc_str = AGENT_LOC_PREFIX+agt_index
            if agt_loc_str not in state.keys()\
                or state[agt_loc_str] == None\
                    or state[agt_loc_str] == EP_VALUE.HAVENT_SEEN\
                        or state[agt_loc_str] == EP_VALUE.NOT_SEEING:
                return PDDL_TERNARY.UNKNOWN
            else:
                agt_loc = int(state[agt_loc_str])

            
            # extract necessary common constants from given domain
            # logger.debug(f"necessary common constants from given domain")

            # logger.debug(f'checking seeing with agent location: {agt_loc} and target location: {tgt_loc}')
            # agent is able to see anything in the same location
            if tgt_loc == agt_loc:
                return PDDL_TERNARY.TRUE
            else:
                return PDDL_TERNARY.FALSE

        except KeyError:
            self.logger.warning(traceback.format_exc())
            self.logger.warning("variable not found when check visibility")
            # logging.error("error when checking visibility")
            return PDDL_TERNARY.UNKNOWN
        except TypeError:
            self.logger.warning(traceback.format_exc())
            self.logger.warning("variable is None when check visibility")
            # logging.error("error when checking visibility")
            return PDDL_TERNARY.UNKNOWN

    # customise action filters
    # to filter out the irrelevant actions
    def filterActionNames(self,problem,action_dict):
        # print(action_dict.keys())
        action_name_list = []
        relevant_variable_parent_index = []
        relevant_agent_index = []
        

        for key,ep_obj in problem.goals.epistemic_dict.items():
            eq_str = ep_obj.query
            match = re.search("[edc]?[ksb] \[[0-9a-z_,]*\] ",eq_str)
            while not match == None:
                eq_list = eq_str.split(" ")
                relevant_agent_index += eq_list[1][1:-1].split(",")
                eq_str = eq_str[len(eq_list[0])+len(eq_list[1])+2:]
                match = re.search("[edc]?[ksb] \[[0-9a-z_,]*\] ",eq_str)
                
            # variable_name,value =self.extractVariable(eq_str)
            variable_name = ep_obj.variable_name
            #print(variable_name)
            relevant_variable_parent_index.append(problem.variables[variable_name].v_parent)
            self.logger.debug("variable_name[%s] , problem.variables[variable_name].v_parent [%s]",variable_name,problem.variables[variable_name].v_parent)




        for name,action in action_dict.items():
            self.logger.debug('action_name: [%s]',name) 
            if "sharing_" in name:
                if name.split("-")[2] in relevant_variable_parent_index:
                    action_name_list.append(name)
            elif "sharing" in name or "lying" in name:
                if name.split("-")[1] in relevant_variable_parent_index:
                    action_name_list.append(name)
            elif "move" in name:
                self.logger.debug('agent_in: [%s]',name.split("-")[1]) 
                if name.split("-")[1] in relevant_agent_index:
                    action_name_list.append(name) 
            else:
                action_name_list.append(name)
        if logging.getLogger().isEnabledFor(logging.DEBUG):
            self.logger.debug('action names after filter: [%s]',action_name_list)   
        return action_name_list
        return action_dict.keys()

    # if __name__ == "__main__":
        
    #     pass
    

    def generate_constrain_dict(self,problem,group_eg_dict):

        self.logger.debug('')
        self.logger.debug('generate_constrain_dict')
        self.logger.debug('group_eg_dict [%s]',group_eg_dict)
        land_marks = dict()
        for v_name, ep_goals in group_eg_dict.items():
            agents = set()
            land_marks[v_name] = []
            for ep_str,value in ep_goals:
                agents_temp = get_agent_names(ep_str)
                agents.update(agents_temp)
            obj_index,obj_domains,obj_name,obj_value = handlerObject(ep_str,problem)

            variable_dict = get_relative_variables(agents,(obj_index,obj_name,obj_domains),problem)
            states = _all_states(variable_dict)
            valid_states = get_valid_states(agents,states,problem,ep_goals,obj_name)
            if not valid_states == []:

                land_marks[v_name]={'landmark_type': [[list(range(len(ep_goals)))]],'ep_list': ep_goals,'landmarks': valid_states}
            else:
                # cannot achieve group goal in one state
                ep_state_dict = {}
                for ep_str,value in ep_goals: 
                    obj_index,obj_domains,obj_name,obj_value = handlerObject(ep_str,problem)
                    variable_dict = get_relative_variables(agents,(obj_index,obj_name,[obj_value]),problem)
                    states = _all_states(variable_dict)
                    valid_states = get_valid_states(agents,states,problem,[(ep_str,value)],obj_name)
                    ep_state_dict.update({ep_str: {'states':valid_states,'obj_value':obj_value}})
                    for key1 in ep_state_dict.keys():
                        for key2 in ep_state_dict.keys():
                            if not key1 == key2:
                                item1 = ep_state_dict[key1]
                                item2 = ep_state_dict[key2]
                                
                                if item1['obj_value'] == item2["obj_value"]:
                                    # there is not constrain since the values are same
                                    # we might want to get intersection
                                    pass
                                else:
                                    for state in item1['states']:
                                        if state not in item2['states']:
                                            if state not in land_marks[v_name]:
                                                land_marks[v_name].append(state)
                                    for state in item2['states']:
                                        if state not in item1['states']:
                                            if state not in land_marks[v_name]:
                                                land_marks[v_name].append(state)
        return land_marks


    def getps(self, new_os,new_rs,p):
        os_dict = self.get_os_dict(new_os,p)
        ps_dict = {}
        
        for state in p:
            for v_name in state.keys():
                ps_dict[v_name] = [None] * len(p)
                
        for v_name, value in os_dict.items():
            for i in range(len(value)):
                ps_dict[v_name][i] = os_dict[v_name][i]
                if value[i] is None:
                    ps_dict[v_name][i] = self.predict(i,new_rs[v_name],value)

        
        new_ps = []
        for i in range(len(p)):
            new_state = {}  
            for v_name, value in ps_dict.items():
                new_state[v_name] = value[i]  
            new_ps.append(new_state)
        
        return new_ps

    def predict(self, i,rule,value):
        if rule['rule_name'] == 'linear':
           result = self.get_predict_linear(i,rule,value)
           return result
        elif rule['rule_name'] == '2nd_poly':
            result = self.get_predict_2poly(i,rule,value)
            return result
        elif rule['rule_name'] == 'static':
            result = self.get_predict_static(i,rule,value)
            return result
        elif rule['rule_name'] == 'undetermined':
            result = self.get_predict_undetermined(i,rule,value)
            return result
        return None
    
    def get_predict_linear(self, i,rule,value):
        a = rule['coefficients'].get('a')
        b = rule['coefficients'].get('b')
        if a is None or b is None:
            result = self.get_predict_static(i,rule,value)
        else:
            result = round(a * i + b)
        return result
    
    def get_predict_2poly(self, i,rule,value):
        a = rule['coefficients'].get('a')
        b = rule['coefficients'].get('b')
        c = rule['coefficients'].get('c')
        if a is None or b is None or c is None:
            result = self.get_predict_static(i,rule,value)
        else:
            result = round(a * i**2 + b * i + c)
        return result
    
    def get_predict_static(self, i,rule,value):
        result = None
        for j in range(i - 1, -1, -1):
            if value[j] is not None:
                result = value[j] 
                return value[j] 
            
        for j in range(i + 1, len(value)):
            if value[j] is not None:
                result = value[j] 
                return value[j]
        return result
    
    def get_predict_undetermined(self, i,rule,value):
        result = "?"
        return result
    
    def get_os_dict(self, new_os,p):
        os_dict = {}
        for state in p:
            for v_name in state.keys():
                os_dict[v_name] = []

        for state in new_os:
            for v_name in os_dict.keys():
                if v_name in state:
                    os_dict[v_name].append(state[v_name])
                else:
                    os_dict[v_name].append(None)
        return os_dict

    def getrs(self, new_os,p, domains):

        rule_dict = self.get_rule_dict(domains)
        os_dict = self.get_os_dict(new_os,p)
        rs = {}

        for v_name,valuelist in os_dict.items():
            keyword = v_name.split('-')[0] #peeking
            v_rult_type = str(rule_dict[keyword])
            if v_rult_type =='2nd_poly':
                rs[v_name] = self.get_coef_2poly(v_name,valuelist)
            elif v_rult_type =='linear':
                rs[v_name] = self.get_coef_linear(v_name,valuelist)
            elif v_rult_type =='static':
                rs[v_name] = self.get_static(v_name,valuelist)
            elif v_rult_type =='undetermined':
                rs[v_name] = self.get_undetermined(v_name,valuelist)
            else:
                rs[v_name] = self.get_static(v_name,valuelist)

        return rs

    def get_coef_2poly(self, v_name,valuelist):
        os_value_list = []
        for index, value in enumerate(valuelist):
            if value is not None:
                os_value_list.append([index, value])
        if len( os_value_list) >=3:
            x_values = [item[0] for item in os_value_list]
            y_values = [item[1] for item in os_value_list]
            coefficients = np.polyfit(x_values, y_values, 2)  # Fit a quadratic polynomial, if linear,a will be 0
            a = coefficients[0]
            b = coefficients[1]
            c = coefficients[2]
            return {'name':v_name, 'rule_name': '2nd_poly','coefficients': {'a': a,'b': b,'c': c}}
        else:
            return {'name':v_name, 'rule_name': '2nd_poly','coefficients': {'a': None,'b': None,'c': None}}

    def get_coef_linear(self, v_name, valuelist):
        os_value_list = []
        for index, value in enumerate(valuelist):
            if value is not None:
                os_value_list.append([index, value])
        if len( os_value_list) >=2:
            x_values = [item[0] for item in os_value_list]
            y_values = [item[1] for item in os_value_list]
            coefficients = np.polyfit(x_values, y_values, 1)  # Fit a quadratic polynomial, if linear,a will be 0
            a = coefficients[0]
            b = coefficients[1]
            return {'name':v_name,'rule_name': 'linear','coefficients': {'a': a,'b': b}}
        else:
            return {'name':v_name, 'rule_name': '2nd_poly','coefficients': {'a': None,'b': None}}

    def get_static(self, v_name, valuelist):
        return {'name':v_name,'rule_name': 'static','coefficients': {'a': None}}
    
    def get_undetermined(self, v_name, valuelist):
        return {'name':v_name,'rule_name': 'undetermined','coefficients': {'a': None}} 
    
    
    
    def get_rule_dict(self,domains):
        rule_dict = {}
        for v_name in domains:
            variable_dict  = domains[v_name]
            dict_list = str(variable_dict).split(';')
            v_rule_type = dict_list[-1].split(':')
            type_name = str(v_rule_type[1])[:-2].strip()
            rule_dict[v_name] = type_name
        return rule_dict       

    def update_state(self, succ_state, path, problem):
        domains = problem.domains
        rule_dict = self.get_rule_dict(domains)
        #keyword = self.checkV()
        x = len(path)
        updated_state = succ_state
        for keyword in succ_state:
            v_name = keyword.split('-')[0]
            v_rult_type = str(rule_dict[v_name])
            if succ_state is not None and keyword in succ_state and v_rult_type =='linear':
                updated_value = self.updatelinear(x)    ##########change model here
                updated_state[keyword] = updated_value
                #print(x,updated_value)
                
            if succ_state is not None and keyword in succ_state and v_rult_type =='2nd_poly':
                updated_value = self.update2Poly(x)    ##########change model here
                updated_state[keyword] = updated_value
                #print(x,updated_value)

        if self.is_value_in_domain(updated_state,domains):
            return updated_state
        else:
            return None
    def is_value_in_domain(self, state,domains):
        for var_name, value in state.items():
            clean_var_name = var_name.split('-')[0]
            if clean_var_name in domains:
                domain = domains[clean_var_name].d_values
                if value not in domain:
                    return False
        return True 


    def updateRuleByLearn(self, new_os, new_p_index,rule_dict,v_name):
        keyword = v_name #peeking-a
        observed_list = []
        v_name = v_name.split('-')[0] #peeking
        v_rult_type = str(rule_dict[v_name])
        #print(v_rult_type)
        #print(v_name,v_rult_type)

        for i in range(len(new_os)-1, -1, -1):
            if keyword in new_os[i]:
                value = new_os[i][keyword]
                if value is not None:
                    observed_list.append([i, value])


        #y = ax^2+bx+c;observed_list and len(observed_list) > 2:  # Check if there are at least 3 points for quadratic fit 
        if observed_list and len(observed_list) >=3 and v_rult_type =='2nd_poly':
            x_values = [item[0] for item in observed_list]
            y_values = [item[1] for item in observed_list]
            #print(x_values,y_values)

            coefficients = np.polyfit(x_values, y_values, 2)  # Fit a quadratic polynomial, if linear,a will be 0
            a = coefficients[0]
            b = coefficients[1]
            c = coefficients[2]
            #print(a,b,c) miaccuracy problem here

            x = new_p_index
            result = round(a * x**2 + b * x + c)
            #if a < 0.0001:
                #return {'rule_name': 'linear','coefficients': {'a': a,'b': b}},result
            #else:
                
            return {'name':keyword,'rule_name': '2nd_poly','coefficients': {'a': a,'b': b,'c': c}},result
        #y = ax+b;observed_list and len(observed_list) > 1: #can update 
        elif observed_list and len(observed_list) >=2 and v_rult_type =='linear':
            x_values = [item[0] for item in observed_list]
            y_values = [item[1] for item in observed_list]
        
            coefficients = np.polyfit(x_values, y_values, 1)    
            a = coefficients[0]
            b = coefficients[1]

            x = new_p_index
            result = round(a * x + b)
            return {'name':keyword,'rule_name': 'linear','coefficients': {'a': round(a),'b': round(b)}},result
        
        elif observed_list and len(observed_list) >=1 and v_rult_type =='static':
            result = observed_list[-1] if observed_list else None
            return {'name':keyword,'rule_name': 'static','coefficients': {'a': 1}},result
        
        elif observed_list and v_rult_type =='undetermined':
            result = "?"
            return {'name':keyword,'rule_name': 'undetermined','coefficients': {}},result
        else: #can not update
            for o in reversed(new_os):
                if keyword in o:
                    if o[keyword] is not None:
                        memoryvalue = o[keyword]
                        break 
                    else:
                        memoryvalue = None
                else:
                    memoryvalue = None
            result = memoryvalue 
            return {'name':keyword,'rule_name': v_rult_type,'coefficients': {}},result
    
    
    def updatelinear(self,x):
        return x + 2    

    def update2Poly(self,x):
        return x**2 + 1
           
def get_valid_states(agents,states,problem,ep_goals,obj_name):
    valid_states = []
    for state in states:
        current_time = datetime.now()
        perspectives_dict,epistemic_dict = problem.epistemic_model.epistemicGoalsHandler(ep_goals,"",[(state,"")])
        
        problem.epistemic_calls += 1
        problem.epistemic_call_time += datetime.now() - current_time
        goal_dict = {}
        # remain_goal_number = list(goal_dict.values()).count(False)
        
        for ep_str,value in ep_goals:
            if epistemic_dict[ep_str].value == value:
                goal_dict[ep_str] = True
            else:
                goal_dict[ep_str] = False
        if list(goal_dict.values()).count(False) ==0:
            filtered_state = _variableFilter(state,obj_name)
            if filtered_state not in valid_states:
                valid_states.append(filtered_state)
    return valid_states
        # if epistemic_dict[ep_str].value == value:
        #     print(state)
        #     filtered_state = self._variableFilter(state,obj_name)
        #     if filtered_state not in ep_state_dict[ep_str]['states']:
        #         ep_state_dict[ep_str]['states'].append(filtered_state)
    # for ep_str,value in ep_goals:
        # ep_value = ep_str.split(v_name)[1][3:-2]
        # ep_front = ep_str.split(v_name)[0]
        # ep_header = format_ep(ep_value,value)
        
        # variable_dict = get_relative_variables(agents,(obj_index,obj_name,obj_value),problem)
        # states = _all_states(variable_dict)

        # ep_state_dict.update({ep_str: {'states':list(),'obj_value':obj_value}})
        
        
        # for state in states:
        #     current_time = datetime.now()
        #     perspectives_dict,epistemic_dict = problem.epistemic_model.epistemicGoalsHandler([(ep_str,value)],"",[(state,"")])    
        #     problem.epistemic_calls += 1
        #     problem.epistemic_call_time += datetime.now() - current_time

        #     if epistemic_dict[ep_str].value == value:

        #         filtered_state = self._variableFilter(state)
        #         if filtered_state not in ep_state_dict[ep_str]['states']:
        #             ep_state_dict[ep_str]['states'].append(filtered_state)
        

    # for ep_str, states in ep_state_dict.items():

    #     for state in states:

    print(ep_state_dict)
    # land_marks = []
    for key1 in ep_state_dict.keys():
        for key2 in ep_state_dict.keys():
            if not key1 == key2:
                item1 = ep_state_dict[key1]
                item2 = ep_state_dict[key2]
                
                if item1['obj_value'] == item2["obj_value"]:
                    # there is not constrain since the values are same
                    # we might want to get intersection
                    pass
                else:
                    for state in item1['states']:
                        if state not in item2['states']:
                            if state not in land_marks[v_name]:
                                land_marks[v_name].append(state)
                    for state in item2['states']:
                        if state not in item1['states']:
                            if state not in land_marks[v_name]:
                                land_marks[v_name].append(state)
    print(land_marks)
    return land_marks
        
def _variableFilter(state,obj_name):
    new_state = {}
    for v_name,value in state.items():
        flag = True
        if v_name == obj_name:
            flag = False
        else:
            for filter_str in FILTER_VARIABLES:
                if filter_str in v_name:
                    flag = False
                    break
        if flag:
            new_state.update({v_name:value})
    return new_state
            
def handlerObject(ep_str,problem):
    obj_index = ""
    variable_reg_str = "\([\w|'|\"|,|-]*\)"
    variable_list = re.findall(variable_reg_str,ep_str)
    for variable_pair_str in variable_list:
        var_temp_list = variable_pair_str[1:-1].split(",")
        obj_name = var_temp_list[0][1:-1]
        obj_value = var_temp_list[1][1:-1]
        obj = problem.variables[obj_name]
        obj_index = obj.v_parent
        obj_domains = problem.domains[obj.v_domain_name].d_values
    return obj_index,obj_domains,obj_name,obj_value
            
      
def get_agent_names(ep_str):
    # print(ep_str)
    agent_set = set()
    
    agent_reg_str =  "[b|k|s] (\[[\w|,]*\])* "
    agent_list_list = re.findall(agent_reg_str,ep_str)
    for agent_list in agent_list_list:
        for agent_id in agent_list[1:-1].split(","):
            agent_set.add(agent_id)
    return agent_set
      
      
                
# def get_entities_names(ep_str,problem):

#     agent_set = set()
#     object_set = set()
    
#     agent_reg_str =  "[b|k|s] (\[[\w|,]*\])* "
#     agent_list_list = re.findall(agent_reg_str,ep_str)
#     for agent_list in agent_list_list:
#         for agent_id in agent_list[1:-1].split(","):
#             agent_set.add(agent_id)
    
#     variable_reg_str = "\([\w|'|\"|,|-]*\)"
#     variable_list = re.findall(variable_reg_str,ep_str)
#     for variable_pair_str in variable_list:
#         variable_name = variable_pair_str[1:-1].split(",")[0][1:-1]
#         object_set.add(problem.variables[variable_name].v_parent)

#     return agent_set,object_set,value
     
def get_relative_variables(agents,object_tuple,problem):
    obj_index,obj_name,obj_value = object_tuple
    variable_dict = {}
    domains = problem.domains
    for v_name, variable in problem.variables.items():
        index = variable.v_parent
        if index in agents and v_name[:-len(index)] in AGENT_VARIABLES:
            variable_dict.update({v_name:domains[variable.v_domain_name].d_values})
        elif index == obj_index and v_name[:-len(index)] in OBJECT_VARIABLES:
            if v_name == obj_name:
                variable_dict.update({v_name:obj_value})
            else:
                variable_dict.update({v_name:domains[variable.v_domain_name].d_values})
    return variable_dict

def _all_states(state_dict):
    states = []
    if state_dict == {}:
        return [{}]    
    key,values = state_dict.popitem()
    for temp_state in _all_states(state_dict):
        for value in values:
            new_state = temp_state.copy()
            new_state.update({key:value})
            states.append(new_state)
    return states

def format_ep(ep_value, value):
    if value == 0:
        ep_value = reverse_ep_value(ep_value)
    
    # return f'{value}{SPLIT_KEY_WORD}{ep_value}'
    return (value,ep_value)
        
        
def reverse_ep_value(ep_value):
    if ep_value == 't':
        return 'f'
    elif ep_value == 'f':
        return 't'
    else:
        return ep_value
    
