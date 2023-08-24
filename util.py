


import logging
from enum import Enum
formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')


def setup_logger(name, handler, level=logging.INFO):
    """To setup as many loggers as you want"""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

def setup_log_handler(log_path):
    handler = logging.FileHandler(log_path)        
    handler.setFormatter(formatter)
    return handler

instance_handler = None

import heapq
class PriorityQueue:
    """
      Implements a priority queue data structure. Each inserted item
      has a priority associated with it and the client is usually interested
      in quick retrieval of the lowest-priority item in the queue. This
      data structure allows O(1) access to the lowest-priority item.
    """
    def  __init__(self):
        self.heap = []
        self.count = 0

    def getMinimumPriority(self):
        return self.heap[0][0]

    def push(self, item=None, priority=None):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        return item        

    def pop_full(self):
        # (_, _, item) = 
        return heapq.heappop(self.heap)


    def isEmpty(self):
        return len(self.heap) == 0

    def update(self, item=None, priority=None):
        # If item already in priority queue with higher priority, update its priority and rebuild the heap.
        # If item already in priority queue with equal or lower priority, do nothing.
        # If item not in priority queue, do the same thing as self.push.
        for index, (p, c, i) in enumerate(self.heap):
            if i == item:
                if p <= priority:
                    break
                del self.heap[index]
                self.heap.append((priority, c, item))
                heapq.heapify(self.heap)
                break
        else:
            self.push(item, priority)
            

            
            
import logging
from enum import Enum
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')


def setup_logger(name, handler, level=logging.INFO):
    """To setup as many loggers as you want"""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

def setup_log_handler(log_path):
    handler = logging.FileHandler(log_path)        
    handler.setFormatter(formatter)
    return handler

instance_handler = None



            

### PDDL value type

# PDDL_TERNARY 
# ternary true value
class PDDL_TERNARY(Enum):
    TRUE = 1
    UNKNOWN = 0
    FALSE = -1
    
    # def __repr__(self): 
    #     # show when in a dictionary
        
    #     return PDDL_TERNARY(self)

# the following classes are for pddl_model

class D_TYPE(Enum):
    ENUMERATE = 1
    INTEGER = 2 
    AGENT = 3

def dTypeConvert(logger,str):
    logger.debug(f"converting D_TYPE for {str}")
    if str == "enumerate":
        return D_TYPE.ENUMERATE
    elif str == "integer":
        return D_TYPE.INTEGER
    elif str == "agent":
        return D_TYPE.AGENT
    else:
        logger.error(f"D_TYPE not found for {str}")


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


# the following classes are for epistemic model


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
    header_str = ""
    agents_str = ""
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
    
    def __init__(self,header_str,agents_str,content):
        
        self.q_type,self.eq_type = self.mapping[header_str]
        self.header_str = header_str
        self.agents_str = agents_str
        self.q_group = agents_str[1:-1].split(",")
        self.q_content = content
        
    def show(self):
        # for debug purpose
        output = f"<epistemic: q_type: {self.q_type}; eq_type: {self.eq_type}; q_group: {self.q_group}; q_content: {self.q_content} >"
        return output
        
    def __str__(self): 
        # show only in the print(object)
        output = f"{self.header_str} {self.agents_str} {self.q_content}"
        return output

    def __repr__(self): 
        # show when in a dictionary
        output = f"{self.header_str} {self.agents_str} {self.q_content}"
        return output





















# LOGGER_NAME = "util"
# logger = setup_logger(LOGGER_NAME,instance_handler,logging.INFO) 

# from epistemic_model import EpistemicQuery,Q_TYPE,EQ_TYPE
# def displayEQuery(epistemic_query: EpistemicQuery):
    
#     logger.debug("display eq")
#     first_char = ''
#     second_char = ''
#     if type(epistemic_query) == str:
#         return epistemic_query
    
#     if len(epistemic_query.q_group):
#         first_char = ''
#     elif epistemic_query.q_type == Q_TYPE.MUTUAL:
#         first_char = 'E'
#     elif epistemic_query.q_type == Q_TYPE.DISTRIBUTION:
#         first_char = 'D'
#     elif epistemic_query.q_type == Q_TYPE.COMMON:
#         first_char = 'C'
#     else:
#         logger.error(f'Unexpected query type: {epistemic_query}')
    

#     if epistemic_query.eq_type == EQ_TYPE.SEEING:
#         second_char = 'S'
#     elif epistemic_query.eq_type == EQ_TYPE.KNOWLEDGE:
#         second_char = 'K'
#     elif epistemic_query.eq_type == EQ_TYPE.BELIEF:
#         second_char = 'B'
#     else:
#         logger.error(f'Unexpected e_query type: {epistemic_query}')
    
#     return f"{first_char}{second_char} {epistemic_query.q_group} {displayEQuery(epistemic_query.q_content)}"
    
