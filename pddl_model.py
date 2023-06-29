from datetime import datetime, timedelta
import logging
import os
import copy
import re
from typing import List
from epistemic_model import EpistemicModel


LOGGER_NAME = "pddl_model"
LOG_LEVEL = logging.INFO
# LOG_LEVEL = logging.DEBUG

from util import setup_logger,PDDL_TERNARY
# logger = setup_logger(LOGGER_NAME,instance_handler,logging.INFO) 
# from numpy.core.defchararray import _join_dispatcher
# from numpy.lib.function_base import extract
# from numpy.lib.shape_base import _put_along_axis_dispatcher
# from numpy.ma.core import common_fill_value
# import bbl
# import coin as external

# # 
# class VALUE(Enum):
#     UNSEEN = None
#     SEEN = 9999


# Class of the problem
class Problem:
    initial_state = {}
    actions = {} 
    entities = {} # agent indicators, should be unique
    variables = {} #variable
    domains = {}
    initial_state = {}
    goal_states = {}
    external = None
    epistemic_calls = 0
    epistemic_call_time = timedelta(0)
    epistemic_model = None
    logger = None

    def __init__(self, domains,i_state,g_states,agent_index,obj_index,variables,actions, external=None,logger_handler=None):
        self.initial_state = {}
        self.actions = {} 
        self.entities = {} # agent indicators, should be unique
        self.variables = {} #variable
        self.domains = {}
        self.initial_state = {}
        self.goal_states = {}
        self.epistemic_calls = 0
        self.epistemic_call_time = timedelta(0)
        self.logger = None
        self.logger = setup_logger(LOGGER_NAME,logger_handler,LOG_LEVEL)
        self.logger.info("initialize entities")
        self.entities = {}
        for i in agent_index:
            e_temp = Entity(i,E_TYPE.AGENT)
            self.entities.update({i:e_temp})
        for i in obj_index:
            e_temp = Entity(i,E_TYPE.OBJECT)
            self.entities.update({i:e_temp})        
        self.logger.debug(self.entities)
        
        self.logger.debug("initialize variable")
        self.variables = {}
        
        for d_name,targets in variables.items():
            # self.logger.debug(self.variables)
            suffix_list = self._generateVariables(targets)
            self.logger.debug(suffix_list)
            for suffix in suffix_list:
                var_name = f"{d_name}{suffix}"
                v_parent = suffix.split('-')[1]
                v_temp = Variable(var_name,d_name,v_parent)
                self.variables.update({var_name:v_temp})
        self.logger.debug(self.variables)
            
        # grounding all actions or do not ground any actions?    
        self.logger.debug("initialize actions")
        self.logger.debug(actions )
        for a_name, parts in actions.items():
            
            p = [ (i,eTypeConvert(self.logger,t))for i,t in parts['parameters']]
            a_temp = Action(a_name, p,parts['precondition'], parts['effect'])
            self.actions.update({a_name:a_temp})
        self.logger.debug(self.actions)
        
        self.logger.debug("initialize domains")
        self.domains = {}
        self.logger.debug(f'input domains: {domains}')
        for d_name in domains.keys():
            values = domains[d_name]['values']
            d_type = dTypeConvert(self.logger,domains[d_name]['basic_type'])
            if d_type == D_TYPE.INTEGER:
                bound = domains[d_name]['values']
                values = list(range(bound[0],bound[1]+1))

            domain_temp = Domain(d_name,values,d_name=='agent',d_type)
            self.domains.update({d_name:domain_temp})
        self.logger.debug(self.domains)
        
        self.goal_states = g_states
        self.logger.info(self.goal_states)
        self.initial_state = i_state
        self.logger.debug(self.initial_state)
        self.external = external
        self.epistemic_model = EpistemicModel(logger_handler,self.entities,self.variables,external)
    
        
    def isGoal(self,state,path):
        is_goal=True
        goal_dict = {}
        self.logger.debug(f"checking goal for state: {state} with path: {path}")
        actions = [ a  for s,a in path]
        actions = actions[1:]
        self.logger.debug(f'plan is: {actions}')
        self.logger.debug(f'ontic_goal: {self.goal_states["ontic_g"]}')
        for k,v in self.goal_states["ontic_g"]:
            if not state[k] == v:
                is_goal = False
                goal_dict.update({k+" "+str(v):False})
            else:
                goal_dict.update({k+" "+str(v):True})
            
        # adding epistemic checker here
        self.logger.debug(f'epistemic_goal: {self.goal_states["epistemic_g"]}')
        current_time = datetime.now()
        self.epistemic_calls +=1
        perspectives_dict,epistemic_dict = self.epistemic_model.epistemicGoalsHandler(self.goal_states["epistemic_g"],"",path)
        self.epistemic_call_time += datetime.now() - current_time
        
        for k,v in self.goal_states["epistemic_g"]:
            if not epistemic_dict[k].value == v:
                is_goal = False
                goal_dict.update({k+" "+str(v):False})
            else:
                goal_dict.update({k+" "+str(v):True})
        self.logger.debug(f"goal {self.goal_states['epistemic_g']}")
        self.logger.debug(f"epistemic_dict {epistemic_dict}")
        self.logger.debug(f"perspectives_dict {perspectives_dict}")
        return is_goal,perspectives_dict,epistemic_dict,goal_dict
    
    # def isGoalP(self,state,path):
    #     is_goal=True
    #     # let's keep iw1 version and extend it later
    #     epistemic_items_set = {}
    #     p_dict = {}
    #     self.logger.debug(f"checking goal for state: {state} with path: {path}")
    #     actions = [ a  for s,a in path]
    #     actions = actions[1:]
    #     self.logger.debug(f'plan is: {actions}')
    #     self.logger.debug(f'ontic_goal: {self.goal_states["ontic_g"]}')
    #     for k,i in self.goal_states["ontic_g"].items():
    #         if not state[k] == i:
    #             is_goal = False
    #             break
            
    #     # adding epistemic checker here
    #     self.logger.debug(f'epistemic_goal: {self.goal_states["epistemic_g"]}')
    #     for eq,value in self.goal_states["epistemic_g"]:
    #         self.epistemic_calls +=1
    #         current_time = datetime.now()
    #         temp_e_v, temp_p_dict = self.epistemic_model.checkingEQstrP(self.external,eq,path,state,self.entities,self.variables)
    #         self.epistemic_call_time += datetime.now() - current_time
    #         if not temp_e_v == value:
    #             is_goal=False
    #         p_dict.update(temp_p_dict)
    #     return is_goal,p_dict    
    
    # def isGoal(self,state,path):
    #     self.logger.debug(f"checking goal for state: {state} with path: {path}")
    #     actions = [ a  for s,a in path]
    #     actions = actions[1:]
    #     self.logger.debug(f'plan is: {actions}')
    #     self.logger.debug(f'ontic_goal: {self.goal_states["ontic_g"]}')
    #     for k,i in self.goal_states["ontic_g"].items():
    #         if not state[k] == i:
    #             return False
            
    #     # adding epistemic checker here
    #     self.logger.debug(f'epistemic_goal: {self.goal_states["epistemic_g"]}')
    #     for eq,value in self.goal_states["epistemic_g"]:
    #        
    #         current_time = datetime.now()
    #         if not self.epistemic_model.checkingEQstr(self.external,eq,path,state,self.entities,self.variables) == value:
    #             self.epistemic_call_time += datetime.now() - current_time
    #             return False
    #         self.epistemic_call_time += datetime.now() - current_time
    #     return True
    
    
    def getAllActions(self,state,path):
        legal_actions = {}
        
        # get all type of actions
        for a_name, a in self.actions.items():
            # self.logger.debug(f'action: {a} ')
            
            
            # generate all possible combination parameters for each type of action
            # self.logger.debug(f'all params: {self._generateParams(a.a_parameters)}')

            if a.a_parameters == []:
                a_temp_name = a_name
                a_temp_parameters = copy.deepcopy(a.a_parameters)
                a_temp_precondition = copy.deepcopy(a.a_precondition)
                a_temp_effects = copy.deepcopy(a.a_effects)
                # if self._checkPreconditions(state,a_temp_precondition,path):
                legal_actions.update({a_temp_name:Action(a_temp_name,a_temp_parameters,a_temp_precondition,a_temp_effects)})
                    # self.logger.debug(f'legal action after single precondition check: {legal_actions}') 
            else:
                for params in self._generateParams(a.a_parameters):
                    a_temp_name = a_name
                    a_temp_parameters = copy.deepcopy(a.a_parameters)
                    a_temp_precondition = copy.deepcopy(a.a_precondition)
                    a_temp_effects = copy.deepcopy(a.a_effects)
                    # self.logger.debug(f'works on params: {params}')
                    for i,v in params:
                        # a_temp_name = a_name
                        # a_temp_parameters = copy.deepcopy(a.a_parameters)
                        # a_temp_precondition = copy.deepcopy(a.a_precondition)
                        # a_temp_effects = copy.deepcopy(a.a_effects)
                        a_temp_name = a_temp_name + "-" + v
                        for j in range(len(a_temp_parameters)):
                            v_name, v_effects = a_temp_parameters[j]
                            v_name = v_name.replace(f'{i}',f'-{v}')
                            a_temp_parameters[j] = (v_name,v_effects)
                        
                        # update parameters in the ontic precondition
                        for j in range(len(a_temp_precondition['ontic_p'])):
                            v_name, v_effects = a_temp_precondition['ontic_p'][j]
                            v_name = v_name.replace(f'{i}',f'-{v}')
                            if type(v_effects) == str:
                                v_effects = v_effects.replace(f'{i}',f'-{v}')
                            a_temp_precondition['ontic_p'][j] = (v_name,v_effects)

                        # update parameters in the epistemic precondition
                        for j in range(len(a_temp_precondition['epistemic_p'])):
                            v_name, v_effects = a_temp_precondition['epistemic_p'][j]
                            v_name = v_name.replace(f'{i}',f'-{v}').replace('[-','[').replace(',-',',')
                            # precondition effect of epistemic is only going to be int
                            # v_effects = v_effects.replace(f'{i}',f'-{v}')
                            a_temp_precondition['epistemic_p'][j] = (v_name,v_effects)                            
                        
                        # update parameters in the effects
                        for j in range(len(a_temp_effects)):
                            v_name, v_effects = a_temp_effects[j]
                            v_name = v_name.replace(f'{i}',f'-{v}')
                            v_effects = v_effects.replace(f'{i}',f'-{v}')
                            a_temp_effects[j] = (v_name,v_effects)
                    # self.logger.debug(f'precondition after matching parameters: {a_temp_precondition}')
                    # self.logger.debug(f'effect after matching parameters: {a_temp_effects}')
                    
                    
                    # self.logger.debug(f'legal action before precondition check: {legal_actions}') 
                    # # TODO: adding precondition check
                    # if self._checkPreconditions(state,a_temp_precondition,path):
                    #     legal_actions.update({a_temp_name:Action(a_temp_name,a_temp_parameters,a_temp_precondition,a_temp_effects)})
                    # self.logger.debug(f'legal action after precondition check: {legal_actions}') 
                    legal_actions.update({a_temp_name:Action(a_temp_name,a_temp_parameters,a_temp_precondition,a_temp_effects)})
                    # self.logger.debug(f'legal action before precondition check: {legal_actions}') 
        self.logger.debug(f'legal actions: {legal_actions.keys()}') 
        return legal_actions

    def checkAllPreconditions(self,state,path,ontic_pre_dict,epistemic_pre_dict):
        self.logger.debug(f'function checkAllPreconditions')
        self.logger.debug(f'checking precondition for state: {state}')
        # preconditions = action.a_precondition

        pre_dict = {}
        flag_dict = {}
        
        # checking ontic preconditions
        self.logger.debug(f'checking all ontic preconditions')
        for action_name,ontic_pre in ontic_pre_dict.items():
            pre_dict[action_name] = {}
            flag_dict[action_name] = True
            self.logger.debug(f'checking ontic precondition {ontic_pre} for action {action_name}')
            for k,e in ontic_pre:
                try:
                    if k in state.keys():
                        if e in state.keys():
                            if not state[k] == state[e]:
                                flag_dict[action_name] = False
                                pre_dict[action_name].update({k+":"+str(e):False})
                            else:
                                pre_dict[action_name].update({k+":"+str(e):True})
                        elif not state[k] == e:
                            flag_dict[action_name] = False
                            pre_dict[action_name].update({k+":"+str(e):False})
                        else:
                            pre_dict[action_name].update({k+":"+str(e):True})
                    else:
                        self.logger.error(f'variable {k} not in state {state}')
                        
                except:
                    self.logger.error("Error when checking precondition: {}\n with state: {}")
                    
                    flag_dict[action_name] = False
        self.logger.debug(f'pre_dict {pre_dict}')
            
        # adding epistemic checker here
        # self.logger.debug(f'epistemic_pre: {preconditions["epistemic_p"]}')

        self.logger.debug(f'checking all epistemic preconditions')
        # get all ep_pre into one list
        temp_ep_list = []
        for action_name,ep_pre in epistemic_pre_dict.items():
            temp_ep_list += ep_pre
            
        self.logger.debug(f'epistemic preconditions list {temp_ep_list}')    
        current_time = datetime.now()
        self.epistemic_calls +=1
        perspectives_dict,epistemic_dict = self.epistemic_model.epistemicGoalsHandler(temp_ep_list,"",path)
        self.epistemic_call_time += datetime.now() - current_time

        ep_dict = {}
        for action_name,ep_pre in epistemic_pre_dict.items():
            ep_dict[action_name] = {}
            for k,v in ep_pre:
                if not epistemic_dict[k].value == v:
                    flag_dict[action_name] = False
                    pre_dict[action_name].update({k+":"+str(e):False})
                    # pre_flag = False
                    # pre_dict.update({k+" "+str(v):False})
                else:
                    pre_dict[action_name].update({k+":"+str(e):True})
        self.logger.debug(f"pre_dict: {pre_dict}")
        
        return flag_dict,perspectives_dict,epistemic_dict,pre_dict    


    def checkPreconditions(self,state,action,path):
        self.logger.debug(f'checking precondition for action: {action}')
        preconditions = action.a_precondition
        pre_flag = True
        pre_dict = {}
        # checking ontic preconditions
        # self.logger.debug(f'ontic_p: {preconditions["ontic_p"]}')
        for k,e in preconditions['ontic_p']:
            try:
                if e in state.keys():
                    e = state[e]
                if not state[k] == e:
                    pre_flag = False
                    pre_dict.update({k+" "+str(e):False})
                else:
                    pre_dict.update({k+" "+str(e):True})
            except:
                self.logger.error("Error when checking precondition: {}\n with state: {}")
                
                pre_flag = False

            
        # adding epistemic checker here
        # self.logger.debug(f'epistemic_pre: {preconditions["epistemic_p"]}')
        current_time = datetime.now()
        self.epistemic_calls +=1
        perspectives_dict,epistemic_dict = self.epistemic_model.epistemicGoalsHandler(preconditions["epistemic_p"],"",path)
        self.epistemic_call_time += datetime.now() - current_time
        for k,v in preconditions["epistemic_p"]:

            if not epistemic_dict[k].value == v:
                pre_flag = False
                pre_dict.update({k+" "+str(v):False})
            else:
                pre_dict.update({k+" "+str(v):True})

        self.logger.debug(f"pre_dict: {pre_dict}")
        
        return pre_flag,perspectives_dict,epistemic_dict,pre_dict    

    # def checkPreconditionsN(self,state,action,path):
    #     # self.logger.debug(f'checking precondition for action: {action}')
    #     preconditions = action.a_precondition
    #     pre_flag = True
    #     epistemic_items_set = {}
    #     # checking ontic preconditions
    #     for v,e in preconditions['ontic_p']:
    #         try:
    #             if e in state:
    #                 if not state[v] == state[e]:  
    #                     pre_flag = False
    #                     break
    #             else:
    #                 if not state[v] == e:  
    #                     pre_flag = False
    #                     break
    #         except:
    #             self.logger.error("Error when checking precondition: {}\n with state: {}")
                
    #             pre_flag = False
    #             break
            
            
    #     # checking epistemic preconditions
    #     for eq,value in preconditions["epistemic_p"]:
    #         current_time = datetime.now()
    #         temp_e_v = self.epistemic_model.checkingEQstr(self.external,eq,path,state,self.entities,self.variables)
    #         self.epistemic_call_time += datetime.now() - current_time
    #         epistemic_items_set.update({eq:temp_e_v})
    #         if not temp_e_v == value:
    #             pre_flag = False
    #     return pre_flag,epistemic_items_set     
    
    
    # def checkPreconditionsP(self,state,action,path):
    #     # self.logger.debug(f'checking precondition for action: {action}')
    #     preconditions = action.a_precondition
    #     pre_flag = True
    #     epistemic_items_set = {}
    #     p_dict ={}
    #     # checking ontic preconditions
    #     for v,e in preconditions['ontic_p']:
    #         try:
    #             if e in state:
    #                 if not state[v] == state[e]:  
    #                     pre_flag = False
    #                     break
    #             else:
    #                 if not state[v] == e:  
    #                     pre_flag = False
    #                     break
    #         except:
    #             self.logger.error("Error when checking precondition: {}\n with state: {}")
                
    #             pre_flag = False
    #             break
    #     # checking epistemic preconditions
    #     for eq,value in preconditions["epistemic_p"]:
    #         current_time = datetime.now()
    #         temp_e_v,temp_p_dict = self.epistemic_model.checkingEQstrP(self.external,eq,path,state,self.entities,self.variables)
    #         self.epistemic_call_time += datetime.now() - current_time
    #         p_dict.update(temp_p_dict)
    #         # epistemic_items_set.update({eq:temp_e_v})
    #         if not temp_e_v == value:
    #             pre_flag = False
    #     return pre_flag,p_dict       
    
    # def checkPreconditions(self,state,action,path):
    #     self.logger.debug(f'checking precondition for action: {action}')
    #     preconditions = action.a_precondition
    #     # checking ontic preconditions
    #     for v,e in preconditions['ontic_p']:
    #         try:
    #             if e in state:
    #                 if not state[v] == state[e]: return False
    #             else:
    #                 if not state[v] == e: return False
    #         except:
    #             self.logger.error("Error when checking precondition: {}\n with state: {}")
                
    #             return False
            
    #     # checking epistemic preconditions
    #     for eq,value in preconditions["epistemic_p"]:
    #         
    #         current_time = datetime.now()
    #         if not self.epistemic_model.checkingEQstr(self.external,eq,path,state,self.entities,self.variables) == value:
    #             self.epistemic_call_time += datetime.now() - current_time
    #             return False
    #         self.epistemic_call_time += datetime.now() - current_time
    #     return True

    # generate all possible parameter combinations
    def _generateVariables(self,params):
        self.logger.debug(f'params: {params}')
        param_list = []

        if params == []:
            return []
        else:
            
            for i in params[0]:
                next_param = copy.deepcopy(params[1:])
                rest = self._generateVariables(next_param)
                if len(rest) == 0:
                    param_list = param_list + [f"-{i}"]
                else:
                    param_list = param_list + [ f"-{i}{t}" for t in rest ]
        return param_list


    
    # generate all possible parameter combinations
    def _generateParams(self,params):
        param_list = []

        if params == []:
            return []
        else:
            i,v = params[0]

            for k,l in self.entities.items():

                if l.e_type == v:
                    next_param = copy.deepcopy(params[1:])
                    rest = self._generateParams(next_param)
                    if len(rest) == 0:
                        param_list = param_list + [[(i,k)]]
                    else:
                        param_list = param_list + [ [(i,k)]+ t for t in self._generateParams(next_param) ]
        return param_list
                    
    # TODO adding action cost
    def generateSuccessor(self,state,action,path):
        
        # TODO valid action
        # need to go nested on the brackets
        self.logger.debug(f'generate successor for state: {state}')
        self.logger.debug(f'generate successor with action: {action}')
        new_state = copy.deepcopy(state)
        
        for v_name,update in action.a_effects:
            old_value = state[v_name]
            # v_name = v_name.replace('?','-')
            # self.logger.debug(f'single effect update: {v_name}/{old_value}/{update}')
            # if update in state:
            #     new_state[v_name] = state[update]
            # elif '-' in update:
            if update.startswith('-'):
                # self.logger.debug(f'update -')
                delta_value = int(update.split('-')[1])
                # self.logger.debug(f'delta value: {delta_value}')
                domain_name = self.variables[v_name].v_domain_name
                # self.logger.debug(f'domain_name {domain_name}')
                if self.domains[domain_name].d_type == D_TYPE.ENUMERATE:
                    index = self.domains[domain_name].d_values.index(old_value)
                    # self.logger.debug(f'index: {index} in the domain: {self.domains[domain_name].d_values}')
                    new_index = (index-delta_value) % len(self.domains[domain_name].d_values)
                    # self.logger.debug(f'new_index: {new_index} in the domain: {self.domains[domain_name].d_values}')
                    new_value = self.domains[domain_name].d_values[new_index]
                    # self.logger.debug(f'new_value: {new_value} in the domain: {self.domains[domain_name].d_values}')
                    new_state[v_name] = new_value
                elif self.domains[domain_name].d_type == D_TYPE.INTEGER:
                    old_int = int(old_value)
                    # self.logger.debug(f'old_int: {old_int}')
                    new_value = old_int - delta_value
                    # self.logger.debug(f'new_value: {new_value} in the domain: {self.domains[domain_name].d_values}')
                    new_state[v_name] = new_value
                    
            elif update.startswith('+'):
                delta_value = int(update.split('+')[-1])
                domain_name = self.variables[v_name].v_domain_name
                if self.domains[domain_name].d_type == D_TYPE.ENUMERATE:
                    index = self.domains[domain_name].d_values.index(old_value)
                    new_index = (index+delta_value) % len(self.domains[domain_name].d_values)
                    new_state[v_name] = self.domains[domain_name].d_values[new_index]
                elif self.domains[domain_name].d_type == D_TYPE.INTEGER:
                    old_int = int(old_value)
                    self.logger.debug(f'old_int: {old_int}')
                    new_value = old_int + delta_value
                    self.logger.debug(f'new_value: {new_value} in the domain: {self.domains[domain_name].d_values}')
                    new_state[v_name] = new_value
            # if '-' in update:
            #     v2_name,value = update.split('-')
            #     v2_name = v2_name.replace('?','-')
            #     v2_value = state[v2_name]
            #     domain_name = self.variables[v_name].v_domain_name
            #     if self.domains[domain_name].d_type == D_TYPE.ENUMERATE:
            #         for index, item in enumerate(self.domains[domain_name].d_values):
            #             if item == v2_value:
            #                 break
            #         new_state[v_name] = self.domains[domain_name].d_values[(index-int(value))%len(self.domains[domain_name].d_values)]
            # elif '+' in update:
            #     v2_name,value = update.split('+')
            #     v2_name = v2_name.replace('?','-')
            #     v2_value = state[v2_name]
            #     domain_name = self.variables[v_name].v_domain_name
            #     if self.domains[domain_name].d_type == D_TYPE.ENUMERATE:
            #         for index, item in enumerate(self.domains[domain_name].d_values):
            #             if item == v2_value:
            #                 break
            #         new_state[v_name] = self.domains[domain_name].d_values[(index+int(value))%len(self.domains[domain_name].d_values)]
            else:
                
                domain_name = self.variables[v_name].v_domain_name
                # self.logger.debug(f'update {v_name} with domain {domain_name} on type {self.domains[domain_name].d_type} ')
                if self.domains[domain_name].d_type == D_TYPE.INTEGER:
                    if re.search("[a-z]|[A-Z]", update):
                        update = state[update]
                    new_state[v_name] = int(update)
                else:
                    new_state[v_name] = update

        # self.logger.debug(f'new state is : {new_state}')
        return new_state
        
        
    
    def __str__(self):
        return f"Problem: \n\t entities: {self.entities}\n\t variables: {self.variables}\n\t actions: {self.actions}\n\t domains: {self.domains}\n\t initial_state: {self.initial_state}\n\t goal_states: {self.goal_states}\n"

