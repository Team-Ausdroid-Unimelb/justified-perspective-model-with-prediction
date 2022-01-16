# from model import Problem,E_TYPE,T_TYPE
import logging 
import math
from typing import Tuple
import numpy as np
import traceback
import model
import re

# {'agent': <domain_name: agent; Basic type: None; values: []; isAgent?: True>
# , 'dir': <domain_name: dir; Basic type: D_TYPE.ENUMERATE; values: ['w', 'nw', 'n', 'ne', 'e', 'se', 's', 'sw']; isAgent?: False>
# , 'x': <domain_name: x; Basic type: D_TYPE.INTEGER; values: [0, 4]; isAgent?: False>
# , 'y': <domain_name: y; Basic type: D_TYPE.INTEGER; values: [0, 4]; isAgent?: False>
# , 'v': <domain_name: v; Basic type: D_TYPE.ENUMERATE; values: ['t', 'f']; isAgent?: False>
# }
# {'dir-a': 'sw', 'dir-b': 'sw', 'x-a': 3, 'x-b': 2, 'x-p': 1, 'y-a': 3, 'y-b': 2, 'y-p': 1, 'v-p': 't'}
# {'ontic_g': {'dir-b': 'se', 'v-p': 't'}, 'epistemic_g': [("k [a,b] (= (v p) 't'))", '1')]}
# {'a': <Entity: name: a; type: E_TYPE.AGENT>
# , 'b': <Entity: name: b; type: E_TYPE.AGENT>
# , 'p': <Entity: name: p; type: E_TYPE.OBJECT>
# }
# {'dir-a': <Variable: name: dir-a; domain: dir; parent: a>
# , 'dir-b': <Variable: name: dir-b; domain: dir; parent: b>
# , 'x-a': <Variable: name: x-a; domain: x; parent: a>
# , 'x-b': <Variable: name: x-b; domain: x; parent: b>
# , 'x-p': <Variable: name: x-p; domain: x; parent: p>
# , 'y-a': <Variable: name: y-a; domain: y; parent: a>
# , 'y-b': <Variable: name: y-b; domain: y; parent: b>
# , 'y-p': <Variable: name: y-p; domain: y; parent: p>
# , 'v-p': <Variable: name: v-p; domain: v; parent: p>
# }
# {'turn_clockwise': <Action: turn_clockwise; parameters: [('?i', <E_TYPE.AGENT: 1>)]; precondition: []; effects: [('dir?i', 'dir?i+1')]>
# , 'turn_counter_clockwise': <Action: turn_counter_clockwise; parameters: [('?i', <E_TYPE.AGENT: 1>)]; precondition: []; effects: [('dir?i', 'dir?i-1')]>
# }

 
# declare common variables
common_constants = {
    'angle-a': 90,
    'angle-b': 90,
}

dir_dict = {
    'n': 90,
    'ne': 45,
    'e':0,
    'se':-45,
    's':-90,
    'sw':-135,
    'w':180,
    'nw':135,
}

# customized evaluation function
def evaluateK(problem,world,statement):
    logging.debug(f"evalute knowledge: {statement} in the world: {world}, {type(statement)}, {len(statement)}")
    #default evaluation for variables
    print()
    if not re.search("\([0-9a-z _\-]*,[0-9a-z _\'\"]*\)",statement) == None:
        var_name = statement.split(",")[0][1:]
        value = statement.split(",")[1][:-1]
        if var_name in world.keys():
            return value == world[var_name]
        else:
            return False
    else:
        logging.warning("the evaluation of the knowledge equation has not defined")
        return False

# customized evaluation function
def evaluateS(problem,world,statement):
    
    #default evaluation for variables
    if type(statement) == Tuple and len(statement) == 2:
        var_name,value = statement
        if var_name in world.keys():
            return True
        else:
            return False
    else:
        logging.warning("the evaluation of the seeing equation has not defined")
        return False



def checkVisibility(problem,state,agt_index,var_index):
    
    logging.debug(f"checkVisibility(_,_,{agt_index},{var_index})")
    try:
        tgt_index = problem.variables[var_index].v_parent
        # check if the agt_index can be found
        assert(problem.entities[agt_index].e_type==model.E_TYPE.AGENT)
        
        #extract necessary variables from state
        logging.debug(f"loading variables from state")
        tgt_x = state[f"x-{tgt_index}"]
        tgt_y = state[f"y-{tgt_index}"]
        agt_x = state[f"x-{agt_index}"]
        agt_y = state[f"y-{agt_index}"]
        agt_dir = dir_dict[state[f"dir-{agt_index}"]]
        
        # extract necessary common constants from given domain
        logging.debug(f"necessary common constants from given domain")
        agt_angle = common_constants[f"angle-{agt_index}"]
        
        # agent is able to see anything in the same location
        if tgt_x == agt_x and tgt_y == agt_y:
            return True
        
        # generate two vector
        v1 = np.array((tgt_y - agt_y,tgt_x - agt_x))
        v1 = v1 / np.linalg.norm(v1)
        radians = math.radians(agt_dir)
        v2 = np.array((math.cos(radians),math.sin(radians)))
        logging.debug(f'v1 {v1}, v2 {v2}')
        cos_ = v1.dot(v2)
        d_radians = math.acos(cos_)
        d_degrees = math.degrees(d_radians)
        logging.debug(f'delta angle degree is {round(d_degrees,3)}')
        
        if d_degrees <= agt_angle/2.0 and d_degrees >= - agt_angle/2.0:
            inside = model.T_TYPE.TRUE
        else:
            inside =model.T_TYPE.FALSE
        logging.debug(f'visibility is {inside}')
        return inside
    except AttributeError:
        logging.warning(traceback.format_exc())
        logging.warning("variable not found when check visibility")
        # logging.error("error when checking visibility")
        return T_TYPE.UNKNOWN



# if __name__ == "__main__":
    
#     pass
    

    