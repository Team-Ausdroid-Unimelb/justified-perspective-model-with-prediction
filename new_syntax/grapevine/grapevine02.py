import logging 
import typing
from util import Function,FunctionSchema,Entity,EntityType,setup_logger, RULE_TYPE
from datetime import datetime
from util import RULE_TYPE, special_value
from collections import Counter
import math

LOGGER_NAME = "grapevine"
LOGGER_LEVEL = logging.INFO
# LOGGER_LEVEL = logging.DEBUG
 
# declare common variables
common_constants = {

}

class ExternalFunction:
    logger = None
    
    def __init__(self, handlers):
        self.logger = setup_logger(LOGGER_NAME,handlers,logger_level=LOGGER_LEVEL) 
    
    def checkVisibility(self,state,agent_index,var_name,entities:typing.Dict[str,Entity],
                        functions:typing.Dict[str,Function],
                        function_schemas:typing.Dict[str,FunctionSchema]):
        if not agent_index in entities.keys():
            raise ValueError(f"agent_index [{agent_index}] not found in entities")
        if not entities[agent_index].enetity_type == EntityType.AGENT:
            raise ValueError(f"agent_index [{agent_index}] is not an agent")
        if var_name not in functions.keys():
            raise ValueError(f"var_name [{var_name}] not found in functions")
        
        function = functions[var_name]
        function_schemas_name = function.function_schema_name
        target_list = function.entity_index_list
        
        
        if 'agent_loc'  == function_schemas_name:
            # it means this is a location variable
            # since there is only two rooms in the grapevine domain
            # agent will know others location if they are in the same room
            # agent will also know others location if they are not in the same room
            return True
        elif 'shared_loc'  == function_schemas_name:
            # it means this is a location variable
            # agent will know the secret is been shared if they are in the same room where the secret shared
            if state[var_name] == 0:
                return True
            return state[var_name] == state[f'agent_loc {agent_index}']
        elif 'own'  == function_schemas_name:
            # all agents sees ownship of secrets
            return True
        elif 'sharing'  == function_schemas_name:
            # this function is to make sure the sharing secret only last one state
            # does not matter
            return True
        elif 'secret_value'  == function_schemas_name or 'secret_truth_value'  == function_schemas_name:
            # it depends on whether agent sees that secret been shared
            if not len(target_list) == 1:
                raise ValueError(f"secret_value function should have only one entity index")
            try:
                # shared_loc = state[f'shared_loc {target_list[0]}']
                # agent_loc = state[f'agent_loc {agent_index}']
                if state[f'own {agent_index} {target_list[0]}'] == 1:
                    # if this secret is own by the agent
                    return True
                # elif shared_loc == agent_loc:
                #     return True

                else:
                    return False
            except KeyError as e:
                self.logger.debug(e)
                self.logger.debug("state: %s",state)
                return False
        elif 'secret_lyging_value'  == function_schemas_name or 'agent_lyging_value'  == function_schemas_name:
            # it depends on whether agent sees that secret been shared
            if not len(target_list) == 1:
                raise ValueError(f"secret_lyging_value function should have only one entity index")
            try:
                if state[f'own {agent_index} {target_list[0]}'] == 1:
                    # if this secret is own by the agent
                    return True
                shared_loc = state[f'shared_loc {target_list[0]}']
                agent_loc = state[f'agent_loc {agent_index}']
                return shared_loc == agent_loc
            except KeyError as e:
                self.logger.debug(e)
                self.logger.debug("state: %s",state)
                return False
        elif 'shared_value'  == function_schemas_name:
            # it depends on whether agent sees that secret been shared
            if not len(target_list) == 1:
                raise ValueError(f"shared_value function should have only one entity index")
            try:
                shared_loc = state[f'shared_loc {target_list[0]}']
                agent_loc = state[f'agent_loc {agent_index}']
                return shared_loc == agent_loc
            except KeyError as e:
                self.logger.debug(e)
                self.logger.debug("state: %s",state)
                return False
        else:
            raise ValueError(f"function_schemas_name [{function_schemas_name}] not found")

    def update1Poly(self,x,paramiters):
        
        a = int(paramiters[0])
        b = int(paramiters[1])
        return a*x + b
    
    def update2Poly(self,x,paramiters):
        a = int(paramiters[0])
        b = int(paramiters[1])
        c = int(paramiters[2])
        return a*x**2 + b*x + c
    

    def update_state(self, succ_state, path, problem):
        #ranges = problem.value_ranges
        #print(ranges)
        # rule_dict = {}
        # for v_name in domains:
        #     print(domains[v_name].rule_type)
        #     variable_dict  = domains[v_name]
        #     dict_list = str(variable_dict).split(';')
        #     v_rule_type = dict_list[-1].split(':')
        #     type_name = str(v_rule_type[1])[:-2].strip()
        #     rule_dict[v_name] = type_name
            
        x = len(path)-1
        
        updated_state = succ_state
        for v_name in succ_state:
            v_rule_type = problem.rules[v_name].rule_type
            paramiters = problem.rules[v_name].rule_content.strip('[]').split(',')
            if succ_state is not None and v_name in succ_state and v_rule_type == RULE_TYPE.POLY_1ST:

                updated_value = self.update1Poly(x,paramiters)    ##########change model here
                if self.is_value_in_domain(v_name,updated_value,problem):
                    updated_state[v_name] = updated_value
                else:
                    return None
                #updated_state[v_name] = updated_value
                
                
            if succ_state is not None and v_name in succ_state and v_rule_type ==RULE_TYPE.POLY_2ND:
                updated_value = self.update2Poly(x,paramiters)    ##########change model here
                #updated_state[v_name] = updated_value
                if self.is_value_in_domain(v_name,updated_value,problem):
                    updated_state[v_name] = updated_value
                else:
                    return None
                #print(x,updated_value)
        
        return updated_state
        # if self.is_value_in_domain(v_name,updated_value,problem):
        #     return updated_state
        # else:
        #     return None

    def is_value_in_domain(self, var_name,value,problem):
        function_schema_name = problem.functions[var_name].function_schema_name
        ranges = problem.function_schemas[function_schema_name]
        domain = str(ranges).split(":")[1].split("]")[1].split(")")[0]#.split()[1]#[:-1]
        #print(domain)
        if domain.startswith('['):
            domain = domain[1][:-1][1:-1].split(",")
            if value not in list(domain):  
                return False
        elif domain.startswith(' ('):
            domain = domain[2:].split(",")
            value = int(value)
            if value < int(domain[0]) or value > int(domain[1]):
                return False
        return True
    
    def get_coef_poly_1st(self, v_name, valuelist,rules):  ##find dominant coefficients method
        #self.segment_count += math.factorial(len(valuelist))
        coefficients_counter = Counter()
        coefficients_known_list = rules[v_name].rule_known_coef.strip('[]').split(',')
        known_coefficients={}

        for idx, coeff in enumerate(coefficients_known_list[::-1]):
            if coeff != '':
                coeff = float(coeff)
                known_coefficients[idx] = coeff
            else:
                known_coefficients[idx] = None

        os_value_list = []
        os_value_list = []
        for index, value in enumerate(valuelist):
            if value is not None and value != special_value.UNSEEN and value != special_value.HAVENT_SEEN:
                os_value_list.append((index, value))

        
        for i in range(len(os_value_list)):
            for j in range(i + 1, len(os_value_list)):
                x1, y1 = os_value_list[i]
                x2, y2 = os_value_list[j]
                if x1 == x2:
                    continue
                a = (y2 - y1) / (x2 - x1)
                b = y1 - a * x1

                coefficients_counter[(round(a, 6), round(b, 6))] += 1
        if not coefficients_counter:
            return {'name': v_name, 'rule_name': '1st_poly', 'coefficients': {}}
        most_common_coefficients = coefficients_counter.most_common(1)[0][0]

        coefficients_dict = {
            'a': most_common_coefficients[0],
            'b': most_common_coefficients[1]
        }

        return {
            'name': v_name,
            'rule_name': '1st_poly',
            'coefficients': coefficients_dict
        }
    
    def get_predict_1st_poly(self, i,rule,value):  ##find dominant coefficients method
        # print("hererer",i,rule,value)
        a = rule['coefficients'].get('a')
        b = rule['coefficients'].get('b')
        if a is None or b is None:
            result = self.get_predict_static(i,rule,value)
        else:
            result = round(a * i + b)
        return result
    
    def get_predict_static(self, i,rule,value):
        result = special_value.HAVENT_SEEN
        for j in range(i - 1, -1, -1):
            if value[j] is not None and value[j] != special_value.UNSEEN and value[j] != special_value.HAVENT_SEEN:
                result = value[j] 
                return value[j] 
            
        for j in range(i + 1, len(value)):
            if value[j] is not None and value[j] != special_value.UNSEEN and value[j] != special_value.HAVENT_SEEN:
                result = value[j] 
                return value[j]
        return result
    # # customise action filters
    # # to filter out the irrelevant actions
    # def filterActionNames(self,problem,action_dict):
    #     # self.logger.debug(action_dict.keys())
    #     action_name_list = []
    #     relevant_variable_parent_index = []
    #     relevant_agent_index = []
        

    #     for key,ep_obj in problem.goals.epistemic_dict.items():
    #         eq_str = ep_obj.query
    #         match = re.search("[edc]?[ksb] \[[0-9a-z_,]*\] ",eq_str)
    #         while not match == None:
    #             eq_list = eq_str.split(" ")
    #             relevant_agent_index += eq_list[1][1:-1].split(",")
    #             eq_str = eq_str[len(eq_list[0])+len(eq_list[1])+2:]
    #             match = re.search("[edc]?[ksb] \[[0-9a-z_,]*\] ",eq_str)
                
    #         # variable_name,value =self.extractVariable(eq_str)
    #         variable_name = ep_obj.variable_name
    #         relevant_variable_parent_index.append(problem.variables[variable_name].v_parent)
    #         self.logger.debug("variable_name[%s] , problem.variables[variable_name].v_parent [%s]",variable_name,problem.variables[variable_name].v_parent)




    #     for name,action in action_dict.items():
    #         self.logger.debug('action_name: [%s]',name) 
    #         if "sharing_" in name:
    #             if name.split("-")[2] in relevant_variable_parent_index:
    #                 action_name_list.append(name)
    #         elif "sharing" in name or "lying" in name:
    #             if name.split("-")[1] in relevant_variable_parent_index:
    #                 action_name_list.append(name)
    #         elif "move" in name:
    #             self.logger.debug('agent_in: [%s]',name.split("-")[1]) 
    #             if name.split("-")[1] in relevant_agent_index:
    #                 action_name_list.append(name) 
    #         else:
    #             action_name_list.append(name)
    #     if logging.getLogger().isEnabledFor(logging.DEBUG):
    #         self.logger.debug('action names after filter: [%s]',action_name_list)   
    #     return action_name_list
    #     return action_dict.keys()

    