from enum import Enum
class E_TYPE(Enum):
    AGENT = 1
    OBJECT = 2

def eTypeConvert(logger,str):
    logger.debug(f"converting E_TYPE for {str}")
    if str == "agent":
        return E_TYPE.AGENT
    elif str == "object":
        return E_TYPE.OBJECT
    else:
        logger.error(f"E_TYPE not found for {str}")
class Entity():
    e_name = None
    e_type = None
   
    def __init__(self,e_name, e_type):
        self.e_name = e_name
        self.e_type = e_type

    def __str__(self): # show only in the print(object)
        return f"<Entity: e_name: {self.e_name}; e_type: {self.e_type}>\n"

    def __repr__(self): # show when in a dictionary
        return f"<Entity: e_name: {self.e_name}; e_type: {self.e_type}>\n"
        # return self

class Action():
    a_name = None
    a_parameters = []
    a_precondition = None
    a_effects = None
    
    def __init__(self,a_name, a_parameters, a_precondition, a_effects):
        self.a_name = a_name
        self.a_parameters = a_parameters
        self.a_precondition = a_precondition
        self.a_effects = a_effects

    def __str__(self): # show only in the print(object)
        return f"<Action: {self.a_name}; parameters: {self.a_parameters}; precondition: {self.a_precondition}; effects: {self.a_effects}>\n"

    def __repr__(self): # show when in a dictionary
        return f"<Action: {self.a_name}; parameters: {self.a_parameters}; precondition: {self.a_precondition}; effects: {self.a_effects}>\n"
    
