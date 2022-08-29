# from model import Problem,E_TYPE,T_TYPE
import logging 
import math
from typing import Tuple
import numpy as np
import traceback
# import model
import re
import pddl_model
import epistemic_model


logger = logging.getLogger("coin")
# import model

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

# # customized evaluation function
# def evaluateK(problem,world,statement):
#     logger.debug(f"evalute knowledge: {statement} in the world: {world}, {type(statement)}, {len(statement)}")
#     #default evaluation for variables
#     print()
#     if not re.search("\([0-9a-z _\-]*,[0-9a-z _\'\"]*\)",statement) == None:
#         var_name = statement.split(",")[0][1:]
#         value = statement.split(",")[1][:-1]
#         if var_name in world.keys():
#             return value == world[var_name]
#         else:
#             return False
#     else:
#         logger.warning("the evaluation of the knowledge equation has not defined")
#         return False

# extract variables from the query
def extractVariables(eq):
    logger.debug(eq)
    # expected output would be a list of (var_name,value)
    if type(eq.q_content) == str:
        # default is a single pair of var_name and value
        if not re.search("\([0-9a-z _\-\'\"]*,[0-9a-z _\'\"]*\)",eq.q_content) == None:
            var_name = eq.q_content.split(",")[0][1:]
            value = eq.q_content.split(",")[1][:-1]
            var_name = var_name.replace("'","").replace('"','')
            value = value.replace("'","").replace('"','')
            return [(var_name,value)]
        else:
            # customized function here
            pass
    else:
        return extractVariables(eq.q_content)
        
# customized evaluation function
def evaluateS(world,statement):
    logger.debug(f"evalute seeing: {statement} in the world: {world}, {type(statement)}, {len(statement)}")
    #default evaluation for variables
    if world == {}:
        return 2
    if not re.search("\([0-9a-z _\-\'\"]*,[0-9a-z _\'\"]*\)",statement) == None:
        var_name = statement.split(",")[0][1:]
        value = statement.split(",")[1][:-1]
        var_name = var_name.replace("'","").replace('"','')
        value = value.replace("'","").replace('"','')
        if var_name in world.keys():
            return 1
        else:
            return 0
    else:
        logger.warning("the evaluation of the seeing equation has not defined")
        return 0



def checkVisibility(problem,state,agt_index,var_index,entities,variables):
    
    logger.debug(f"checkVisibility(_,{state},{agt_index},{var_index})")
    try:
        tgt_index = variables[var_index].v_parent
        # check if the agt_index can be found
        assert(entities[agt_index].e_type==pddl_model.E_TYPE.AGENT)
        
        # agents are able to see each other
        if entities[tgt_index].e_type==pddl_model.E_TYPE.AGENT:
            return pddl_model.convertBooltoT_TYPE(True)
        else:
            
            #extract necessary variables from state
            return  pddl_model.convertBooltoT_TYPE(state[f"peeking-{agt_index}"]=='t')
        
    #     # extract necessary common constants from given domain
    #     # logger.debug(f"necessary common constants from given domain")
    #     agt_angle = common_constants[f"angle-{agt_index}"]
        
    #     # agent is able to see anything in the same location
    #     if tgt_x == agt_x and tgt_y == agt_y:
    #         return model.T_TYPE.TRUE
        
    #     # generate two vector
    #     v1 = np.array((tgt_y - agt_y,tgt_x - agt_x))
    #     v1 = v1 / np.linalg.norm(v1)
    #     radians = math.radians(agt_dir)
    #     v2 = np.array((math.cos(radians),math.sin(radians)))
    #     # logger.debug(f'v1 {v1}, v2 {v2}')
    #     cos_ = v1.dot(v2)
    #     d_radians = math.acos(cos_)
    #     d_degrees = math.degrees(d_radians)
    #     # logger.debug(f'delta angle degree is {round(d_degrees,3)}')
        
    #     if d_degrees <= agt_angle/2.0 and d_degrees >= - agt_angle/2.0:
    #         inside = model.T_TYPE.TRUE
    #     else:
    #         inside =model.T_TYPE.FALSE
    #     # logger.debug(f'visibility is {inside}')
    #     return inside
    except KeyError:
        logger.warning(traceback.format_exc())
        logger.warning("variable not found when check visibility")
        # logger.error("error when checking visibility")
        return pddl_model.T_TYPE.UNKNOWN



# if __name__ == "__main__":
    
#     pass
    

    