#     def generate_constrain_dict(self,problem,group_eg_dict):

#         self.logger.debug('')
#         self.logger.debug('generate_constrain_dict')
#         self.logger.debug('group_eg_dict [%s]',group_eg_dict)
#         land_marks = dict()
#         for v_name, ep_goals in group_eg_dict.items():
#             agents = set()
#             land_marks[v_name] = []
#             for ep_str,value in ep_goals:
#                 agents_temp = get_agent_names(ep_str)
#                 agents.update(agents_temp)
#             obj_index,obj_domains,obj_name,obj_value = handlerObject(ep_str,problem)

#             variable_dict = get_relative_variables(agents,(obj_index,obj_name,obj_domains),problem)
#             states = _all_states(variable_dict)
#             valid_states = get_valid_states(agents,states,problem,ep_goals,obj_name)
#             if not valid_states == []:

#                 land_marks[v_name]={'landmark_type': [[list(range(len(ep_goals)))]],'ep_list': ep_goals,'landmarks': valid_states}
#             else:
#                 # cannot achieve group goal in one state
#                 ep_state_dict = {}
#                 for ep_str,value in ep_goals: 
#                     obj_index,obj_domains,obj_name,obj_value = handlerObject(ep_str,problem)
#                     variable_dict = get_relative_variables(agents,(obj_index,obj_name,[obj_value]),problem)
#                     states = _all_states(variable_dict)
#                     valid_states = get_valid_states(agents,states,problem,[(ep_str,value)],obj_name)
#                     ep_state_dict.update({ep_str: {'states':valid_states,'obj_value':obj_value}})
#                     for key1 in ep_state_dict.keys():
#                         for key2 in ep_state_dict.keys():
#                             if not key1 == key2:
#                                 item1 = ep_state_dict[key1]
#                                 item2 = ep_state_dict[key2]
                                
