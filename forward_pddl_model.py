from datetime import datetime, timedelta
import logging
import os
import copy
import re
from typing import List
# from epistemic_model import EpistemicModel
# from forward_epistemic_model import EpistemicModel

import epistemic_model
import forward_epistemic_model

LOGGER_NAME = "pddl_model"
LOGGER_LEVEL = logging.INFO
# LOGGER_LEVEL = logging.DEBUG


from util import setup_logger,PDDL_TERNARY
from util import Variable,Action
from util import Domain,D_TYPE,dTypeConvert
from util import Entity,E_TYPE,eTypeConvert
from util import Conditions

# Class of the problem
class Problem:
    initial_state = {}
    actions = {} 
    entities = {} # agent indicators, should be unique
    variables = {} #variable
    domains = {}
    initial_state = {}
    goals = None
    external = None
    epistemic_calls = 0
    epistemic_call_time = timedelta(0)
    epistemic_model = None
    logger = None

    def __init__(self, domains,i_state,g_states,agent_index,obj_index,variables, actions, external=None, belief_mode=-1,handlers=None):
        self.initial_state = {}
        self.abstract_actions = {} 
        self.entities = {} # agent indicators, should be unique
        self.variables = {} #variable
        self.domains = {}
        self.initial_state = {}
        self.goals = None
        self.epistemic_calls = 0
        self.epistemic_call_time = timedelta(0)
        self.logger = None
        self.logger = setup_logger(LOGGER_NAME,handlers,logger_level=LOGGER_LEVEL) 
        self.logger.debug("initialize entities")
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
            
        # grounding all abstract_actions or do not ground any abstract_actions?    
        # self.logger.debug("initialize abstract_actions")
        # self.logger.debug(actions )
        for a_name, parts in actions.items():
            
            p = [ (i,eTypeConvert(self.logger,t))for i,t in parts['parameters']]
            self.logger.debug("parts['precondition']: [%s]",parts['precondition'])
            a_temp = Action(a_name, p,parts['precondition'], parts['effect'])
            self.abstract_actions.update({a_name:a_temp})
        self.logger.debug(self.abstract_actions)
        
        # self.logger.debug("initialize domains")
        self.domains = {}
        # self.logger.debug('input domains: {domains}')
        for d_name in domains.keys():
            values = domains[d_name]['values']
            d_type = dTypeConvert(self.logger,domains[d_name]['basic_type'])
            if d_type == D_TYPE.INTEGER:
                bound = domains[d_name]['values']
                values = list(range(bound[0],bound[1]+1))

            domain_temp = Domain(d_name,values,d_name=='agent',d_type)
            self.domains.update({d_name:domain_temp})
        self.logger.debug(self.domains)
        
        self.goals = Conditions(g_states['ontic_g'],g_states['epistemic_g'])
        self.logger.debug(self.goals)
        self.initial_state = i_state
        self.logger.debug(self.initial_state)
        self.external = external
        if belief_mode == 0:
            self.epistemic_model = epistemic_model.EpistemicModel(handlers,self.entities,self.variables,external)
        elif belief_mode == 1:
            self.epistemic_model = forward_epistemic_model.EpistemicModel(handlers,self.entities,self.variables,external)
        elif belief_mode == 2:
            assert False,"belief mode not defined yet" 
        elif belief_mode ==3:
            assert False,"belief mode not defined yet"
        else:
            assert False,"belief mode should be between 0-3"

    
    def isGoal(self,state,path,p_path):
        is_goal=True
        goal_dict = {}
        # self.logger.debug("checking goal for state: {state} with path: {path}")
        actions = [ a  for s,a in path]
        actions = actions[1:]
        for k,v in self.goals.ontic_dict.items():
            if not state[k] == v:
                is_goal = False
                goal_dict.update({k+" "+str(v):False})
            else:
                goal_dict.update({k+" "+str(v):True})
            
        # adding epistemic checker here
        current_time = datetime.now()
        self.epistemic_calls +=1
        epistemic_dict = \
            self.epistemic_model.epistemicGoalsHandler(self.goals.epistemic_dict,"",path,p_path)
        self.epistemic_call_time += datetime.now() - current_time
        
        for k,v in self.goals.epistemic_dict.items():
            if not epistemic_dict[k].value == v:
                is_goal = False
                goal_dict.update({k+" "+str(v):False})
            else:
                goal_dict.update({k+" "+str(v):True})
                
        # self.logger.debug("epistemic_dict {epistemic_dict}")
        # self.logger.debug("p_dict {p_dict}")
        return is_goal,epistemic_dict,goal_dict
    
    def getAllActions(self,state,path):
        all_actions = {}
        
        # get all type of actions
        for a_name, abstract_a in self.abstract_actions.items():
            # # self.logger.debug('action: {a} ')
            
            
            # generate all possible combination parameters for each type of action
            # # self.logger.debug('all params: {self._generateParams(a.a_parameters)}')

            if abstract_a.a_parameters == []:
                a_temp_name = a_name
                a_temp_parameters = copy.deepcopy(abstract_a.a_parameters)
                a_temp_pre = copy.deepcopy(abstract_a.a_preconditions)
                a_temp_pre_dict = {'ontic_p':a_temp_pre.ontic_dict,'epistemic_p':a_temp_pre.epistemic_dict}
                # a_temp_ontic_p = copy.deepcopy(list(abstract_a.a_precondition.ontic_dict))
                # a_temp_epistemic_p = copy.deepcopy(list(abstract_a.a_precondition.epistemic_dict))
                a_temp_effects = copy.deepcopy(abstract_a.a_effects)
                # if self._checkPreconditions(state,a_temp_precondition,path):
                all_actions.update({a_temp_name:Action(a_temp_name,a_temp_parameters,a_temp_pre_dict,a_temp_effects)})
                    # # self.logger.debug('legal action after single precondition check: {all_actions}') 
            else:
                for params in self._generateParams(abstract_a.a_parameters):
                    a_temp_name = a_name
                    a_temp_parameters = copy.deepcopy(abstract_a.a_parameters)
                    a_temp_ontic_p_list = copy.deepcopy(list(abstract_a.a_preconditions.ontic_dict.items()))
                    a_temp_epistemic_p_list = copy.deepcopy(list(abstract_a.a_preconditions.epistemic_dict.items()))
                    a_temp_effects = copy.deepcopy(abstract_a.a_effects)
                    # # self.logger.debug('works on params: {params}')
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
                        for j in range(len(a_temp_ontic_p_list)):
                            v_name, v_effects = a_temp_ontic_p_list[j]
                            v_name = v_name.replace(f'{i}',f'-{v}')
                            if type(v_effects) == str:
                                v_effects = v_effects.replace(f'{i}',f'-{v}')
                            a_temp_ontic_p_list[j]  = (v_name,v_effects)

                        # update parameters in the epistemic precondition
                        for j in range(len(a_temp_epistemic_p_list)):
                            v_name, v_effects = a_temp_epistemic_p_list[j]
                            v_name = v_name.replace(f'{i}',f'-{v}').replace('[-','[').replace(',-',',')
                            # precondition effect of epistemic is only going to be int
                            # v_effects = v_effects.replace(f'{i}',f'-{v}')
                            a_temp_epistemic_p_list[j] = (v_name,v_effects)                            
                        
                        # update parameters in the effects
                        for j in range(len(a_temp_effects)):
                            v_name, v_effects = a_temp_effects[j]
                            v_name = v_name.replace(f'{i}',f'-{v}')
                            v_effects = v_effects.replace(f'{i}',f'-{v}')
                            a_temp_effects[j] = (v_name,v_effects)
                    # # self.logger.debug('precondition after matching parameters: {a_temp_precondition}')
                    # # self.logger.debug('effect after matching parameters: {a_temp_effects}')
                    
                    
                    # # self.logger.debug('legal action before precondition check: {all_actions}') 
                    # # TODO: adding precondition check
                    # if self._checkPreconditions(state,a_temp_precondition,path):
                    #     all_actions.update({a_temp_name:Action(a_temp_name,a_temp_parameters,a_temp_precondition,a_temp_effects)})
                    # # self.logger.debug('legal action after precondition check: {all_actions}') 
                    # self.logger.debug("dict(a_temp_ontic_p_list){a_temp_ontic_p_list}")
                    
                    a_temp_pre_dict = {'ontic_p':dict(a_temp_ontic_p_list),'epistemic_p':dict(a_temp_epistemic_p_list)}
                    
                    all_actions.update({a_temp_name:Action(a_temp_name,a_temp_parameters,a_temp_pre_dict,a_temp_effects)})
                    # # self.logger.debug('legal action before precondition check: {all_actions}') 
        # self.logger.debug('legal actions: {all_actions.keys()}') 
        return all_actions   

    def checkAllPreconditions(self,state,path,ontic_pre_dict,epistemic_pre_dict,p_path):
        self.logger.debug('function checkAllPreconditions')
        self.logger.debug('checking precondition for state: [%s]', state)
        # preconditions = action.a_precondition

        pre_dict = {}
        flag_dict = {}
        
        # checking ontic preconditions
        self.logger.debug('checking all ontic preconditions')
        for action_name,ontic_pre in ontic_pre_dict.items():
            pre_dict[action_name] = {}
            flag_dict[action_name] = True
            self.logger.debug('checking ontic precondition [%s] for action [%s]',ontic_pre,action_name)
            for k,e in ontic_pre.items():
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
                    self.logger.error("Error when checking precondition: [%s]\n with state: [%s]", ontic_pre,state)
                    
                    flag_dict[action_name] = False
        self.logger.debug("pre_dict [%s]", pre_dict)
            
        # adding epistemic checker here
        # self.logger.debug("epistemic_pre: {preconditions['epistemic_p']}")

        self.logger.debug("checking all epistemic preconditions")
        # get all ep_pre into one list
        temp_ep_dict = {}
        # this part need to be changed
        self.logger.debug("epistemic_pre_dict: [%s]",epistemic_pre_dict)
        for action_name,ep_pre in epistemic_pre_dict.items():
            # for ep in ep_pre.items():
            temp_ep_dict.update(ep_pre) 
            
        self.logger.debug("epistemic preconditions list [%s]",epistemic_pre_dict)    
        current_time = datetime.now()
        self.epistemic_calls +=1
        epistemic_dict = self.epistemic_model.epistemicGoalsHandler(temp_ep_dict,"",path,p_path)
        self.epistemic_call_time += datetime.now() - current_time

        ep_dict = {}
        for action_name,ep_pre in epistemic_pre_dict.items():
            ep_dict[action_name] = {}
            for k,v in ep_pre.items():
                if not epistemic_dict[k].value == v:
                    flag_dict[action_name] = False
                    pre_dict[action_name].update({k+":"+str(e):False})
                    # pre_flag = False
                    # pre_dict.update({k+" "+str(v):False})
                else:
                    pre_dict[action_name].update({k+":"+str(e):True})
        self.logger.debug("pre_dict: [%s]",pre_dict)
        
        return flag_dict,epistemic_dict,pre_dict

    # generate all possible parameter combinations
    def _generateVariables(self,params):
        self.logger.debug('params: [%s]',params)
        param_list = []

        if params == []:
            return []
        else:
            
            for i in params[0]:
                next_param = copy.deepcopy(params[1:])
                rest = self._generateVariables(next_param)
                if len(rest) == 0:
                    param_list = param_list + [f"-{i}" ]
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
        self.logger.debug('generate successor for state: [%s]',state)
        self.logger.debug('generate successor with action: [%s]',action)
        new_state = copy.deepcopy(state)
        
        for v_name,update in action.a_effects:
            old_value = state[v_name]
            # v_name = v_name.replace('?','-')
            # self.logger.debug('single effect update: {v_name}/{old_value}/{update}')
            # if update in state:
            #     new_state[v_name] = state[update]
            # elif '-' in update:
            if update.startswith('-'):
                # self.logger.debug('update -')
                delta_value = int(update.split('-')[1])
                # self.logger.debug('delta value: {delta_value}')
                domain_name = self.variables[v_name].v_domain_name
                # self.logger.debug('domain_name {domain_name}')
                if self.domains[domain_name].d_type == D_TYPE.ENUMERATE:
                    index = self.domains[domain_name].d_values.index(old_value)
                    # self.logger.debug('index: {index} in the domain: {self.domains[domain_name].d_values}')
                    new_index = (index-delta_value) % len(self.domains[domain_name].d_values)
                    # self.logger.debug('new_index: {new_index} in the domain: {self.domains[domain_name].d_values}')
                    new_value = self.domains[domain_name].d_values[new_index]
                    # self.logger.debug('new_value: {new_value} in the domain: {self.domains[domain_name].d_values}')
                    new_state[v_name] = new_value
                elif self.domains[domain_name].d_type == D_TYPE.INTEGER:
                    old_int = int(old_value)
                    # self.logger.debug('old_int: {old_int}')
                    new_value = old_int - delta_value
                    # self.logger.debug('new_value: {new_value} in the domain: {self.domains[domain_name].d_values}')
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
                    self.logger.debug('old_int: [%s]',old_int)
                    new_value = old_int + delta_value
                    self.logger.debug('new_value: [%s] in the domain: [%s]',new_value,self.domains[domain_name].d_values)
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
                # self.logger.debug('update {v_name} with domain {domain_name} on type {self.domains[domain_name].d_type} ')
                if self.domains[domain_name].d_type == D_TYPE.INTEGER:
                    if re.search("[a-z]|[A-Z]", update):
                        update = state[update]
                    new_state[v_name] = int(update)
                else:
                    new_state[v_name] = update

        # self.logger.debug('new state is : {new_state}')
        return new_state
        
        
    
    def __str__(self):
        return f"Problem: \n\t entities: {self.entities}\n\t variables: {self.variables}\n\t actions: {self.actions}\n\t domains: {self.domains}\n\t initial_state: {self.initial_state}\n\t goals: {self.goals}\n"



    
