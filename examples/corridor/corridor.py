# from model import Problem,E_TYPE,T_TYPE
import logging 
import math
from typing import Tuple
import numpy as np
import traceback

import re
import pddl_model
import epistemic_model

logger = logging.getLogger("bbl")

 
# declare common variables
common_constants = {

}


# # customized evaluation function

# extract variables from the query
def extractVariables(eq):
    # expected output would be a list of (var_name,value)
    if not type(eq) == epistemic_model.EpistemicQuery:
        # print(eq)
        # default is a single pair of var_name and value
        if not re.search("\([0-9a-z _\-\'\"]*,[0-9a-z _\'\"]*\)",eq) == None:
            var_name = eq.split(",")[0][1:]
            value = eq.split(",")[1][:-1]
            return [(var_name.replace('"','').replace("'",''),value.replace('"','').replace("'",''))]
        else:
            # customized function here
            pass
    else:
        return extractVariables(eq.q_content)
        
# customized evaluation function
def evaluateS(world,statement):
    logger.debug(f"evaluate seeing: {statement} in the world: {world}, {type(statement)}, {len(statement)}")
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
        logger.warning("the evaluation of the seeing equation has not defined")
        return 0



def checkVisibility(external,state,agt_index,var_index,entities,variables):
    
    # logger.debug(f"checkVisibility(_,_,{agt_index},{var_index})")
    try:
        tgt_index = variables[var_index].v_parent

        # if the target index is object, which mean it is the secret
        # then the location is same as the location that (shared-s)
        if entities[tgt_index].e_type == pddl_model.E_TYPE.OBJECT:

            tgt_loc = int(state['shared-s'])

            if tgt_loc == 0:
                # if the sercret has not been shared
                return pddl_model.T_TYPE.FALSE
        else:
            # the target is an agent, it has its own location
            tgt_loc = int(state[f'agent_at-{tgt_index}'])

        # check if the agt_index can be found
        assert(entities[agt_index].e_type==pddl_model.E_TYPE.AGENT)

        agt_loc = int(state[f'agent_at-{agt_index}'])

        
        # extract necessary common constants from given domain
        # logger.debug(f"necessary common constants from given domain")

        logger.debug(f'checking seeing with agent location: {agt_loc} and target location: {tgt_loc}')
        # agent is able to see anything in the same location
        if tgt_loc == agt_loc:
            return pddl_model.T_TYPE.TRUE


        # seeing relation for corridor is in the same room or adjuscent room
        if abs(tgt_loc-agt_loc) <=1:
            return pddl_model.T_TYPE.TRUE
        else:
            return pddl_model.T_TYPE.FALSE

    except KeyError:
        logger.warning(traceback.format_exc())
        logger.warning("variable not found when check visibility")
        # logging.error("error when checking visibility")
        return pddl_model.T_TYPE.UNKNOWN
    except TypeError:
        logger.warning(traceback.format_exc())
        logger.warning("variable is None d when check visibility")
        # logging.error("error when checking visibility")
        return pddl_model.T_TYPE.UNKNOWN

# customise action filters
# to filter out the irrelevant actions
def filterActionNames(problem,action_dict):
    return action_dict.keys()

# if __name__ == "__main__":
    
#     pass
    

    