#                                 if item1['obj_value'] == item2["obj_value"]:
#                                     # there is not constrain since the values are same
#                                     # we might want to get intersection
#                                     pass
#                                 else:
#                                     for state in item1['states']:
#                                         if state not in item2['states']:
#                                             if state not in land_marks[v_name]:
#                                                 land_marks[v_name].append(state)
#                                     for state in item2['states']:
#                                         if state not in item1['states']:
#                                             if state not in land_marks[v_name]:
#                                                 land_marks[v_name].append(state)
#         return land_marks
            
                
# def get_valid_states(agents,states,problem,ep_goals,obj_name):
#     valid_states = []
#     for state in states:
#         current_time = datetime.now()
#         perspectives_dict,epistemic_dict = problem.epistemic_model.epistemicGoalsHandler(ep_goals,"",[(state,"")])
        
#         problem.epistemic_calls += 1
#         problem.epistemic_call_time += datetime.now() - current_time
#         goal_dict = {}
#         # remain_goal_number = list(goal_dict.values()).count(False)
        
#         for ep_str,value in ep_goals:
#             if epistemic_dict[ep_str].value == value:
#                 goal_dict[ep_str] = True
#             else:
#                 goal_dict[ep_str] = False
#         if list(goal_dict.values()).count(False) ==0:
#             filtered_state = _variableFilter(state,obj_name)
#             if filtered_state not in valid_states:
#                 valid_states.append(filtered_state)
#     return valid_states
        # if epistemic_dict[ep_str].value == value:
        #     self.logger.debug(state)
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

