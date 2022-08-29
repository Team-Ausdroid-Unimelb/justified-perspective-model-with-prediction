import logging
import os
import copy
import re
from typing import List

logger = logging.getLogger("pddl_model")
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
class Problem():
    initial_state = {}
    actions = {} 
    entities = {} # agent indicators, should be unique
    variables = {} #variable
    domains = {}
    initial_state = {}
    goal_states = {}
    external = None

    def __init__(self, domains,i_state,g_states,agent_index,obj_index,variables,actions, external=None):
        
        logger.debug("initialize entities")
        self.entities = {}
        for i in agent_index:
            e_temp = Entity(i,E_TYPE.AGENT)
            self.entities.update({i:e_temp})
        for i in obj_index:
            e_temp = Entity(i,E_TYPE.OBJECT)
            self.entities.update({i:e_temp})        
        logger.debug(self.entities)
        
        logger.debug("initialize variable")
        self.variables = {}
        for v_name,targets in variables.items():
            for i in targets:
                v_temp = Variable(f"{v_name}-{i}",v_name,i)
                self.variables.update({f"{v_name}-{i}":v_temp})
        logger.debug(self.variables)
            
        # grounding all actions or do not ground any actions?    
        logger.debug("initialize actions")
        logger.debug(actions )
        for a_name, parts in actions.items():
            
            p = [ (i,eTypeConvert(t))for i,t in parts['parameters']]
            a_temp = Action(a_name, p,parts['precondition'], parts['effect'])
            self.actions.update({a_name:a_temp})
        logger.debug(self.actions)
        
        logger.debug("initialize domains")
        self.domains = {}
        for d_name in domains.keys():
            # print(d_name)
            domain_temp = Domain(d_name,domains[d_name]['values'],d_name=='agent',dTypeConvert(domains[d_name]['basic_type']))
            self.domains.update({d_name:domain_temp})
        logger.debug(self.domains)
        
        self.goal_states = g_states
        logger.debug(self.goal_states)
        self.initial_state = i_state
        logger.debug(self.initial_state)
        
        self.external = external
    
        
    def isGoal(self,state):
        logger.debug(f"checking goal for state: {state}")
        for k,i in self.goal_states["ontic_g"].items():
            if not state[k] == i:
                return False
            
        # adding epistemic checker here
        return True
    
    def getLegalActions(self,state):
        legal_actions = {}
        
        # get all type of actions
        for a_name, a in self.actions.items():
            print(f"param: {a.a_parameters}; all params: {self._generateParams(a.a_parameters)}")
            
            # generate all possible combination parameters for each type of action
            for params in self._generateParams(a.a_parameters):
                
                for i,v in params:
                    a_temp_name = a_name
                    a_temp_parameters = copy.deepcopy(a.a_parameters)
                    print(f"a's PPPPP {a.a_parameters}")
                    print(a)
                    print((i,v))
                    a_temp_precondition = copy.deepcopy(a.a_precondition)
                    a_temp_effects = copy.deepcopy(a.a_effects)
                    a_temp_name = a_temp_name + "-" + v
                    for j in range(len(a_temp_parameters)):
                        v_name, v_effects = a_temp_parameters[j]
                        v_name = v_name.replace(f'{i}',f'?{v}')
                        a_temp_parameters[j] = (v_name,v_effects)
                    for j in range(len(a_temp_precondition)):
                        v_name, v_effects = a_temp_precondition[j]
                        v_name = v_name.replace(f'{i}',f'?{v}')
                        v_effects = v_effects.replace(f'{i}',f'?{v}')
                        a_temp_precondition[j] = (v_name,v_effects)
                    for j in range(len(a_temp_effects)):
                        v_name, v_effects = a_temp_effects[j]
                        v_name = v_name.replace(f'{i}',f'?{v}')
                        v_effects = v_effects.replace(f'{i}',f'?{v}')
                        a_temp_effects[j] = (v_name,v_effects)
                        
                        
                    # TODO: adding precondition check
                    if self._checkPreconditions(state,a_temp_precondition):
                        legal_actions.update({a_temp_name:Action(a_temp_name,a_temp_parameters,a_temp_precondition,a_temp_effects)})
                    print(legal_actions)
        return legal_actions
    
    def _checkPreconditions(self,state,preconditions):
        for v,e in preconditions:
            try:
                if not state[v] == e: return False
            except:
                logger.error("Error when checking precondition: {}\n with state: {}")
                
                return False
        return True
    
    # generate all possible parameter combinations
    def _generateParams(self,params):
        param_list = []
        print(params)
        if params == []:
            return []
        else:
            i,v = params[0]
            print((i,v))
            for k,l in self.entities.items():
                print(l)
                if l.e_type == v:
                    next_param = copy.deepcopy(params[1:])
                    rest = self._generateParams(next_param)
                    if len(rest) == 0:
                        param_list = param_list + [[(i,k)]]
                    else:
                        param_list = param_list + [ [(i,k)]+ t for t in self._generateParams(next_param) ]
        return param_list
                    
    # TODO adding action cost
    def generatorSuccessor(self,state,action,path):
        
        # TODO valid action
        # need to go nested on the brackets
        
        new_state = copy.deepcopy(state)
        print(action)
        for v_name,update in action.a_effects:
            v_name = v_name.replace('?','-')
            if '-' in update:
                v2_name,value = update.split('-')
                v2_name = v2_name.replace('?','-')
                v2_value = state[v2_name]
                domain_name = self.variables[v_name].v_domain_name
                if self.domains[domain_name].d_type == D_TYPE.ENUMERATE:
                    for index, item in enumerate(self.domains[domain_name].d_values):
                        if item == v2_value:
                            break
                    new_state[v_name] = self.domains[domain_name].d_values[(index-int(value))%len(self.domains[domain_name].d_values)]
            elif '+' in update:
                v2_name,value = update.split('+')
                v2_name = v2_name.replace('?','-')
                v2_value = state[v2_name]
                domain_name = self.variables[v_name].v_domain_name
                if self.domains[domain_name].d_type == D_TYPE.ENUMERATE:
                    for index, item in enumerate(self.domains[domain_name].d_values):
                        if item == v2_value:
                            break
                    new_state[v_name] = self.domains[domain_name].d_values[(index+int(value))%len(self.domains[domain_name].d_values)]
            elif '=' in update:
                pass
        
        return new_state
        
        
    
    def __str__(self):
        return f"Problem: \n\t entities: {self.entities}\n\t variables: {self.variables}\n\t actions: {self.actions}\n\t domains: {self.domains}\n\t initial_state: {self.initial_state}\n\t goal_states: {self.goal_states}\n"

from enum import Enum
class E_TYPE(Enum):
    AGENT = 1
    OBJECT = 2

def eTypeConvert(str):
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
        
class T_TYPE(Enum):
    TRUE = 1
    UNKNOWN = 0
    FALSE = -1
    
def convertBooltoT_TYPE(bool):
    return T_TYPE.TRUE if bool else T_TYPE.FALSE
        
class D_TYPE(Enum):
    ENUMERATE = 1
    INTEGER = 2 

def dTypeConvert(str):
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


    


    
