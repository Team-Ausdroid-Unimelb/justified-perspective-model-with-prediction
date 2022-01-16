import logging
import os
import copy
import re
from typing import List

from numpy.core.defchararray import _join_dispatcher
from numpy.lib.shape_base import _put_along_axis_dispatcher
from numpy.ma.core import common_fill_value
import bbl


# Class of the problem
class Problem():
    initial_state = {}
    actions = {} 
    entities = {} # agent indicators, should be unique
    variables = {} #variable
    domains = {}
    initial_state = {}
    goal_states = {}

    def __init__(self, domains,i_state,g_states,agent_index,obj_index,variables,actions):
        
        logging.debug("initialize entities")
        self.entities = {}
        for i in agent_index:
            e_temp = Entity(i,E_TYPE.AGENT)
            self.entities.update({i:e_temp})
        for i in obj_index:
            e_temp = Entity(i,E_TYPE.OBJECT)
            self.entities.update({i:e_temp})        
        logging.debug(self.entities)
        
        logging.debug("initialize variable")
        self.variables = {}
        for v_name,targets in variables.items():
            for i in targets:
                v_temp = Variable(f"{v_name}-{i}",v_name,i)
                self.variables.update({f"{v_name}-{i}":v_temp})
        logging.debug(self.variables)
            
        # grounding all actions or do not ground any actions?    
        logging.debug("initialize actions")
        logging.debug(actions )
        for a_name, parts in actions.items():
            
            p = [ (i,eTypeConvert(t))for i,t in parts['parameters']]
            a_temp = Action(a_name, p,parts['precondition'], parts['effect'])
            self.actions.update({a_name:a_temp})
        logging.debug(self.actions)
        
        logging.debug("initialize domains")
        self.domains = {}
        for d_name in domains.keys():
            # print(d_name)
            domain_temp = Domain(d_name,domains[d_name]['values'],d_name=='agent',dTypeConvert(domains[d_name]['basic_type']))
            self.domains.update({d_name:domain_temp})
        logging.debug(self.domains)
        
        self.goal_states = g_states
        logging.debug(self.goal_states)
        self.initial_state = i_state
        logging.debug(self.initial_state)
    
        
    def isGoal(self,state):
        logging.debug(f"checking goal for state: {state}")
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
                    legal_actions.update({a_temp_name:Action(a_temp_name,a_temp_parameters,a_temp_precondition,a_temp_effects)})
                    print(legal_actions)
        return legal_actions
    
    
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
        return f"Problem: \n\t entities: {self.entities}\n\t variables: {self.variables}\n\t actions: {self.actions}\n\t types: {self.types}\n\t initial_state: {self.initial_state}\n\t goal_states: {self.goal_states}\n"

from enum import Enum
class E_TYPE(Enum):
    AGENT = 1
    OBJECT = 2

def eTypeConvert(str):
    logging.debug(f"converting E_TYPE for {str}")
    if str == "agent":
        return E_TYPE.AGENT
    elif str == "object":
        return E_TYPE.OBJECT
    else:
        logging.error(f"E_TYPE not found for {str}")
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
    
        
class D_TYPE(Enum):
    ENUMERATE = 1
    INTEGER = 2 

def dTypeConvert(str):
    logging.debug(f"converting D_TYPE for {str}")
    if str == "enumerate":
        return D_TYPE.ENUMERATE
    elif str == "integer":
        return D_TYPE.INTEGER
    else:
        logging.error(f"D_TYPE not found for {str}")

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

def generateObservation(problem:Problem,state,agt_index):
    new_state = {}
    for var_index,value in state.items():
        if bbl.checkVisibility(problem,state,agt_index,var_index)==T_TYPE.TRUE:
            new_state.update({var_index:value})
    return new_state

def generatePerspective(problem:Problem, path:List, agt_index):
    logging.debug("generatePerspective")
    assert(path == [])
    state, action = path[-1]
    new_state = generateObservation(problem,state,agt_index)
    memory = generateMemorization(problem, path[:-1],agt_index)

    for var_index,value in state.items():
        if var_index not in new_state.keys():
            if memory == {}:
                new_state.update({var_index:None})
            else:
                new_state.update({var_index:memory[var_index]})
    return new_state

def generateMemorization(problem:Problem,path:List,agt_index):
    # if there is no state ahead, then return empty
    # this can be altered to handle different initial BELIEF
    if path == []:
        return {}
    new_state = {}
    state,action=path[-1]
    observation = generateObservation(problem,state,agt_index)
    perspective = generatePerspective(problem,path[:-1],agt_index)
    for var_index,value in perspective.items():
        if not var_index in observation.keys():
            new_state.update({var_index,value})
    return new_state
    