#     #     for state in states:

#     self.logger.debug(ep_state_dict)
#     # land_marks = []
#     for key1 in ep_state_dict.keys():
#         for key2 in ep_state_dict.keys():
#             if not key1 == key2:
#                 item1 = ep_state_dict[key1]
#                 item2 = ep_state_dict[key2]
                
#                 if item1['obj_value'] == item2["obj_value"]:
#                     # there is not constrain since the values are same
#                     # we might want to get intersection
#                     pass
#                 else:
#                     for state in item1['states']:
#                         if state not in item2['states']:
#                             if state not in land_marks[v_name]:
#                                 land_marks[v_name].append(state)
#                     for state in item2['states']:
#                         if state not in item1['states']:
#                             if state not in land_marks[v_name]:
#                                 land_marks[v_name].append(state)
#     self.logger.debug(land_marks)
#     return land_marks
        
# def _variableFilter(state,obj_name):
#     new_state = {}
#     for v_name,value in state.items():
#         flag = True
#         if v_name == obj_name:
#             flag = False
#         else:
#             for filter_str in FILTER_VARIABLES:
#                 if filter_str in v_name:
#                     flag = False
#                     break
#         if flag:
#             new_state.update({v_name:value})
#     return new_state
            
# def handlerObject(ep_str,problem):
#     obj_index = ""
#     variable_reg_str = "\([\w|'|\"|,|-]*\)"
#     variable_list = re.findall(variable_reg_str,ep_str)
#     for variable_pair_str in variable_list:
#         var_temp_list = variable_pair_str[1:-1].split(",")
#         obj_name = var_temp_list[0][1:-1]
#         obj_value = var_temp_list[1][1:-1]
#         obj = problem.variables[obj_name]
#         obj_index = obj.v_parent
#         obj_domains = problem.domains[obj.v_domain_name].d_values
#     return obj_index,obj_domains,obj_name,obj_value
            
      
# def get_agent_names(ep_str):
#     # self.logger.debug(ep_str)
#     agent_set = set()
    
#     agent_reg_str =  "[b|k|s] (\[[\w|,]*\])* "
#     agent_list_list = re.findall(agent_reg_str,ep_str)
#     for agent_list in agent_list_list:
#         for agent_id in agent_list[1:-1].split(","):
#             agent_set.add(agent_id)
#     return agent_set
      
      
                
# # def get_entities_names(ep_str,problem):

# #     agent_set = set()
# #     object_set = set()
    
# #     agent_reg_str =  "[b|k|s] (\[[\w|,]*\])* "
# #     agent_list_list = re.findall(agent_reg_str,ep_str)
# #     for agent_list in agent_list_list:
# #         for agent_id in agent_list[1:-1].split(","):
# #             agent_set.add(agent_id)
    
# #     variable_reg_str = "\([\w|'|\"|,|-]*\)"
# #     variable_list = re.findall(variable_reg_str,ep_str)
# #     for variable_pair_str in variable_list:
# #         variable_name = variable_pair_str[1:-1].split(",")[0][1:-1]
# #         object_set.add(problem.variables[variable_name].v_parent)

# #     return agent_set,object_set,value
     
# def get_relative_variables(agents,object_tuple,problem):
#     obj_index,obj_name,obj_value = object_tuple
#     variable_dict = {}
#     domains = problem.domains
#     for v_name, variable in problem.variables.items():
#         index = variable.v_parent
#         if index in agents and v_name[:-len(index)] in AGENT_VARIABLES:
#             variable_dict.update({v_name:domains[variable.v_domain_name].d_values})
#         elif index == obj_index and v_name[:-len(index)] in OBJECT_VARIABLES:
#             if v_name == obj_name:
#                 variable_dict.update({v_name:obj_value})
#             else:
#                 variable_dict.update({v_name:domains[variable.v_domain_name].d_values})
#     return variable_dict

# def _all_states(state_dict):
#     states = []
#     if state_dict == {}:
#         return [{}]    
#     key,values = state_dict.popitem()
#     for temp_state in _all_states(state_dict):
#         for value in values:
#             new_state = temp_state.copy()
#             new_state.update({key:value})
#             states.append(new_state)
#     return states

# def format_ep(ep_value, value):
#     if value == 0:
#         ep_value = reverse_ep_value(ep_value)
    
#     # return f'{value}{SPLIT_KEY_WORD}{ep_value}'
#     return (value,ep_value)
        
        
# def reverse_ep_value(ep_value):
#     if ep_value == 't':
#         return 'f'
#     elif ep_value == 'f':
#         return 't'
#     else:
#         return ep_value
    