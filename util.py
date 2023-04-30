


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
    