class Q_TYPE(Enum):
    MUTUAL = 0
    DISTRIBUTION = -1
    COMMON = 1
    
class EQ_TYPE(Enum):
    KNOWLEDGE = 1
    SEEING = 0
    BELIEF = 2
    
class EpistemicQuery:
    q_type = None
    q_content = None
    eq_type = None
    q_group = []
    mapping = {
        'k': (Q_TYPE.MUTUAL, EQ_TYPE.KNOWLEDGE),
        'ek': (Q_TYPE.MUTUAL, EQ_TYPE.KNOWLEDGE),
        'dk': (Q_TYPE.DISTRIBUTION ,EQ_TYPE.KNOWLEDGE),
        'ck': (Q_TYPE.COMMON, EQ_TYPE.KNOWLEDGE),
        's': (Q_TYPE.MUTUAL, EQ_TYPE.SEEING),
        'es': (Q_TYPE.MUTUAL, EQ_TYPE.SEEING),
        'ds': (Q_TYPE.DISTRIBUTION, EQ_TYPE.SEEING),
        'cs': (Q_TYPE.COMMON, EQ_TYPE.SEEING),
        'b': (Q_TYPE.MUTUAL, EQ_TYPE.BELIEF),
        'eb': (Q_TYPE.MUTUAL, EQ_TYPE.BELIEF),
        'db': (Q_TYPE.DISTRIBUTION, EQ_TYPE.BELIEF),
        'cb': (Q_TYPE.COMMON, EQ_TYPE.BELIEF),
    }
    
    def __init__(self,header,group_str,content):
        self.q_type,self.eq_type = self.mapping[header]
        self.q_group = group_str.split(",")
        self.q_content = content
        # import re
        # if not len(re.findall()) == 0:
        #     self.content = EpistemicQuery
        
        
    def __str__(self): # show only in the print(object)
        output = f"<epistemic: q_type: {self.q_type}; eq_type: {self.eq_type}; q_group: {self.q_group}; q_content: {self.q_content} >"
        # if type(self.q_content) == str:
        #     output += "\n\n"
        return output

    def __repr__(self): # show when in a dictionary
        output = f"<epistemic: q_type: {self.q_type}; eq_type: {self.eq_type}; q_group: {self.q_group}; q_content: {self.q_content} >"
        # if type(self.q_content) == str:
        #     output += "\n\n"
        return output
    
def generateEpistemicQuery(eq_str):
    match = re.search("[edc]?[ksb] \[[0-9a-z_,]*\] ",eq_str)
    if match == None:
        return eq_str
    else:
        eq_list = eq_str.split(" ")
        header = eq_list[0]
        agents = eq_list[1][1:-1]
        content = eq_str[len(header)+len(agents)+4:]
        return EpistemicQuery(header,agents,generateEpistemicQuery(content))
    

def checkingEQs(problem:Problem,eq_str_list:List,path:List):
    eq_pair_list = [(generateEpistemicQuery(eq_str),value) for eq_str,value in eq_str_list]
    logging.debug(f"{eq_pair_list}")
    for eq,value in eq_pair_list:
        print(value)
        if not checkingEQ(problem,eq,path) == value:
            return False
    return True

def checkingEQ(problem:Problem,eq:EpistemicQuery,path:List):
    logging.debug(f"checking eq {eq}, {eq.eq_type}")
    if eq.eq_type == EQ_TYPE.BELIEF:
        print()
    elif eq.eq_type == EQ_TYPE.SEEING:
        
        # generate the world
        world = generateObservation(problem,path[-1][0],eq.q_group[0])
        logging.debug(f"b's observation {world}")
        if len(eq.q_group) > 1:
            # merging observation
            pass
        if type(eq.q_content) == str:
            return bbl.evaluateS(problem,world,eq.q_content)
    elif eq.eq_type == EQ_TYPE.KNOWLEDGE:   
        logging.debug("checking knowledge")
        # generate the world
        world = generateObservation(problem,path[-1][0],eq.q_group[0])
        logging.debug(f"b's observation {world}")
        if len(eq.q_group) > 1:
            # merging observation
            pass
        logging.debug(type(eq.q_content))
        if type(eq.q_content) == str:
            return bbl.evaluateK(problem,world,eq.q_content)
    else:
        logging.error(f"not found eq_type in the query: {eq}")
        
    
    if type(eq.q_content) == str:
        # checking the last level of the formula
        pass
    
    return