class Variable():
    v_name = None
    v_domain_name = None
    v_parent = None
    
    def __init__(self,name,domain_name,v_parent):
        self.v_name = name
        self.v_domain_name = domain_name
        self.v_parent = v_parent
        
    def __str__(self): # show only in the print(object)
        return f"<Variable: v_name: {self.v_name}; v_domain: {self.v_domain_name}; v_parent: {self.v_parent}>\n"

    def __repr__(self): # show when in a dictionary
        return f"<Variable: v_name: {self.v_name}; v_domain: {self.v_domain_name}; v_parent: {self.v_parent}>\n"
        

    
def convertBooltoPDDL_TERNARY(bool):
    return PDDL_TERNARY.TRUE if bool else PDDL_TERNARY.FALSE
        
class D_TYPE(Enum):
    ENUMERATE = 1
    INTEGER = 2 

def dTypeConvert(logger,str):
    logger.debug(f"converting D_TYPE for {str}")
    if str == "enumerate":
        return D_TYPE.ENUMERATE
    elif str == "integer":
        return D_TYPE.INTEGER
    else:
        logger.error(f"D_TYPE not found for {str}")

class Domain():
    d_name = None
    d_values = None
    d_type = None
    agency = False
    
    def __init__(self,d_name,d_values,agency,d_type):
        self.d_name = d_name
        self.d_values = d_values
        self.agency = agency
        self.d_type = d_type
    
    def __str__(self): # show only in the print(object)
        return f"<domain_name: {self.d_name}; Basic type: {self.d_type}; values: {self.d_values}; isAgent?: {self.agency}>\n"

    def __repr__(self): # show when in a dictionary
        return f"<domain_name: {self.d_name}; Basic type: {self.d_type}; values: {self.d_values}; isAgent?: {self.agency}>\n"
    
    def isAgent(self):
        return self.agency


    


    
