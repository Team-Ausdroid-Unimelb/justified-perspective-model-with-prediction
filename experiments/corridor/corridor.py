# from model import Problem,E_TYPE,PDDL_TERNARY
import logging 
import math
from typing import Tuple
import numpy as np
import traceback
import re

from util import PDDL_TERNARY
from util import EpistemicQuery,E_TYPE
AGENT_ID_PREFIX = "agent_at-"
AGENT_LOC_PREFIX = 'agent_at-'
OBJ_LOC_PREFIX = 'shared-s'

LOGGER_NAME = "corridor"
LOGGER_LEVEL = logging.INFO
from util import setup_logger
 
# declare common variables
common_constants = {

}

class ExternalFunction:
    logger = None
    
    def __init__(self, handlers):
        self.logger = setup_logger(LOGGER_NAME,handlers,logger_level=logging.INFO) 


# # customized evaluation function

# extract variables from the query
    def extractVariables(self,eq):
        # expected output would be a list of (var_name,value)
        if not type(eq) == EpistemicQuery:
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
            return self.extractVariables(eq.q_content)
            
    # customized evaluation function
    def evaluateS(self,world,statement):
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
            self.logger.warning("the evaluation of the seeing equation has not defined")
            return 0
        
    def agentsExists(self,path,g_group_index):
        state = path[-1][0]
        for agt_id in g_group_index:
            if not AGENT_ID_PREFIX+agt_id in state.keys():
                return False
        return True


    # customised function for each domain
    def checkVisibility(self,state,agt_index,var_index,entities,variables):
        
        # logger.debug(f"checkVisibility(_,_,{agt_index},{var_index})")
        try:
            target_index = variables[var_index].v_parent

            # if the target index is object, 
            # which mean it is the secret in corridor domain
            # then its location is same as the location that (shared-s)
            if entities[target_index].e_type == E_TYPE.OBJECT:
                # there is only one secret in corridor
                obj_loc_str = OBJ_LOC_PREFIX + "" 
                if obj_loc_str not in state.keys() or state[obj_loc_str] == None:
                    self.logger.debug('current perspective does not have {}',obj_loc_str)
                    return PDDL_TERNARY.UNKNOWN
                
                target_loc = int(state[obj_loc_str])
                
                if target_loc == 0:
                    self.logger.debug('secret has not been shared')
                    # if the secret has not been shared
                    # but agent might not know
                    return PDDL_TERNARY.UNKNOWN
                
            else:
            # the target is an agent, it has its own location
                target_agent_loc_str = AGENT_LOC_PREFIX+target_index
                if target_agent_loc_str not in state.keys() or state[target_agent_loc_str] == None:
                    self.logger.debug('current perspective does not have {}',target_agent_loc_str)
                    return PDDL_TERNARY.UNKNOWN
                
                target_loc = int(state[target_agent_loc_str])

            # check if the agt_index can be found
            assert(entities[agt_index].e_type==E_TYPE.AGENT)

            agent_loc_str = AGENT_LOC_PREFIX+agt_index
            if agent_loc_str not in state.keys() or state[agent_loc_str] == None:
                self.logger.debug('current perspective does not have {}',agent_loc_str)
                return PDDL_TERNARY.UNKNOWN

            agt_loc = int(state[agent_loc_str])

            
            # extract necessary common constants from given domain
            # logger.debug(f"necessary common constants from given domain")

            self.logger.debug('checking seeing with agent location: {} and target location: {}',agt_loc,target_loc)
            # # agent is able to see anything in the same location
            # if target_loc == agt_loc:
            #     return PDDL_TERNARY.TRUE

            # agent is able to see anything in the same or adjacent rooms
            if abs(target_loc-agt_loc) <=1:
                return PDDL_TERNARY.TRUE
            else:
                return PDDL_TERNARY.FALSE

        except KeyError:
            self.logger.warning(traceback.format_exc())
            self.logger.warning("variable not found when check visibility")
            # logging.error("error when checking visibility")
            return PDDL_TERNARY.UNKNOWN
        except TypeError:
            self.logger.warning(traceback.format_exc())
            self.logger.warning("variable is None d when check visibility")
            # logging.error("error when checking visibility")
            return PDDL_TERNARY.UNKNOWN

    # customise action filters
    # to filter out the irrelevant actions
    def filterActionNames(self,problem,action_dict):
        return action_dict.keys()

    # if __name__ == "__main__":
        
    #     pass
    

    