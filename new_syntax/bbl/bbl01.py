import logging 
import typing
from util import Function,FunctionSchema,Entity,EntityType,setup_logger, RULE_TYPE
from datetime import datetime

LOGGER_NAME = "bbl"
LOGGER_LEVEL = logging.INFO
# LOGGER_LEVEL = logging.DEBUG

#####
import numpy as np
import math
common_constants = {
    'angle a': 90,
    'angle b': 90,
    'angle c': 90,
    'angle d': 90,
    'angle e': 90,
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

#####

class ExternalFunction:
    logger = None
    
    def __init__(self, handlers):
        self.logger = setup_logger(LOGGER_NAME,handlers,logger_level=LOGGER_LEVEL) 
    
    def checkVisibility(self,state,agent_index,var_name,entities:typing.Dict[str,Entity],
                        functions:typing.Dict[str,Function],
                        function_schemas:typing.Dict[str,FunctionSchema]):
        if not agent_index in entities.keys():
            raise ValueError(f"agent_index [{agent_index}] not found in entities")
        if not entities[agent_index].enetity_type == EntityType.AGENT:
            raise ValueError(f"agent_index [{agent_index}] is not an agent")
        if var_name not in functions.keys():
            raise ValueError(f"var_name [{var_name}] not found in functions")
        
        function = functions[var_name]
        function_schemas_name = function.function_schema_name
        target_list = function.entity_index_list
        
        # for the bbl domain, all visibility function should be the same
        # based on whether the agents physically see the objects/agents or not
        # and all functions in bbl domain have only one entity
        if len(target_list) != 1:
            raise ValueError("all function in bbl should have only one entity",var_name)

        target_index = target_list[0]
        try:
            #extract necessary variables from state
            # logger.debug(f"loading variables from state")
            target_x = state[f"x {target_index}"]
            target_y = state[f"y {target_index}"]
            agent_x = state[f"x {agent_index}"]
            agent_y = state[f"y {agent_index}"]
            agent_dir = dir_dict[state[f"dir {agent_index}"]]
            
            # extract necessary common constants from given domain
            # logger.debug(f"necessary common constants from given domain")
            agent_angle = common_constants[f"angle {agent_index}"]
            
            # agent is able to see anything in the same location
            if target_x == agent_x and target_y == agent_y:
                return True
            
            # generate two vector
            v1 = np.array((target_y - agent_y,target_x - agent_x))
            v1 = v1 / np.linalg.norm(v1)
            radians = math.radians(agent_dir)
            v2 = np.array((math.cos(radians),math.sin(radians)))
            # logger.debug(f'v1 {v1}, v2 {v2}')
            cos_ = v1.dot(v2)
            d_radians = math.acos(cos_)
            d_degrees = math.degrees(d_radians)
            # logger.debug(f'delta angle degree is {round(d_degrees,3)}')
            
            if d_degrees <= agent_angle/2.0 and d_degrees >= - agent_angle/2.0:
                inside = True
            else:
                inside = False
            # logger.debug(f'visibility is {inside}')
            return inside
        except KeyError as e:
            self.logger.debug(e)
            self.logger.debug("state: %s",state)
            return False
        except TypeError as e:
            self.logger.debug(e)
            self.logger.debug("state: %s",state)
            return False
        

    def update1Poly(self,x,paramiters):
        a = int(paramiters[0])
        b = int(paramiters[1])
        return a*x + b
    
    def update2Poly(self,x,paramiters):
        a = int(paramiters[0])
        b = int(paramiters[1])
        c = int(paramiters[2])
        return a*x**2 + b*x + c
    

    def update_state(self, succ_state, path, problem):
        #ranges = problem.value_ranges
        #print(ranges)
        # rule_dict = {}
        # for v_name in domains:
        #     print(domains[v_name].rule_type)
        #     variable_dict  = domains[v_name]
        #     dict_list = str(variable_dict).split(';')
        #     v_rule_type = dict_list[-1].split(':')
        #     type_name = str(v_rule_type[1])[:-2].strip()
        #     rule_dict[v_name] = type_name
            
        x = len(path)-1
        
        updated_state = succ_state
        for v_name in succ_state:
            v_rule_type = problem.rules[v_name].rule_type
            paramiters = problem.rules[v_name].rule_content
            if succ_state is not None and v_name in succ_state and v_rule_type == RULE_TYPE.POLY_1ST:

                updated_value = self.update1Poly(x,paramiters)    ##########change model here
                if self.is_value_in_domain(v_name,updated_value,problem):
                    updated_state[v_name] = updated_value
                else:
                    return None
                #updated_state[v_name] = updated_value
                
                
            if succ_state is not None and v_name in succ_state and v_rule_type ==RULE_TYPE.POLY_2ND:
                updated_value = self.update2Poly(x,paramiters)    ##########change model here
                #updated_state[v_name] = updated_value
                if self.is_value_in_domain(v_name,updated_value,problem):
                    updated_state[v_name] = updated_value
                else:
                    return None
                #print(x,updated_value)
            if succ_state is not None and v_name in succ_state and v_rule_type ==RULE_TYPE.MOD_1ST:
                value = succ_state[v_name]
                #directions = ['ne','e', 'se', 's', 'sw', 'w', 'nw','n']
                ###########################################################################
                function_schema_name = problem.functions[v_name].function_schema_name
                ranges = problem.function_schemas[function_schema_name]
                domain = str(ranges).split(":")[1].split("]")[1].split(")")[0]
                domain = domain[2:].split(",")
                
                directions = list(domain)
                index_of_value = directions.index(value)
                updated_value = directions[(index_of_value + 1) % len(directions)]  
                
                if self.is_value_in_domain(v_name,updated_value,problem):
                    updated_state[v_name] = updated_value
                else:
                    return None
                #updated_state[v_name] = updated_value

        return updated_state
        # if self.is_value_in_domain(v_name,updated_value,problem):
        #     return updated_state
        # else:
        #     return None

    def is_value_in_domain(self, var_name,value,problem):
        function_schema_name = problem.functions[var_name].function_schema_name
        ranges = problem.function_schemas[function_schema_name]
        domain = str(ranges).split(":")[1].split("]")[1].split(")")[0]#.split()[1]#[:-1]
        #print(domain)
        if domain.startswith(' ('):
            domain = domain[2:].split(",")
            value = int(value)
            if value < int(domain[0]) or value > int(domain[1]):
                return False
        return True